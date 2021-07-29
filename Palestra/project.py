# modules-import
import classes
import functions

# flask-import
from flask import Flask, render_template, request, url_for, make_response
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from flask_migrate import Migrate

# sqlalchemy-import
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

# other-import
from werkzeug.utils import redirect
from datetime import datetime

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
Session.close_all()
session = Session()

#############################
# Variabili e costanti globali
first_id_client = 100
admin_email = 'admin@palestra.it'
admin_pwd = 'admin'


#user-loader
@login_manager.user_loader
def load_user(user_id):
    conn = engine.connect()
    #rs = conn.execute('SELECT * FROM utenti WHERE id = %s' % user_id)
    #user = rs.fetchone()
    p_query = "SELECT * FROM utenti WHERE id = %s"
    user = conn.engine.execute(p_query, user_id).first()
    conn.close()
    return classes.User(user.id, user.username, user.password, user.nome, user.cognome, user.email, user.datanascita)


# Routes
@app.route('/')
def home():
    i = datetime.now()
    mydate = classes.MyDate()
    return render_template("index.html", month=i.month, year=i.year, day=i.day, first_column=mydate.first_column, last_day=mydate.last_day)


@app.route('/signup')
def signup():
    return render_template("signup.html")


@app.route('/create', methods=['GET', 'POST'])
def create_user():
    new_id = functions.get_id_increment()
    user = classes.User(id=new_id, username=request.form['username'], password=request.form['password'], nome=request.form['nome'], cognome=request.form['cognome'], email=request.form['email'], datanascita=request.form['dataNascita'])
    client = classes.Client(id=new_id)
    session.add(user)
    session.add(client)
    if request.form['abb'] != 'null':
        sub = functions.get_subscription(request.form['abb'])
        if request.form['abb'] == 'prova':
            subscriber = classes.Subscriber(id=new_id, abbonamento=sub.id, datainizioabbonamento=functions.get_current_date(), datafineabbonamento=functions.get_increment_date(int(request.form['durata'])), durata=null)
            session.add(subscriber)
        else:
            subscriber = classes.Subscriber(id=new_id, abbonamento=sub.id, datainizioabbonamento=functions.get_current_date(), datafineabbonamento=functions.get_increment_date(int(request.form['durata'])), durata=request.form['durata'])
            session.add(subscriber)
    session.commit()
    return render_template("confirm.html")


