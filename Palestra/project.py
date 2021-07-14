#modules-import
import classes

#flask-import
from flask import Flask, render_template, request, redirect, url_for, make_response
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from flask_migrate import Migrate

#sqlalchemy-import
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

#other-import
from werkzeug.utils import redirect

#######################
#Parametri applicazione
app = Flask(__name__)
engine = create_engine('postgresql://postgres:postgres@localhost:5432/progetto_palestra', echo=True)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/progetto_palestra"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#Secret key
#app.config['SECRET_KEY'] = 'secret11'
app.secret_key = 'secret14'

#Gestione login
login_manager = LoginManager()
login_manager.init_app(app)

#Sessione
Session = sessionmaker(bind=engine)
session = Session()

#############################
#Variabili e costanti globali
first_id_client = 100
admim_email = 'admin@palestra.it'
admim_pwd = 'admin'

#Functions
def get_user_by_email(email):
    conn = engine.connect()
    p_query = "SELECT * FROM utenti WHERE email = %s"
    user = conn.engine.execute(p_query, email).first()
    conn.close()
    return classes.User(user.id, user.username, user.password, user.nome, user.cognome, user.email, user.datanascita)

#Funzione per autoincrementare id tramite query
def get_id_increment():
    conn = engine.connect()
    p_query = "SELECT * FROM utenti WHERE id>=100 ORDER BY id DESC"
    user = conn.engine.execute(p_query).first()
    conn.close()
    if(user is not None):
        return user.id + 1
    else:
        return first_id_client

#Funzione per tornare l'utente amministratore
def get_admin_user():
    conn = engine.connect()
    rs = conn.execute('SELECT * FROM utenti WHERE id = 0')
    user = rs.fetchone()
    conn.close()
    return classes.User(user.id, user.username, user.password, user.nome, user.cognome, user.email, user.datanascita)

#user_loader
@login_manager.user_loader
def load_user(user_id):
    conn = engine.connect()
    rs = conn.execute('SELECT * FROM utenti WHERE id = %s' % user_id)
    user = rs.fetchone()
    conn.close()
    return classes.User(user.id, user.username, user.password, user.nome, user.cognome, user.email, user.datanascita)


#self, username, password, nome, cognome, email, datanascita):
#Routes
@app.route('/')
def home():
    return render_template("index.html")


@app.route('/signup')
def signup():
    return render_template("signup.html")


@app.route('/login', methods =['GET', 'POST'])
def login():
    if request.method == 'POST':
        p_email = request.form['user']
        p_pass = request.form['pass']
        conn = engine.connect()
        p_query = "SELECT password AS password FROM utenti WHERE email = %s"
        real_pwd = conn.engine.execute(p_query, p_email).first()
        print('real_pwd %s', real_pwd)
        conn.close()

        if p_email == admim_email:
            print('NO')
            if real_pwd is not None and p_pass == real_pwd['password']:
                user = get_user_by_email(request.form['user'])
                login_user(user)
                return redirect(url_for('administration'))
            else:
                return redirect(url_for('home'))
        elif(real_pwd is not None):
            print('SI')
            if p_pass == real_pwd['password']:
                user = get_user_by_email(request.form['user'])
                login_user(user) # chiamata a Flask - Login
                return redirect(url_for('private'))
            else:
                return redirect(url_for('home'))
        else:
            print('NO2')
            return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))


@app.route('/reserved_private')
def reserved():
    if current_user.is_authenticated:
        return private()
    return render_template("base.html")


@app.route('/private')
@login_required
def private():
    resp = make_response(render_template("private.html", current_user=current_user))
    return resp


@app.route('/administration')
@login_required
def administration():
    if current_user == get_admin_user():
        resp = make_response(render_template("administration.html", current_user=current_user))
        return resp
    else:
        ###############################################################
        resp = make_response(render_template("private.html", current_user=current_user))
        return resp

@app.route('/calendar')
@login_required
def calendar():
    resp = make_response(render_template("calendar.html", current_user=current_user))
    return resp


@app.route('/create', methods=['GET', 'POST'])
def create_user():
    new_id = get_id_increment()
    user = classes.User(id=new_id, username=request.form['username'], password=request.form['password'], nome=request.form['nome'],
                cognome=request.form['cognome'], email=request.form['email'], datanascita=request.form['dataNascita'])
    client = classes.Client(id=new_id)
    print(user)
    print(client)
    session.add(user)
    session.add(client)
    session.commit()
    return render_template("conferma.html")


@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('home'))