# flask-import
from flask_login import UserMixin

# sqlalchemy-import
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

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
        CheckConstraint('"datafineabbonamento" > "datainizioabbonamento"'),
        CheckConstraint('"durata" > 0'),
    )

    id = Column(Integer, ForeignKey(Client.id, ondelete='cascade'), primary_key=True)
    # abbonamento = Column(AbbonamentoT, ForeignKey(Subscription.tipo), nullable=False)
    abbonamento = Column(Integer, ForeignKey(Subscription.id), nullable=False)
    datainizioabbonamento = Column(Date)
    datafineabbonamento = Column(Date)
    durata = Column(Integer)
    client = relationship(Client, uselist=False)
    abbonato = relationship(Subscription, uselist=False)

    def __init__(self, id, abbonamento, datainizioabbonamento, datafineabbonamento, durata):
        self.id = id
        self.abbonamento = abbonamento
        self.datainizioabbonamento = datainizioabbonamento
        self.datafineabbonamento = datafineabbonamento
        self.durata = durata

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
        CheckConstraint('"iscrittimax" > 0'),
    )

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    iscrittimax = Column(Integer)
    istruttore = Column(Integer, ForeignKey(Trainer.id), nullable=False)
    stanza = Column(Integer, ForeignKey(Room.id, ondelete='cascade'), nullable=False)
    trainer = relationship(Trainer, uselist=False)
    room = relationship(Room, uselist=False)

    # primary key progressiva
    def __init__(self, id, nome, iscrittimax, istruttore, stanza):
        self.id = id
        self.nome = nome
        self.iscrittimax = iscrittimax
        self.istruttore = istruttore
        self.stanza = stanza

    def __repr__(self):
        return "<Course(id = {0}, nome = {1}, iscrittimax = {2}, istruttore = {3}, stanza = {4})>".format(self.id, self.nome, self.iscrittimax, self.istruttore, self.stanza)


class Sitting(Base):
    __tablename__ = 'sedute'

    id = Column(Integer, primary_key=True)
    corso = Column(Integer, ForeignKey(Course.id, ondelete='cascade'), nullable=False)
    dataseduta = Column(DateTime)
    course = relationship(Course, uselist=False)

    # primary key progressiva
    def __init__(self, id, corso, dataseduta):
        self.id = id
        self.corso = corso
        self.dataseduta = dataseduta

    def __repr__(self):
        return "<Session(id = {0}, corso = {1}, dataseduta = {2})>".format(self.id, self.corso, self.dataseduta)


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
        CheckConstraint('"orafine"> "orainizio"'),
    )

    id = Column(Integer, primary_key=True)
    personemax = Column(Integer)
    giorno = Column(Date, ForeignKey(Day.data, ondelete='cascade'), nullable=False)
    orainizio = Column(DateTime)
    orafine = Column(DateTime)
    date = relationship(Day, uselist=False)

    def __init__(self, id, personemax, giorno, orainizio, orafine):
        self.id = id
        self.personemax = personemax
        self.giorno = giorno
        self.orainizio = orainizio
        self.orafine = orafine

    def __repr__(self):
        return "<Slot(id = {0}, personemax = {1}, giorno = {2}, orainizio = {3}, orafine = {4})>".format(self.id, self.personemax, self.giorno, self.orainizio, self.orafine)


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


class My2Date:
    first_column = []
    second_column = []
    third_column = []
    fourth_column = []
    last_column = []

    def __init__(self):
        i = datetime.now()
        first = datetime(i.year, i.month, 1)
        last = datetime(i.year, i.month, i.day) + relativedelta(day=31)  # torna l'utlimo giorno del mese
        days = 0

        first_column_days = 7 - first.weekday()
        for i in range(7 - first_column_days):
            self.first_column.append(0)
        for i in range(first_column_days):
            self.first_column.append(i+1)

        second_column_day = first_column_days + 1
        for i in range(second_column_day, second_column_day + 7):
            self.second_column.append(i)

        third_column_day = second_column_day + 7
        for i in range(third_column_day, third_column_day + 7):
            self.third_column.append(i)

        fourth_column_day = third_column_day + 7
        for i in range(fourth_column_day, fourth_column_day + 7):
            self.fourth_column.append(i)

        last_column_day = fourth_column_day + 7
        days += first_column_days + 21
        last_column_days = last.day - days
        end_days = 7 - last_column_days
        for i in range(last_column_day, last_column_day + last_column_days):
            self.last_column.append(i)
        for i in range(end_days):
            self.last_column.append(0)


class MyDate():
    first_column = Integer
    last_day = Integer

    def __init__(self):
        i = datetime.now()
        first = datetime(i.year, i.month, 1)
        last = datetime(i.year, i.month, i.day) + relativedelta(day=31)  # torna l'utlimo giorno del mese
        first_column_days = 7 - first.weekday()
        self.first_column = 7 - first_column_days
        self.last_day = last.day