@app.route('/reserved_private')
def reserved():
    if current_user.is_authenticated:
        return private()
    return render_template("signin.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        p_email = request.form['user']
        p_pass = request.form['pass']
        conn = engine.connect()
        p_query = "SELECT password AS password FROM utenti WHERE email = %s"
        real_pwd = conn.engine.execute(p_query, p_email).first()
        conn.close()

        if p_email == admin_email:
            if real_pwd is not None and p_pass == real_pwd['password']:
                user = functions.get_user_by_email(request.form['user'])
                login_user(user)
                return redirect(url_for('administration'))
            else:
                return render_template("wrong.html")
        elif real_pwd is not None:
            if p_pass == real_pwd['password']:
                user = functions.get_user_by_email(request.form['user'])
                login_user(user) # chiamata a Flask - Login
                return redirect(url_for('private'))
            else:
                return render_template("wrong.html")
        else:
            print('NO2')
            return render_template("wrong.html")
    else:
        return render_template("wrong.html")


@app.route('/private')
@login_required
def private():
    if current_user == functions.get_admin_user():
        info = functions.get_information()
        resp = make_response(render_template("administration.html", current_user=current_user, accessi_settimana=info.accessisettimana, slot_giorno=info.slotgiorno, persone_max=info.personemaxslot))
        return resp
    else:
        sub = functions.is_subscriber(current_user.id)
        resp = make_response(render_template("private.html", current_user=current_user, sub=sub))
        return resp


@app.route('/subscribe_course', methods=['GET', 'POST'])
@login_required
def subscribe_course():
    return render_template("subscribe_course.html")


@app.route('/subscribe', methods=['GET', 'POST'])
@login_required
def subscribe():
    user_id = current_user.id
    if not functions.is_subscriber(user_id) and request.form['abb'] != 'null':
        sub = functions.get_subscription(request.form['abb'])
        if request.form['abb'] == 'prova':
            subscriber = classes.Subscriber(id=user_id, abbonamento=sub.id, datainizioabbonamento=functions.get_current_date(), datafineabbonamento=functions.get_increment_date(int(request.form['durata'])), durata=null)
            session.add(subscriber)
        else:
            subscriber = classes.Subscriber(id=user_id, abbonamento=sub.id, datainizioabbonamento=functions.get_current_date(), datafineabbonamento=functions.get_increment_date(int(request.form['durata'])), durata=request.form['durata'])
            session.add(subscriber)
        session.commit()
        return render_template("confirm.html")
    else:
        return render_template("wrong.html")


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


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/info')
def info():
    return render_template("info.html", courses=functions.get_courses(), rooms=functions.get_rooms(), weight_rooms=functions.get_weight_rooms(), trainers=functions.get_trainers(), clients=functions.get_clients())


@app.route('/administration')
@login_required
def administration():
    if current_user == functions.get_admin_user():
        info = functions.get_information()
        resp = make_response(render_template("administration.html", current_user=current_user, accessi_settimana=info.accessisettimana, slot_giorno=info.slotgiorno, persone_max=info.personemaxslot))
        return resp
    else:
        sub = functions.is_subscriber(current_user.id)
        resp = make_response(render_template("private.html", current_user=current_user, sub=sub))
        return resp


@app.route('/edit_information', methods=['GET', 'POST'])
@login_required
def edit_information():
    if current_user == functions.get_admin_user():
        functions.set_information(request.form['accessiSettimana'], request.form['tempoAllenamento'], request.form['personeMassime'])
        return render_template("confirm.html")
    else:
        return render_template("wrong.html")


@app.route('/edit_courses', methods=['GET', 'POST'])
@login_required
def edit_courses():
    if current_user == functions.get_admin_user():
        courses = functions.get_courses()
        return render_template("edit_courses.html", courses=courses)
    else:
        return render_template("wrong.html")


@app.route('/edit_rooms', methods=['GET', 'POST'])
@login_required
def edit_rooms():
    if current_user == functions.get_admin_user():
        rooms = functions.get_rooms()
        rooms2 = functions.get_rooms()
        return render_template("edit_rooms.html", rooms=rooms, rooms2=rooms2)
    else:
        return render_template("wrong.html")


@app.route('/edit_weight_rooms', methods=['GET', 'POST'])
@login_required
def edit_weight_rooms():
    if current_user == functions.get_admin_user():
        weight_rooms = functions.get_weight_rooms()
        weight_rooms2 = functions.get_weight_rooms()
        return render_template("edit_weight_rooms.html", weight_rooms=weight_rooms, weight_rooms2=weight_rooms2)
    else:
        return render_template("wrong.html")


@app.route('/add_weight_room', methods=['GET', 'POST'])
@login_required
def add_weight_room():
    if current_user == functions.get_admin_user():
        functions.add_weight_room(request.form['dim'])
        return render_template("confirm.html")
    else:
        return render_template("wrong.html")


@app.route('/remove_weight_room', methods=['GET', 'POST'])
@login_required
def remove_weight_room():
    if current_user == functions.get_admin_user():
        functions.remove_weight_room(request.form['idSala'])
        return render_template("confirm.html")
    else:
        return render_template("wrong.html")


@app.route('/update_weight_room', methods=['GET', 'POST'])
@login_required
def update_weight_room():
    if current_user == functions.get_admin_user():
        functions.update_weight_room(request.form['idSala'], request.form['dim'])
        return render_template("confirm.html")
    else:
        return render_template("wrong.html")