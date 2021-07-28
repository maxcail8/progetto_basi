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
    p_query = "SELECT * FROM corsi"
    courses = conn.engine.execute(p_query)
    conn.close()
    return courses


def get_rooms():
    conn = engine.connect()
    p_query = "SELECT * FROM stanze"
    rooms = conn.engine.execute(p_query)
    conn.close()
    return rooms


def get_weight_rooms():
    conn = engine.connect()
    p_query = "SELECT * FROM salepesi"
    weight_rooms = conn.engine.execute(p_query)
    conn.close()
    return weight_rooms


def get_trainers():
    conn = engine.connect()
    p_query = "SELECT * FROM istruttori NATURAL JOIN utenti"
    trainers = conn.engine.execute(p_query)
    conn.close()
    return trainers


def get_clients():
    conn = engine.connect()
    p_query = "SELECT * FROM clienti NATURAL JOIN utenti"
    clients = conn.engine.execute(p_query)
    conn.close()
    return clients


def is_subscriber(user_id):
    conn = engine.connect()
    p_query = "SELECT * FROM abbonati WHERE id = %s"
    sub = conn.engine.execute(p_query, user_id).first()
    conn.close()
    if sub is not None:
        return True
    else:
        return False