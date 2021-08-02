#modules-import
import classes

# flask-import
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate

# sqlalchemy-import
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *

# other-import
from datetime import datetime, timedelta

# Parametri applicazione
app = Flask(__name__)
engine = create_engine('postgresql://postgres:postgres@localhost:5432/progetto_palestra', echo=True)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/progetto_palestra"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Secret key
# app.config['SECRET_KEY'] = 'secret11'
app.secret_key = 'secret14'

# Gestione login
login_manager = LoginManager()
login_manager.init_app(app)

#############################
# Variabili e costanti globali
first_id_client = 100


# Functions
# GETTERS
def get_user_by_email(email):
    conn = engine.connect()
    p_query = "SELECT * FROM utenti WHERE email = %s"
    user = conn.engine.execute(p_query, email).first()
    conn.close()
    return classes.User(user.id, user.username, user.password, user.nome, user.cognome, user.email, user.datanascita)


# Funzione per autoincrementare id tramite query
def get_id_increment():
    conn = engine.connect()
    p_query = "SELECT * FROM utenti WHERE id>=100 ORDER BY id DESC"
    user = conn.engine.execute(p_query).first()
    conn.close()
    if(user is not None):
        return user.id + 1
    else:
        return first_id_client


# Funzione per tornare l'utente amministratore
def get_admin_user():
    conn = engine.connect()
    p_query = "SELECT * FROM utenti WHERE id = 0"
    user = conn.engine.execute(p_query).first()
    conn.close()
    return classes.User(user.id, user.username, user.password, user.nome, user.cognome, user.email, user.datanascita)


def get_current_date():
    now = datetime.now()
    return now.strftime("%Y-%m-%d")


def get_increment_date(giorni):
    data = datetime.now() + timedelta(days=giorni)
    return data.strftime("%Y-%m-%d")


def get_subscription(subscription):
    conn = engine.connect()
    p_query = "SELECT * FROM abbonamenti WHERE tipo = %s"
    sub = conn.engine.execute(p_query, subscription).first()
    conn.close()
    return classes.Subscription(sub.id, sub.tipo, sub.costo)


def get_courses():
    conn = engine.connect()
    p_query = "SELECT * FROM corsi ORDER BY id ASC"
    courses = conn.engine.execute(p_query)
    conn.close()
    return courses


def get_course(idCorso):
    conn = engine.connect()
    p_query = "SELECT * FROM corsi WHERE id = %s"
    course = conn.engine.execute(p_query, idCorso).first()
    conn.close()
    return classes.Course(course.id, course.nome, course.iscrittimax, course.istruttore, course.stanza)


def get_rooms():
    conn = engine.connect()
    p_query = "SELECT * FROM stanze ORDER BY id ASC"
    rooms = conn.engine.execute(p_query)
    conn.close()
    return rooms


def get_weight_rooms():
    conn = engine.connect()
    p_query = "SELECT * FROM salepesi ORDER BY id ASC"
    weight_rooms = conn.engine.execute(p_query)
    conn.close()
    return weight_rooms


def get_trainers():
    conn = engine.connect()
    p_query = "SELECT * FROM istruttori NATURAL JOIN utenti ORDER BY id ASC"
    trainers = conn.engine.execute(p_query)
    conn.close()
    return trainers


def get_clients():
    conn = engine.connect()
    p_query = "SELECT * FROM clienti NATURAL JOIN utenti ORDER BY id ASC"
    clients = conn.engine.execute(p_query)
    conn.close()
    return clients


def get_information():
    conn = engine.connect()
    p_query = "SELECT * FROM informazioni"
    info = conn.engine.execute(p_query).first()
    conn.close()
    return classes.Information(info.accessisettimana, info.slotgiorno, info.personemaxslot, info.personemq)


# BOOLEANS
def is_subscriber(user_id):
    conn = engine.connect()
    p_query = "SELECT * FROM abbonati WHERE id = %s"
    sub = conn.engine.execute(p_query, user_id).first()
    conn.close()
    if sub is not None:
        return True
    else:
        return False


# UPDATE
def set_information(accessiSettimana, slotGiorno, personeMax, personeMq):
    conn = engine.connect()
    p_query = "UPDATE informazioni SET accessisettimana = %s, slotgiorno = %s, personemaxslot = %s, personemq = %s"
    conn.engine.execute(p_query, accessiSettimana, slotGiorno, personeMax, personeMq)
    conn.close()


def update_weight_room(idSala, dimensione):
    conn = engine.connect()
    p_query = "UPDATE salepesi SET dimensione = %s WHERE id = %s"
    conn.engine.execute(p_query, dimensione, idSala)
    conn.close()


def update_room(idStanza, nome, dimensione):
    conn = engine.connect()
    p_query = "UPDATE stanze SET nome = %s, dimensione = %s WHERE id = %s"
    conn.engine.execute(p_query, nome, dimensione, idStanza)
    conn.close()


def update_course(idCorso, nome, iscrittiMax, idIstruttore, idStanza):
    conn = engine.connect()
    p_query = "UPDATE corsi SET nome = %s, iscrittimax = %s, istruttore = %s, stanza = %s WHERE id = %s"
    conn.engine.execute(p_query, nome, iscrittiMax, idIstruttore, idStanza, idCorso)
    conn.close()


# ADD
def add_weight_room(dimensione):
    conn = engine.connect()
    p_query = "INSERT INTO salepesi(dimensione) VALUES (%s)"
    conn.engine.execute(p_query, dimensione)
    conn.close()


def add_room(nome, dimensione):
    conn = engine.connect()
    p_query = "INSERT INTO stanze(nome, dimensione) VALUES (%s, %s)"
    conn.engine.execute(p_query, nome, dimensione)
    conn.close()


def add_course(nome, iscrittimax, idIstruttore, idStanza):
    conn = engine.connect()
    p_query = "INSERT INTO corsi(nome, iscrittimax, istruttore, stanza) VALUES (%s, %s, %s, %s)"
    conn.engine.execute(p_query, nome, iscrittimax, idIstruttore, idStanza)
    conn.close()


# REMOVE
def remove_weight_room(idSala):
    conn = engine.connect()
    p_query = "DELETE FROM salepesi WHERE id = %s"
    conn.engine.execute(p_query, idSala)
    conn.close()


def remove_room(idStanza):
    conn = engine.connect()
    p_query = "DELETE FROM stanze WHERE id = %s"
    conn.engine.execute(p_query, idStanza)
    conn.close()


def remove_course(idCorso):
    conn = engine.connect()
    p_query = "DELETE FROM corsi WHERE id = %s"
    conn.engine.execute(p_query, idCorso)
    conn.close()


# Day of week: select extract(dow from date '2021-07-30');