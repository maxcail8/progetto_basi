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

class User(db.Model):
    __tablename__ = 'utenti'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    nome = Column(String)
    cognome = Column(String)
    email = Column(String)
    dataNascita = Column(Date)

    #primary key progressiva
    def __init__(self, username, password, nome, cognome, email, dataNascita):
        self.username = username
        self.password = password
        self.nome = nome
        self.cognome = cognome
        self.email = email
        self.dataNascita = dataNascita

    def __repr__(self):
        return "<User(username = {0}, nome= {1}, cognome = {2}, email = {3})>".format(self.username, self.nome, self.cognome, self.email)

class Trainer(db.Model):
    __tablename__ = 'istruttori'

    id = Column(Integer, ForeignKey(User.id, ondelete='cascade'), primary_key=True)
    user = relationship(User, uselist=False)

    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return "<Trainer(username = {0}, nome= {1}, cognome = {2}, email = {3})>".format(self.user.username, self.user.nome, self.user.cognome, self.user.email)


class Other(db.Model):
    __tablename__ = 'altri'

    id = Column(Integer, ForeignKey(User.id, ondelete='cascade'), primary_key=True)
    user = relationship(User, uselist=False)

    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return "<Other(username = {0}, nome= {1}, cognome = {2}, email = {3})>".format(self.user.username, self.user.nome, self.user.cognome, self.user.email)


class Client(db.Model):
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

    def __init__(self, tipo, costo):
        self.tipo = tipo
        self.costo = costo

    def __repr__(self):
        return "<Subscription(type = {0}, costo = {1})>".format(self.tipo, self.costo)


class Subscriber(db.Model):
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


class NotSubscriber(db.Model):
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
    def __init__(self, dimensione):
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
    def __init__(self, nome, iscrittiMax, istruttore, stanza):
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
    def __init__(self, corso, dataSeduta):
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

    def __init__(self, personeMax, giorno, oraInizio, oraFine):
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
    #rs = session.query(User).filter_by(email=request.form['user'])
    rs = session.query(User).filter_by(email=request.form.get('user'))
    user = rs.one()
    return User(user.username, user.password, user.nome, user.cognome, user.email, user.dataNascita)

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
        conn = engine.connect()
        #rs = conn.execute('SELECT password FROM utenti WHERE email = ?', [request.form['user']])
        rs = conn.execute('SELECT password FROM utenti WHERE email = ?', request.form.get('user'))
        #rs = session.query(User.password).filter_by(email=[request.form['user']])
        #rs = session.query(User.password).filter_by(email=request.form.get('user'))
        real_pwd = rs.fetchone()
        conn.close()

        if(real_pwd is not None):
            #if request.form['pass'] == real_pwd['utenti_password']:
            if request.form.get('pass') == real_pwd['password']:
                user = get_user_by_email(request.form.get('user'))
                login_user(user) # chiamata a Flask - Login
                return redirect(url_for('private'))
            else:
                return redirect(url_for('home'))
        else:
            return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))
    '''    
    if request.method == 'POST':
        p_email = request.form['user']
        p_password = request.form['password']
        rs = session.query(User.password).filter_by(email=p_email)
        #conn = engine.connect()
        #rs = conn.execute('SELECT pwd FROM Users WHERE email = ?', [request.form['user']])
        real_pwd = rs.one()
        #conn.close()

        if(real_pwd is not None):
            if p_password == real_pwd['password']:
                user = get_user_by_email(p_email)
                login_user(user) # chiamata a Flask - Login
                return redirect(url_for('private'))
            else:
                return redirect(url_for('home'))
        else:
            return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))
    '''

@app.route('/private')
@login_required
def private():
    resp = make_response(render_template("private.html", current_user = current_user))
    return resp

@login_manager.user_loader
def load_user(user_id):
    rs = session.query(User.id, User.email, User.password).filter(User.id == user_id)
    user = rs.one()
    return User(user.id, user.email, user.password)

@app.route('/create', methods =['GET', 'POST'])
def create_user():
    user = User(request.form['username'], request.form['password'], request.form['nome'], request.form['cognome'], request.form['email'], request.form['dataNascita'])
    session.add(user)
    session.commit()
    return render_template("conferma.html")

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('index'))



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