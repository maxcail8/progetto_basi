from flask import Flask, render_template, request, redirect, url_for, make_response
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from werkzeug.utils import redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_migrate import Migrate

app = Flask(__name__)
#engine = create_engine('postgresql://postgres:password@localhost:5432/progetto_palestra', echo=True)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:password@localhost:5432/progetto_palestra"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class CarsModel(db.Model):
    __tablename__ = 'cars'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    model = db.Column(db.String())
    doors = db.Column(db.Integer())

    def __init__(self, name, model, doors):
        self.name = name
        self.model = model
        self.doors = doors

    def __repr__(self):
        return f"<Car {self.name}>"










'''
class User(UserMixin):
    # costruttore di classe
    def __init__(self, id_, email, pwd):
        self.id = id_
        self.email = email
        self.pwd = pwd

def get_user_by_email(email):
    conn = engine.connect()
    rs = conn.execute('SELECT * FROM Users WHERE email = ?', email)
    user = rs.fetchone()
    conn.close()
    return User(user.id, user.email, user.pwd)

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(user_id)
    if user:
        return DbUser(user)
    else:
        return None

@login_manager.user_loader # attenzione a questo!
def load_user(user_id):
    conn = engine.connect()
    rs = conn.execute('SELECT * FROM Users WHERE id = ?', user_id)
    user = rs.fetchone()
    conn.close()
    return User(user.id, user.email, user.pwd)

@app.route('/')
def home():
    # current_user identifica l'utente attuale
    # utente anonimo prima dell'autenticazione
    if current_user.is_authenticated:
        return redirect(url_for('private'))
    return render_template("base.html")

@app.route('/login', methods =['GET', 'POST'])
def login():
    if request.method == 'POST':
        conn = engine.connect()
        rs = conn.execute('SELECT pwd FROM Users WHERE email = ?', [request.form['user']])
        real_pwd = rs.fetchone()
        conn.close()

        if(real_pwd is not None):
            if request.form['pass'] == real_pwd['pwd']:
                user = get_user_by_email(request.form['user'])
                login_user(user) # chiamata a Flask - Login
                return redirect(url_for('private'))
            else:
                return redirect(url_for('home'))
        else:
            return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))
        
@app.route('/private')
@login_required # richiede autenticazione
def private():
    conn = engine.connect()
    users = conn.execute('SELECT * FROM Users')
    resp = make_response(render_template("private.html", users = users))
    conn.close()
    return resp

@app.route('/logout')
@login_required # richiede autenticazione
def logout():
    logout_user() #chiamata a Flask - Login
    return redirect(url_for('home'))
'''

# set FLASK_APP=project.py
# flask run
# pacchetto flask-sqlalchemy