#modules-import
import classes

# flask-import
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate

# sqlalchemy-import
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

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

#Session
Session = sessionmaker(bind=engine)
Session.close_all()
session = Session()

#############################
# Variabili e costanti globali
first_id_client = 100


# Functions
# GETTERS
def get_subscriber_by_id(id):
    conn = engine.connect()
    p_query = "SELECT * FROM abbonati WHERE id = %s"
    subscriber = conn.engine.execute(p_query, id).first()
    conn.close()
    return classes.Subscriber(subscriber.id, subscriber.abbonamento, subscriber.datafineabbonamento, subscriber.datafineabbonamento, subscriber.durata)


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


def get_course_id_increment():
    conn = engine.connect()
    p_query = "SELECT * FROM corsi ORDER BY id DESC"
    course = conn.engine.execute(p_query).first()
    conn.close()
    if (course is not None):
        return course.id + 1
    else:
        return 0


def get_room_id_increment():
    conn = engine.connect()
    p_query = "SELECT * FROM stanze ORDER BY id DESC"
    room = conn.engine.execute(p_query).first()
    conn.close()
    if (room is not None):
        return room.id + 1
    else:
        return 0


def get_weight_room_id_increment():
    conn = engine.connect()
    p_query = "SELECT * FROM salepesi ORDER BY id DESC"
    weight_room = conn.engine.execute(p_query).first()
    conn.close()
    if(weight_room is not None):
        return weight_room.id + 1
    else:
        return 0


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


def get_subscription_by_id(id):
    conn = engine.connect()
    p_query = "SELECT * FROM abbonamenti WHERE id = %s"
    sub = conn.engine.execute(p_query, id).first()
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


def get_last_id_course():
    conn = engine.connect()
    p_query = "SELECT * FROM corsi ORDER BY id DESC"
    course = conn.engine.execute(p_query).first()
    conn.close()
    return course.id


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


def get_checks():
    conn = engine.connect()
    p_query = "SELECT * FROM controlli"
    checks = conn.engine.execute(p_query).first()
    conn.close()
    return classes.Checks(checks.controllo)


def get_slot_from_date(data):
    conn = engine.connect()
    p_query = "SELECT * FROM slot WHERE giorno = DATE %s"
    slots = conn.engine.execute(p_query, data)
    conn.close()
    return slots


def get_slot_weight_rooms(idSlot, subscription):
    if subscription=='corsi':
        return None
    else:
        conn = engine.connect()
        p_query = "SELECT salapesi FROM salapesislot WHERE slot= %s"
        weightrooms = conn.engine.execute(p_query, idSlot)
        conn.close()
        return weightrooms


def get_slot_courses(idSlot, subscription):
    if subscription=='sala_pesi':
        return None
    else:
        conn = engine.connect()
        p_query = "SELECT corso FROM corsislot WHERE slot= %s"
        courses = conn.engine.execute(p_query, idSlot)
        conn.close()
        return courses


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
def set_checks(controlliGiornalieri):
    conn = engine.connect()
    p_query = "UPDATE controlli SET controllo = %s"
    conn.engine.execute(p_query, controlliGiornalieri)
    conn.close()


def set_information_accessisettimana(accessiSettimana):
    conn = engine.connect()
    p_query = "UPDATE informazioni SET accessisettimana = %s"
    conn.engine.execute(p_query, accessiSettimana)
    conn.close()


def set_information_slotgiorno(slotGiorno):
    conn = engine.connect()
    p_query = "UPDATE informazioni SET slotgiorno = %s"
    conn.engine.execute(p_query, slotGiorno)
    conn.close()


def set_information_personemaxslot(personeMax):
    conn = engine.connect()
    p_query = "UPDATE informazioni SET personemaxslot = %s"
    conn.engine.execute(p_query, personeMax)
    conn.close()


def set_information_personemq(personeMq):
    conn = engine.connect()
    p_query = "UPDATE informazioni SET personemq = %s"
    conn.engine.execute(p_query, personeMq)
    conn.close()


def update_weight_room(idSala, dimensione):
    conn = engine.connect()
    pmq = get_information().personemq
    p_query = "UPDATE salepesi SET dimensione = %s, iscrittimax = %s WHERE id = %s"
    conn.engine.execute(p_query, dimensione, int(dimensione)/pmq, idSala)
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


# REMOVE
def remove_room(idStanza):
    conn = engine.connect()
    p_query = "DELETE FROM stanze WHERE id = %s"
    conn.engine.execute(p_query, idStanza)
    conn.close()


def remove_weight_room(idSala):
    conn = engine.connect()
    p_query = "DELETE FROM salepesi WHERE id = %s"
    conn.engine.execute(p_query, idSala)
    conn.close()


def remove_course(idCorso):
    conn = engine.connect()
    p_query = "DELETE FROM corsi WHERE id = %s"
    conn.engine.execute(p_query, idCorso)
    conn.close()


def remove_not_subscriber(idCliente):
    conn = engine.connect()
    p_query = "DELETE FROM nonabbonati WHERE id = %s"
    conn.engine.execute(p_query, idCliente)
    conn.close()


# ADD
def add_course_slot(idCorso, giorno, orario):
    p_query = "CALL aggiungi_corsi_slot(" + str(idCorso) + ", " + str(giorno) + ", TIME '" + str(orario) + "')"
    session.execute(p_query)
    session.commit()
    session.close()


# Day of week: select extract(dow from date '2021-07-30');