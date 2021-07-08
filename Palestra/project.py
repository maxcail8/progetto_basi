import sys

import sqlalchemy
import enum

#flask-import
from flask import Flask, render_template, request, redirect, url_for, make_response
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from flask_migrate import Migrate

#sqlalchemy-import
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, relation, sessionmaker

#other-import
from werkzeug.utils import redirect

################################################################
#Parametri applicazione
app = Flask(__name__)
engine = create_engine('postgresql://postgres:postgres@localhost:5432/progetto_palestra', echo=True)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/progetto_palestra"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#Secret key
#app.config['SECRET_KEY'] = 'secret11'
app.secret_key = 'secret13'

#Gestione login
login_manager = LoginManager()
login_manager.init_app(app)

#Sessione
Session = sessionmaker(bind=engine)
session = Session()
################################################################
Base = declarative_base()
################################################################

#Dichiarazione Classi-Tabelle

class User(UserMixin):
    __tablename__ = 'utenti'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    nome = Column(String)
    cognome = Column(String)
    email = Column(String)
    dataNascita = Column(Date)

    #primary key progressiva
    def __init__(self, id, username, password, nome, cognome, email, dataNascita):
        self.id = id
        self.username = username
        self.password = password
        self.nome = nome
        self.cognome = cognome
        self.email = email
        self.dataNascita = dataNascita

    def __repr__(self):
        return "<User(username = {0}, nome= {1}, cognome = {2}, email = {3})>".format(self.username, self.nome, self.cognome, self.email)

class Trainer(UserMixin):
    __tablename__ = 'istruttori'

    id = Column(Integer, ForeignKey(User.id, ondelete='cascade'), primary_key=True)
    user = relationship(User, uselist=False)

    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return "<Trainer(username = {0}, nome= {1}, cognome = {2}, email = {3})>".format(self.user.username, self.user.nome, self.user.cognome, self.user.email)


class Other(UserMixin):
    __tablename__ = 'altri'

    id = Column(Integer, ForeignKey(User.id, ondelete='cascade'), primary_key=True)
    user = relationship(User, uselist=False)

    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return "<Other(username = {0}, nome= {1}, cognome = {2}, email = {3})>".format(self.user.username, self.user.nome, self.user.cognome, self.user.email)


class Client(UserMixin):
    __tablename__ = 'clienti'

    id = Column(Integer, ForeignKey(User.id, ondelete='cascade'), primary_key=True)
    user = relationship(User, uselist=False)

    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return "<Client(username = {0}, nome= {1}, cognome = {2}, email = {3})>".format(self.user.username, self.user.nome, self.user.cognome, self.user.email)


class AbbonamentoT(enum.Enum):
    one = "sala_pesi"
    two = "corsi"
    three = "completo"
    four = "prova"
#insert: (t.insert(), {"value": MyEnum.two})
#sqlalchemy.exc.ArgumentError: 'SchemaItem' object, such as a 'Column' or a 'Constraint' expected, got <enum 'AbbonamentoT'>

class Subscription(db.Model):
    __tablename__ = 'abbonamenti'
    __table_args__ = (
        CheckConstraint('"costo" > 0'),
    )

    id = Column(Integer, primary_key=True) #aggiunta provvisoria id
    tipo = Column(Enum(AbbonamentoT))
    costo = Column(REAL)

    def __init__(self, id, tipo, costo):
        self.id = id
        self.tipo = tipo
        self.costo = costo

    def __repr__(self):
        return "<Subscription(type = {0}, costo = {1})>".format(self.tipo, self.costo)


class Subscriber(UserMixin):
    __tablename__ = 'abbonati'
    __table_args__ = (
        CheckConstraint('"dataFineAbbonamento" > "dataInizioAbbonamento"'),
    )

    id = Column(Integer, ForeignKey(Client.id, ondelete='cascade'), primary_key=True)
    #abbonamento = Column(AbbonamentoT, ForeignKey(Subscription.tipo), nullable=False)
    abbonamento = Column(Integer, ForeignKey(Subscription.id), nullable=False)
    dataInizioAbbonamento = Column(Date)
    dataFineAbbonamento = Column(Date)
    client = relationship(Client, uselist=False)
    abbonato = relationship(Subscription, uselist=False)

    def __init__(self, id, abbonamento, dataInizioAbbonamento, dataFineAbbonamento):
        self.id = id
        self.abbonamento = abbonamento
        self.dataInizioAbbonamento = dataInizioAbbonamento
        self.dataFineAbbonamento = dataFineAbbonamento

    def __repr__(self):
        return "<Subscriber(username = {0}, nome= {1}, cognome = {2}, email = {3})>".format(self.user.username, self.user.nome, self.user.cognome, self.user.email)


