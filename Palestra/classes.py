#flask-import
from flask_login import UserMixin

#sqlalchemy-import
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# Dichiarazione Classi-Tabelle
class User(Base, UserMixin):
    __tablename__ = 'utenti'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    password = Column(String)
    nome = Column(String)
    cognome = Column(String)
    email = Column(String)
    datanascita = Column(Date)

    # primary key progressiva
    def __init__(self, id, username, password, nome, cognome, email, datanascita):
        self.id = id
        self.username = username
        self.password = password
        self.nome = nome
        self.cognome = cognome
        self.email = email
        self.datanascita = datanascita

    def __repr__(self):
        return "<User(id = {0}, username = {1}, nome= {2}, cognome = {3}, email = {4})>".format(self.id, self.username, self.nome, self.cognome, self.email)


class Trainer(Base):
    __tablename__ = 'istruttori'

    id = Column(Integer, ForeignKey(User.id, ondelete='cascade'), primary_key=True)
    user = relationship(User, uselist=False)

    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return "<Trainer(username = {0}, nome= {1}, cognome = {2}, email = {3})>".format(self.user.username, self.user.nome, self.user.cognome, self.user.email)


class Other(Base):
    __tablename__ = 'altri'

    id = Column(Integer, ForeignKey(User.id, ondelete='cascade'), primary_key=True)
    user = relationship(User, uselist=False)

    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return "<Other(username = {0}, nome= {1}, cognome = {2}, email = {3})>".format(self.user.username, self.user.nome, self.user.cognome, self.user.email)


class Client(Base):
    __tablename__ = 'clienti'

    id = Column(Integer, ForeignKey(User.id, ondelete='cascade'), primary_key=True)
    user = relationship(User, uselist=False)

    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return "<Client(id = {0})>".format(self.id)


class Subscription(Base):
    __tablename__ = 'abbonamenti'
    __table_args__ = (
        CheckConstraint('"costo" > 0'),
    )

    id = Column(Integer, primary_key=True)  # aggiunta provvisoria id
    tipo = Column(String)
    costo = Column(REAL)

    def __init__(self, id, tipo, costo):
        self.id = id
        self.tipo = tipo
        self.costo = costo

    def __repr__(self):
        return "<Subscription(type = {0}, costo = {1})>".format(self.tipo, self.costo)


class Subscriber(Base):
    __tablename__ = 'abbonati'
    __table_args__ = (
        CheckConstraint('"dataFineAbbonamento" > "dataInizioAbbonamento"'),
    )

    id = Column(Integer, ForeignKey(Client.id, ondelete='cascade'), primary_key=True)
    # abbonamento = Column(AbbonamentoT, ForeignKey(Subscription.tipo), nullable=False)
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


class NotSubscriber(Base):
    __tablename__ = 'nonabbonati'

    id = Column(Integer, ForeignKey(Client.id, ondelete='cascade'), primary_key=True)
    client = relationship(Client, uselist=False)

    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return "<NotSubscriber(username = {0}, nome= {1}, cognome = {2}, email = {3})>".format(self.user.username, self.user.nome, self.user.cognome, self.user.email)


class Room(Base):
    __tablename__ = 'stanze'
    __table_args__ = (
        CheckConstraint('"dimensione" > 0'),
    )

    id = Column(Integer, primary_key=True)
    dimensione = Column(Integer)

    # primary key progressiva
    def __init__(self, id, dimensione):
        self.id = id
        self.dimensione = dimensione

    def __repr__(self):
        return "<Room(id = {0}, dimensione = {1})>".format(self.id, self.dimensione)


class WeightRoom(Base):
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


class Course(Base):
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

    # primary key progressiva
    def __init__(self, id, nome, iscrittiMax, istruttore, stanza):
        self.id = id
        self.nome = nome
        self.iscrittiMax = iscrittiMax
        self.istruttore = istruttore
        self.stanza = stanza

    def __repr__(self):
        return "<Course(id = {0}, nome = {1}, iscrittiMax = {2}, istruttore = {3}, stanza = {4})>".format(self.id, self.nome, self.iscrittiMax, self.istruttore, self.stanza)


class Sitting(Base):
    __tablename__ = 'sedute'

    id = Column(Integer, primary_key=True)
    corso = Column(Integer, ForeignKey(Course.id, ondelete='cascade'), nullable=False)
    dataSeduta = Column(DateTime)
    course = relationship(Course, uselist=False)

    # primary key progressiva
    def __init__(self, id, corso, dataSeduta):
        self.id = id
        self.corso = corso
        self.dataSeduta = dataSeduta

    def __repr__(self):
        return "<Session(id = {0}, corso = {1}, dataSeduta = {2})>".format(self.id, self.corso, self.dataSeduta)


class SubscriberSession(Base):
    __tablename__ = 'abbonatisedute'

    abbonato = Column(Integer, ForeignKey(Subscriber.id, ondelete='cascade'), primary_key=True)
    seduta = Column(Integer, ForeignKey(Sitting.id, ondelete='cascade'), primary_key=True)
    subscriber = relationship(Subscriber, uselist=False)
    sitting = relationship(Sitting, uselist=False)

    def __init__(self, abbonato, seduta):
        self.abbonato = abbonato
        self.seduta = seduta

    def __repr__(self):
        return "<SubScriberSession(abbonato = {0}, seduta = {1})>".format(self.abbonato, self.seduta)


class Day(Base):
    __tablename__ = 'giorni'

    data = Column(Date, primary_key=True)

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return "<Day(data = {0})>".format(self.data)


class Slot(Base):
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


class CourseSlot(Base):
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


class WeightRoomSlot(Base):
    __tablename__ = 'salepesislot'

    salaPesi = Column(Integer, ForeignKey(WeightRoom.id, ondelete='cascade'), primary_key=True)
    slot = Column(Integer, ForeignKey(Slot.id, ondelete='cascade'), primary_key=True)
    weightroom = relationship(WeightRoom, uselist=False)
    weightroomslot = relationship(Slot, uselist=False)

    def __init__(self, salaPesi, slot):
        self.salaPesi = salaPesi
        self.slot = slot

    def __repr__(self):
        return "<WeightRoomSlot(sala = {0}, slot = {1})>".format(self.salaPesi, self.slot)


class Reservation(Base):
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