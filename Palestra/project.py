# modules-import
import array

import classes

# flask-import
from flask import Flask, render_template, request, redirect, url_for, make_response
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from flask_migrate import Migrate

# sqlalchemy-import
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

# other-import
from werkzeug.utils import redirect
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

#######################
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

# Sessione
Session = sessionmaker(bind=engine)
session = Session()

#############################
# Variabili e costanti globali
first_id_client = 100
admim_email = 'admin@palestra.it'
admim_pwd = 'admin'


# Functions
# user_loader
@login_manager.user_loader
def load_user(user_id):
    conn = engine.connect()
    #rs = conn.execute('SELECT * FROM utenti WHERE id = %s' % user_id)
    #user = rs.fetchone()
    p_query = "SELECT * FROM utenti WHERE id = %s"
    user = conn.engine.execute(p_query, user_id).first()
    conn.close()
    return classes.User(user.id, user.username, user.password, user.nome, user.cognome, user.email, user.datanascita)


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


# Routes
@app.route('/')
def home():
    i = datetime.now()
    mydate = classes.MyDate()
    return render_template("index.html", month=i.month, year=i.year, day=i.day, first_column=mydate.first_column, last_day=mydate.last_day)


@app.route('/wrong')
def wrong():
    return render_template("wrong.html")


@app.route('/signup')
def signup():
    return render_template("signup.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        p_email = request.form['user']
        p_pass = request.form['pass']
        conn = engine.connect()
        p_query = "SELECT password AS password FROM utenti WHERE email = %s"
        real_pwd = conn.engine.execute(p_query, p_email).first()
        conn.close()

        if p_email == admim_email:
            if real_pwd is not None and p_pass == real_pwd['password']:
                user = get_user_by_email(request.form['user'])
                login_user(user)
                return redirect(url_for('administration'))
            else:
                return redirect(url_for('wrong'))
        elif real_pwd is not None:
            if p_pass == real_pwd['password']:
                user = get_user_by_email(request.form['user'])
                login_user(user) # chiamata a Flask - Login
                return redirect(url_for('private'))
            else:
                return redirect(url_for('wrong'))
        else:
            print('NO2')
            return redirect(url_for('wrong'))
    else:
        return redirect(url_for('wrong'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/reserved_private')
def reserved():
    if current_user.is_authenticated:
        return private()
    return render_template("signin.html")


@app.route('/private')
@login_required
def private():
    sub = is_subscriber(current_user.id)
    resp = make_response(render_template("private.html", current_user=current_user, sub=sub))
    return resp


@app.route('/administration')
@login_required
def administration():
    if current_user == get_admin_user():
        resp = make_response(render_template("administration.html", current_user=current_user))
        return resp
    else:
        resp = make_response(render_template("private.html", current_user=current_user))
        return resp


@app.route('/create', methods=['GET', 'POST'])
def create_user():
    new_id = get_id_increment()
    user = classes.User(id=new_id, username=request.form['username'], password=request.form['password'], nome=request.form['nome'], cognome=request.form['cognome'], email=request.form['email'], datanascita=request.form['dataNascita'])
    client = classes.Client(id=new_id)
    session.add(user)
    session.add(client)
    if request.form['abbonamento'] != "null":
        sub = get_subscription(request.form['abbonamento'])
        if request.form['abbonamento'] == "prova":
            subscriber = classes.Subscriber(id=new_id, abbonamento=sub.id, datainizioabbonamento=get_current_date(), datafineabbonamento=get_increment_date(int(request.form['durata'])), durata=null)
            session.add(subscriber)
        else:
            subscriber = classes.Subscriber(id=new_id, abbonamento=sub.id, datainizioabbonamento=get_current_date(), datafineabbonamento=get_increment_date(int(request.form['durata'])), durata=request.form['durata'])
            session.add(subscriber)
    session.commit()
    return render_template("confirm.html")


@app.route('/subscribe', methods=['GET', 'POST'])
@login_required
def subscribe():
    user_id = current_user.id
    if not is_subscriber(user_id) and request.form['abbonamento'] != "null":
        sub = get_subscription(request.form['abbonamento'])
        if request.form['abbonamento'] == "prova":
            subscriber = classes.Subscriber(id=user_id, abbonamento=sub.id, datainizioabbonamento=get_current_date(), datafineabbonamento=get_increment_date(int(request.form['durata'])), durata=null)
            session.add(subscriber)
        else:
            subscriber = classes.Subscriber(id=user_id, abbonamento=sub.id, datainizioabbonamento=get_current_date(), datafineabbonamento=get_increment_date(int(request.form['durata'])), durata=request.form['durata'])
            session.add(subscriber)
        session.commit()
        return render_template("confirm_private.html")
    else:
        return render_template("wrong.html")


@app.route('/info')
def info():
    return render_template("info.html", courses=get_courses(), rooms=get_rooms(), weight_rooms=get_weight_rooms(), trainers=get_trainers(), clients=get_clients())


@app.route('/info_user', methods=['GET', 'POST'])
@login_required
def info_user():
    return render_template("info_user.html")


@app.route('/calendar', methods=['GET', 'POST'])
@login_required
def calendar():
    i = datetime.now()
    mydate = classes.MyDate()
    return render_template("calendar.html", month=i.month, year=i.year, day=i.day, first_column=mydate.first_column, last_day=mydate.last_day)


@app.route('/subscribe_course', methods=['GET', 'POST'])
@login_required
def subscribe_course():
    return render_template("subscribe_course.html")