class NotSubscriber(UserMixin):
    __tablename__ = 'nonabbonati'

    id = Column(Integer, ForeignKey(Client.id, ondelete='cascade'), primary_key=True)
    client = relationship(Client, uselist=False)

    def __init__(self, id):
        self.id = id
    
    def __repr__(self):
        return "<NotSubscriber(username = {0}, nome= {1}, cognome = {2}, email = {3})>".format(self.user.username, self.user.nome, self.user.cognome, self.user.email)


class Room(db.Model):
    __tablename__ = 'stanze'
    __table_args__ = (
        CheckConstraint('"dimensione" > 0'),
    )

    id = Column(Integer, primary_key=True)
    dimensione = Column(Integer)

    #primary key progressiva
    def __init__(self, id, dimensione):
        self.id = id
        self.dimensione = dimensione

    def __repr__(self):
        return "<Room(id = {0}, dimensione = {1})>".format(self.id, self.dimensione)


class WeightRoom(db.Model):
    __tablename__ = 'salepesi'
    __table_args__ = (
        CheckConstraint('"dimensione" > 0'),
    )

    id = Column(Integer, primary_key=True)
    dimensione = Column(Integer)

    def __init__(self, id, dimensione):
        self.id = id
        self.dimensione = dimensione

    def __repr__(self):
        return "<WeightRoom(id = {0}, dimensione = {1})>".format(self.id, self.dimensione)


class Course(db.Model):
    __tablename__ = 'corsi'
    __table_args__ = (
        CheckConstraint('"iscrittiMax" > 0'),
    )

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    iscrittiMax = Column(Integer)
    istruttore = Column(Integer, ForeignKey(Trainer.id), nullable=False)
    stanza = Column(Integer, ForeignKey(Room.id, ondelete='cascade'), nullable=False)
    trainer = relationship(Trainer, uselist=False)
    room = relationship(Room, uselist=False)

    #primary key progressiva
    def __init__(self, id, nome, iscrittiMax, istruttore, stanza):
        self.id = id
        self.nome = nome
        self.iscrittiMax = iscrittiMax
        self.istruttore = istruttore
        self.stanza = stanza

    def __repr__(self):
        return "<Course(id = {0}, nome = {1}, iscrittiMax = {2}, istruttore = {3}, stanza = {4})>".format(self.id, self.nome, self.iscrittiMax, self.istruttore, self.stanza)


class Session(db.Model):
    __tablename__ = 'sedute'

    id = Column(Integer, primary_key=True)
    corso = Column(Integer, ForeignKey(Course.id, ondelete='cascade'), nullable=False)
    dataSeduta = Column(DateTime)
    course = relationship(Course, uselist=False)

    #primary key progressiva
    def __init__(self, id,  corso, dataSeduta):
        self.id = id
        self.corso = corso
        self.dataSeduta = dataSeduta
        
    def __repr__(self):
        return "<Session(id = {0}, corso = {1}, dataSeduta = {2})>".format(self.id, self.corso, self.dataSeduta)


class SubscriberSession(db.Model):
    __tablename__ = 'abbonatisedute'

    abbonato = Column(Integer, ForeignKey(Subscriber.id, ondelete='cascade'), primary_key=True)
    seduta = Column(Integer, ForeignKey(Session.id, ondelete='cascade'), primary_key=True)
    subscriber = relationship(Subscriber, uselist=False)
    session = relationship(Session, uselist=False)

    def __init__(self, abbonato, seduta):
        self.abbonato = abbonato
        self.seduta = seduta

    def __repr__(self):
        return "<SubScriberSession(abbonato = {0}, seduta = {1})>".format(self.abbonato, self.seduta)


class Day(db.Model):
    __tablename__ = 'giorni'

    data = Column(Date, primary_key=True)
    
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return "<Day(data = {0})>".format(self.data)


class Slot(db.Model):
    __tablename__ = 'slot'
    __table_args__ = (
        CheckConstraint('"oraFine"> "oraInizio"'),
    )

    id = Column(Integer, primary_key=True)
    personeMax = Column(Integer)
    giorno = Column(Date, ForeignKey(Day.data, ondelete='cascade'), nullable=False)
    oraInizio = Column(DateTime)
    oraFine = Column(DateTime)
    date = relationship(Day, uselist=False)

    def __init__(self, id, personeMax, giorno, oraInizio, oraFine):
        self.id = id
        self.personeMax = personeMax
        self.giorno = giorno
        self.oraInizio = oraInizio
        self.oraFine = oraFine

    def __repr__(self):
        return "<Slot(id = {0}, personeMax = {1}, giorno = {2}, oraInizio = {3}, oraFine = {4})>".format(self.id, self.personeMax, self.giorno, self.oraInizio, self.oraFine)


class CourseSlot(db.Model):
    __tablename__ = 'corsislot'

    corso = Column(Integer, ForeignKey(Course.id, ondelete='cascade'), primary_key=True)
    slot = Column(Integer, ForeignKey(Slot.id, ondelete='cascade'), primary_key=True)
    course = relationship(Course, uselist=False)
    courseslot = relationship(Slot, uselist=False)
    
    def __init__(self, corso, slot):
        self.corso = corso 
        self.slot = slot
    
    def __repr__(self):
        return "<CourseSlot(corso = {0}, slot = {1})>".format(self.corso, self.slot)


class WeightRoomSlot(db.Model):
    __tablename__ = 'salepesislot'

    salaPesi = Column(Integer, ForeignKey(WeightRoom.id, ondelete='cascade'), primary_key=True)
    slot = Column(Integer, ForeignKey(Slot.id, ondelete='cascade'), primary_key=True)
    weightroom= relationship(WeightRoom, uselist=False)
    weightroomslot = relationship(Slot, uselist=False)

    def __init__(self, salaPesi, slot):
        self.salaPesi = salaPesi
        self.slot = slot

    def __repr__(self):
        return "<WeightRoomSlot(sala = {0}, slot = {1})>".format(self.salaPesi, self.slot)


class Reservation(db.Model):
    __tablename__ = 'prenotazioni'

    abbonato = Column(Integer, ForeignKey(Subscriber.id, ondelete='cascade'), primary_key=True)
    slot = Column(Integer, ForeignKey(Slot.id, ondelete='cascade'), primary_key=True)
    subscriber = relationship(Subscriber, uselist=False)
    reservationslot = relationship(Slot, uselist=False)

    def __init__(self, abbonato, slot):
        self.abbonato = abbonato
        self.slot = slot

    def __repr__(self):
        return "<Reservation(abbonato = {0}, slot = {1})>".format(self.abbonato, self.slot)


#Functions
def get_user_by_email(email):
    conn = engine.connect()
    p_query = "SELECT * FROM utenti WHERE email = %s"
    user = conn.engine.execute(p_query, email).first()
    conn.close()
    return User(user.id, user.username, user.password, user.nome, user.cognome, user.email, user.dataNascita)

#user_loader
'''
@login_manager.user_loader # attenzione a questo!
def load_user(user_id):
    conn = engine.connect()
    rs = conn.execute('SELECT * FROM utenti WHERE id = ?', user_id)
    user = rs.fetchone()
    conn.close()
    return User(user.id, user.username, user.password, user.nome, user.cognome, user.email, user.dataNascita)
'''
'''
@login_manager.user_loader
def load_user(user_id):
    conn = engine.connect()
    p_query = "SELECT * FROM utenti WHERE id = %s"
    user = conn.engine.execute(p_query, user_id).first()
    conn.close()
    return User(user.id, user.username, user.password, user.nome, user.cognome, user.email, user.dataNascita)
'''

@login_manager.user_loader
def load_user(user_id):
    conn = engine.connect()
    rs = conn.execute('SELECT * FROM utenti WHERE id = %s' % user_id)
    user = rs.fetchone()
    conn.close()
    return User(user.id, user.username, user.password, user.nome, user.cognome, user.email, user.dataNascita)

#self, username, password, nome, cognome, email, dataNascita):
#Routes
@app.route('/')
def home():
    if current_user.is_authenticated:
        return render_template("private.html")
    return render_template("base.html")

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
        conn.close()

        if(real_pwd is not None):
            #if request.form['pass'] == real_pwd['password']:
            print(p_pass)
            print(" -> ")
            print(real_pwd['password'])
            if p_pass == real_pwd['password']:
                user = get_user_by_email(request.form['user'])
                print("id")
                print(user.id)
                print("username: " + user.username)
                print("password: " + user.password)
                login_user(user) # chiamata a Flask - Login
                return redirect(url_for('private'))
            else:
                sys.stdout.write("ciao mamma")
                return redirect(url_for('home'))
        else:
            sys.stdout.write("ciao papa")
            return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))

@app.route('/private')
@login_required
def private():
    resp = make_response(render_template("private.html", current_user = current_user))
    return resp

@app.route('/create', methods =['GET', 'POST'])
def create_user():
    user = User(request.form['id'] ,request.form['username'], request.form['password'], request.form['nome'], request.form['cognome'], request.form['email'], request.form['dataNascita'])
    session.add(user)
    session.commit()
    return render_template("conferma.html")

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('home'))