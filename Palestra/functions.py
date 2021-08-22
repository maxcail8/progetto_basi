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
    subscriber = session.query(Subscriber).filter(Subscriber.id == id).first()
    '''conn = engine.connect()
    p_query = "SELECT * FROM abbonati WHERE id = %s"
    subscriber = conn.engine.execute(p_query, id).first()
    conn.close()'''
    return classes.Subscriber(subscriber.id, subscriber.abbonamento, subscriber.datafineabbonamento, subscriber.datafineabbonamento, subscriber.durata)


def get_user_by_email(email):
    user = session.query(User).filter(User.email == email).first()
    '''conn = engine.connect()
    p_query = "SELECT * FROM utenti WHERE email = %s"
    user = conn.engine.execute(p_query, email).first()
    conn.close()'''
    return classes.User(user.id, user.username, user.password, user.nome, user.cognome, user.email, user.datanascita)


# Funzione per autoincrementare id tramite query
def get_id_increment():
    user = session.query(User).order_by(User.id.desc()).first()
    '''conn = engine.connect()
    p_query = "SELECT * FROM utenti WHERE id>=100 ORDER BY id DESC"
    user = conn.engine.execute(p_query).first()
    conn.close()'''
    if user:
        return user.id + 1
    else:
        return first_id_client


def get_course_id_increment():
    course = session.query(Course).order_by(Course.id.desc()).first()
    '''conn = engine.connect()
    p_query = "SELECT * FROM corsi ORDER BY id DESC"
    course = conn.engine.execute(p_query).first()
    conn.close()'''
    if course:
        return course.id + 1
    else:
        return 0


def get_room_id_increment():
    room = session.query(Room).order_by(Room.id.desc()).first()
    '''conn = engine.connect()
    p_query = "SELECT * FROM stanze ORDER BY id DESC"
    room = conn.engine.execute(p_query).first()
    conn.close()'''
    if room:
        return room.id + 1
    else:
        return 0


def get_weight_room_id_increment():
    weight_room = session.query(WeightRoom).order_by(WeightRoom.id.desc()).first()
    '''conn = engine.connect()
    p_query = "SELECT * FROM salepesi ORDER BY id DESC"
    weight_room = conn.engine.execute(p_query).first()
    conn.close()'''
    if weight_room:
        return weight_room.id + 1
    else:
        return 0


# Funzione per tornare l'utente amministratore
def get_admin_user():
    user = session.query(User).filter(User.id == 0).first()
    '''conn = engine.connect()
    p_query = "SELECT * FROM utenti WHERE id = 0"
    user = conn.engine.execute(p_query).first()
    conn.close()'''
    return classes.User(user.id, user.username, user.password, user.nome, user.cognome, user.email, user.datanascita)


def get_current_date():
    now = datetime.now()
    return now.strftime("%Y-%m-%d")


def get_increment_date(giorni):
    data = datetime.now() + timedelta(days=giorni)
    return data.strftime("%Y-%m-%d")


def get_subscription(subscription):
    sub = session.query(Subscription).filter(Subscription.tipo == subscription).first()
    '''conn = engine.connect()
    p_query = "SELECT * FROM abbonamenti WHERE tipo = %s"
    sub = conn.engine.execute(p_query, subscription).first()
    conn.close()'''
    return classes.Subscription(sub.id, sub.tipo, sub.costo)


def get_subscription_by_id(id):
    sub = session.query(Subscription).filter(Subscription.id == id).first()
    '''conn = engine.connect()
    p_query = "SELECT * FROM abbonamenti WHERE id = %s"
    sub = conn.engine.execute(p_query, id).first()
    conn.close()'''
    return classes.Subscription(sub.id, sub.tipo, sub.costo)


def get_courses():
    courses = session.query(Course).order_by(Course.id.asc()).all()
    '''conn = engine.connect()
    p_query = "SELECT * FROM corsi ORDER BY id ASC"
    courses = conn.engine.execute(p_query)
    conn.close()'''
    return courses


def get_course(idCorso):
    course = session.query(Course).filter(Course.id == idCorso).first()
    '''conn = engine.connect()
    p_query = "SELECT * FROM corsi WHERE id = %s"
    course = conn.engine.execute(p_query, idCorso).first()
    conn.close()'''
    return classes.Course(course.id, course.nome, course.iscrittimax, course.istruttore, course.stanza)


def get_last_id_course():
    course = session.query(Course).order_by(Course.id.desc()).first()
    '''conn = engine.connect()
    p_query = "SELECT * FROM corsi ORDER BY id DESC"
    course = conn.engine.execute(p_query).first()
    conn.close()'''
    return course.id


def get_rooms():
    rooms = session.query(Room).order_by(Room.id.asc()).all()
    '''conn = engine.connect()
    p_query = "SELECT * FROM stanze ORDER BY id ASC"
    rooms = conn.engine.execute(p_query)
    conn.close()'''
    return rooms


def get_weight_rooms():
    weight_rooms = session.query(WeightRoom).order_by(WeightRoom.id.asc()).all()
    '''conn = engine.connect()
    p_query = "SELECT * FROM salepesi ORDER BY id ASC"
    weight_rooms = conn.engine.execute(p_query)
    conn.close()'''
    return weight_rooms


def get_trainers():
    trainers = session.query(Trainer, User).filter(Trainer.id == User.id).order_by(Trainer.id.asc()).all()
    '''conn = engine.connect()
    p_query = "SELECT * FROM istruttori NATURAL JOIN utenti ORDER BY id ASC"
    trainers = conn.engine.execute(p_query)
    conn.close()'''
    return trainers


def get_clients():
    clients = session.query(Client, User).filter(Client.id == User.id).order_by(Client.id.asc()).all()
    '''conn = engine.connect()
    p_query = "SELECT * FROM clienti NATURAL JOIN utenti ORDER BY id ASC"
    clients = conn.engine.execute(p_query)
    conn.close()'''
    return clients


def get_information():
    info = session.query(Information).first()
    '''conn = engine.connect()
    p_query = "SELECT * FROM informazioni"
    info = conn.engine.execute(p_query).first()
    conn.close()'''
    return classes.Information(info.accessisettimana, info.slotgiorno, info.personemaxslot, info.personemq)


def get_checks():
    checks = session.query(Checks).first()
    '''conn = engine.connect()
    p_query = "SELECT * FROM controlli"
    checks = conn.engine.execute(p_query).first()
    conn.close()'''
    return classes.Checks(checks.controllo)


def get_slot_from_date(data):
    slots = session.query(Slot).format(Slot.giorno == data).all()
    '''conn = engine.connect()
    p_query = "SELECT * FROM slot WHERE giorno = DATE %s"
    slots = conn.engine.execute(p_query, data)
    conn.close()'''
    return slots


def get_slot_weight_rooms(idSlot, subscription):
    if subscription=='corsi':
        return None
    else:
        salepesi = session.query(WeightRoomSlot.salapesi).filter(WeightRoomSlot.slot == idSlot).all()
        weightrooms = session.query(Courses).filter(in_(Courses.id, salepesi)).all()
        '''conn = engine.connect()
        p_query = "SELECT * FROM salepesi WHERE id IN (SELECT salapesi FROM salapesislot WHERE slot= %s)"
        weightrooms = conn.engine.execute(p_query, idSlot)
        conn.close()'''
        return weightrooms


def get_slot_courses(idSlot, subscription):
    if subscription=='sala_pesi':
        return None
    else:
        corsi = session.query(CourseSlot.corso).filter(CourseSlot.slot == idSlot).all()
        courses = session.query(Courses).filter(in_(Courses.id, corsi)).all()
        '''conn = engine.connect()
        p_query = "SELECT * FROM corsi WHERE id IN (SELECT corso FROM corsislot WHERE slot= %s)"
        courses = conn.engine.execute(p_query, idSlot)
        conn.close()'''
        return courses


def get_coursesitting_id(idSlot, idCorso):
    giorno = session.query(Slot.giorno).filter(Slot.giorno == idSlot).first()
    id_sitting = session.query(CourseSitting.id).filter(and_(func.DATE(CourseSitting.dataseduta) == giorno, CourseSitting.corso == idCorso)).first()
    '''conn = engine.connect()
    p_query = "SELECT id FROM sedutecorsi WHERE (dataseduta::date)=(SELECT giorno FROM slot WHERE id = %s) AND corso = %s"
    id_sitting = conn.engine.execute(p_query, idSlot, idCorso).first()
    conn.close()'''
    return id_sitting


def get_weightroomsitting_id(idSlot, idSala):
    giorno = session.query(Slot.giorno).filter(Slot.giorno == idSlot).first()
    id_sitting = session.query(WeightRoomSitting.id).filter(and_(func.DATE(WeightRoomSitting.dataseduta) == giorno, WeightRoomSitting.salapesi == idSala)).first()
    '''conn = engine.connect()
    p_query = "SELECT id FROM sedutesalepesi WHERE (dataseduta::date)=(SELECT giorno FROM slot WHERE id = %s) AND salapesi = %s"
    id_sitting = conn.engine.execute(p_query, idSlot, idSala).first()
    conn.close()'''
    return id_sitting


def get_reservations(idSub):
    reservations = session.query(Reservation, Slot).filter(and_(Reservation.slot == Slot.id, Reservation.abbonato == idSub, Slot.giorno > date.today())).all()
    '''conn = engine.connect()
    p_query = "SELECT * FROM prenotazioni p JOIN slot s ON p.slot=s.id WHERE p.abbonato = %s AND s.giorno > CURRENT_DATE"
    reservations = conn.engine.execute(p_query, idSub)
    conn.close()'''
    return reservations


# BOOLEANS
def is_subscriber(user_id):
    p_query = session.query(Subscriber).filter(Subscriber.id == user_id).first()
    '''conn = engine.connect()
    p_query = "SELECT * FROM abbonati WHERE id = %s"
    sub = conn.engine.execute(p_query, user_id).first()
    conn.close()'''
    if p_query:
        return True
    else:
        return False


def is_reserved(user_id, idSlot):
    res = session.query(Reservation).filter(and_(Reservation.abbonato == user_id, Reservation.slot == idSlot)).first()
    '''conn = engine.connect()
    p_query = "SELECT * FROM prenotazioni WHERE abbonato = %s AND slot = %s"
    res = conn.engine.execute(p_query, user_id, idSlot).first()
    conn.close()'''
    if res:
        return True
    else:
        return False


def is_available_slot(idSlot):
    res = session.query(func.count(Reservation.abbonato)).filter(Reservation.slot == idSlot).first()
    personemax = session.query(Slot.personemax).filter(Slot.id == idSlot).first()
    '''conn = engine.connect()
    p_query1 = "SELECT COUNT(abbonato) FROM prenotazioni WHERE slot = %s"
    res = conn.engine.execute(p_query1, idSlot).first()
    p_query2 = "SELECT personemax FROM slot WHERE id = %s"
    personemax = conn.engine.execute(p_query2, idSlot).first()
    conn.close()'''
    if res < personemax:
        return True
    else:
        return False


def is_available_course(idSeduta, idSlot):
    res = session.query(func.count(SubscriberCourseSession)).filter(SubscriberCourseSession.seduta == idSeduta).first()
    corso = session.query(CourseSitting.corso).filter(CourseSitting.id == idSeduta).first()
    iscrittimax_corso = session.query(Course.iscrittimax).filter(Course.id == corso).first()
    iscrittimax_corsislot = session.query(CourseSlot.iscrittimax).filter(and_(CourseSlot.corso == corso, slot == idSlot)).first()
    '''conn = engine.connect()
    p_query = "SELECT COUNT(*) FROM abbonatisedutecorsi WHERE seduta = %s"
    res = conn.engine.execute(p_query, idSeduta).first()
    p_query2 = "SELECT iscrittimax FROM corsi WHERE id = (SELECT corso FROM sedutecorsi WHERE id = %s)"
    iscrittimax_corso = conn.engine.execute(p_query2, idSeduta).first()
    p_query3 = "SELECT iscrittimax FROM corsislot WHERE corso = (SELECT corso FROM sedutecorsi WHERE id = %s) AND slot = %s"
    iscrittimax_corsislot = conn.engine.execute(p_query3, idSeduta, idSlot).first()
    conn.close()'''
    if res < iscrittimax_corso and res < iscrittimax_corsislot:
        return True
    else:
        return False


def is_available_weight_room(idSeduta, idSlot):
    res = session.query(func.count(SubscriberWeightRoomSession)).filter(SubscriberWeightRoomSession.seduta == idSeduta).first()
    sala = session.query(WeightRoomSitting.corso).filter(WeightRoomSitting.id == idSeduta).first()
    iscrittimax_sala = session.query(WeightRoom.iscrittimax).filter(WeightRoom.id == sala).first()
    iscrittimax_salapesislot = session.query(WeightRoomSlot.iscrittimax).filter(and_(WeightRoomSlot.corso == sala, slot == idSlot)).first()
    '''conn = engine.connect()
    p_query = "SELECT COUNT(*) FROM abbonatisedutesalepesi WHERE seduta = %s"
    res = conn.engine.execute(p_query, idSeduta).first()
    p_query2 = "SELECT iscrittimax FROM salepesi WHERE id = (SELECT salapesi FROM sedutesalepesi WHERE id = %s)"
    iscrittimax_sala = conn.engine.execute(p_query2, idSeduta).first()
    p_query3 = "SELECT iscrittimax FROM salapesislot WHERE salapesi = (SELECT salapesi FROM sedutesalepesi WHERE id = %s) AND slot = %s"
    iscrittimax_salapesislot = conn.engine.execute(p_query3, idSeduta, idSlot).first()
    conn.close()'''
    if res < iscrittimax_sala and res < iscrittimax_salapesislot:
        return True
    else:
        return False


def has_exceeded_accessisettimana(user_id, giorno):
    res1 = session.query(func.extract('dow', giorno))
    if res1 > 0:
        res2 = session.query(func.count(Slot.giorno.distinct())).filter(
            and_(Reservation.slot == Slot.id, Reservation.abbonato == user_id, Slot.giorno > giorno - res1,
                 Slot.giorno <= giorno + (7 - res1), Slot.giorno != giorno)).first()
    else:
        res2 = session.query(func.count(Slot.giorno.distinct())).filter(
            and_(Reservation.slot == Slot.id, Reservation.abbonato == user_id, Slot.giorno >= giorno - 6,
                 Slot.giorno <= giorno, Slot.giorno != giorno)).first()
    res3 = session.query(Information.accessisettimana).first()

    '''conn = engine.connect()
    p_query1 = "SELECT EXTRACT(DOW FROM DATE %s)"
    res1 = conn.engine.execute(p_query1, giorno).first()
    if int(str(res1)[1:2]) > 0:
        p_query2 = "SELECT COUNT(DISTINCT(s.giorno)) FROM prenotazioni p JOIN slot s ON p.slot=s.id WHERE abbonato = %s AND s.giorno > DATE %s - %s AND s.giorno <= DATE %s + (7 - %s) AND s.giorno <> %s"
        res2 = conn.engine.execute(p_query2, user_id, giorno, int(str(res1)[1:2]), giorno, int(str(res1)[1:2]), giorno).first()
    else:
        p_query2 = "SELECT COUNT(DISTINCT(s.giorno)) FROM prenotazioni p JOIN slot s ON p.slot=s.id WHERE abbonato = %s AND s.giorno >= DATE %s - 6 AND s.giorno <= DATE %s AND s.giorno <> %s"
        res2 = conn.engine.execute(p_query2, user_id, giorno, giorno, giorno).first()
    p_query3 = "SELECT accessisettimana FROM informazioni"
    res3 = conn.engine.execute(p_query3).first()
    conn.close()'''
    if res2 < res3:
        return False
    else:
        return True


def has_exceeded_slotgiorno(user_id, giorno):
    res1 = session.query(func.count(Reservation)).filter(and_(Reservation.slot == Slot.id, Reservation.abbonato == user_id, Slot.giorno == giorno)).first()
    res2 = session.query(Information.slotgiorno).first()
    '''conn = engine.connect()
    p_query1 = "SELECT COUNT(*) FROM prenotazioni p JOIN slot s ON p.slot=s.id WHERE abbonato = %s AND s.giorno = %s"
    res1 = conn.engine.execute(p_query1, user_id, giorno).first()
    p_query2 = "SELECT slotgiorno FROM informazioni"
    res2 = conn.engine.execute(p_query2).first()
    conn.close()'''
    if res1 >= res2:
        return True
    else:
        return False


# UPDATE
def set_checks(controlliGiornalieri):
    session.query(Checks).update({"controllo": controlliGiornalieri})
    '''conn = engine.connect()
    p_query = "UPDATE controlli SET controllo = %s"
    conn.engine.execute(p_query, controlliGiornalieri)
    conn.close()'''


def set_information_accessisettimana(accessiSettimana):
    session.query(Information).update({"accessisettimana": accessiSettimana})
    '''conn = engine.connect()
    p_query = "UPDATE informazioni SET accessisettimana = %s"
    conn.engine.execute(p_query, accessiSettimana)
    conn.close()'''


def set_information_slotgiorno(slotGiorno):
    session.query(Information).update({"slotgiorno": slotGiorno})
    '''conn = engine.connect()
    p_query = "UPDATE informazioni SET slotgiorno = %s"
    conn.engine.execute(p_query, slotGiorno)
    conn.close()'''


def set_information_personemaxslot(personeMax):
    session.query(Information).update({"personemaxslot": personeMax})
    '''conn = engine.connect()
    p_query = "UPDATE informazioni SET personemaxslot = %s"
    conn.engine.execute(p_query, personeMax)
    conn.close()'''


def set_information_personemq(personeMq):
    session.query(Information).update({"personemq": personeMq})
    '''conn = engine.connect()
    p_query = "UPDATE informazioni SET personemq = %s"
    conn.engine.execute(p_query, personeMq)
    conn.close()'''


def update_weight_room(idSala, dimensione):
    pmq = get_information().personemq
    session.query(WeightRoom).filter(WeightRoom.id == idSala).update({"dimensione": dimensione})
    session.query(WeightRoom).filter(WeightRoom.id == idSala).update({"iscrittimax": int(dimensione)/pmq})
    '''conn = engine.connect()
    pmq = get_information().personemq
    p_query = "UPDATE salepesi SET dimensione = %s, iscrittimax = %s WHERE id = %s"
    conn.engine.execute(p_query, dimensione, int(dimensione)/pmq, idSala)
    conn.close()'''


def update_room(idStanza, nome, dimensione):
    session.query(Room).filter(Room.id == idStanza).update({"nome": nome})
    session.query(Room).filter(Room.id == idStanza).update({"nome": dimensione})
    '''conn = engine.connect()
    p_query = "UPDATE stanze SET nome = %s, dimensione = %s WHERE id = %s"
    conn.engine.execute(p_query, nome, dimensione, idStanza)
    conn.close()'''


def update_course(idCorso, nome, iscrittiMax, idIstruttore, idStanza):
    session.query(Course).filter(Course.id == idCorso).update({"nome": nome})
    session.query(Course).filter(Course.id == idCorso).update({"iscrittimax": iscrittiMax})
    session.query(Course).filter(Course.id == idCorso).update({"istruttore": idIstruttore})
    session.query(Course).filter(Course.id == idCorso).update({"stanza": idStanza})
    '''conn = engine.connect()
    p_query = "UPDATE corsi SET nome = %s, iscrittimax = %s, istruttore = %s, stanza = %s WHERE id = %s"
    conn.engine.execute(p_query, nome, iscrittiMax, idIstruttore, idStanza, idCorso)
    conn.close()'''


# REMOVE
def remove_room(idStanza):
    session.query(Room).filter(Room.id == idStanza).delete()
    '''conn = engine.connect()
    p_query = "DELETE FROM stanze WHERE id = %s"
    conn.engine.execute(p_query, idStanza)
    conn.close()'''


def remove_weight_room(idSala):
    session.query(WeightRoom).filter(WeightRoom.id == idSala).delete()
    '''conn = engine.connect()
    p_query = "DELETE FROM salepesi WHERE id = %s"
    conn.engine.execute(p_query, idSala)
    conn.close()'''


def remove_course(idCorso):
    session.query(Course).filter(Course.id == idCorso).delete()
    '''conn = engine.connect()
    p_query = "DELETE FROM corsi WHERE id = %s"
    conn.engine.execute(p_query, idCorso)
    conn.close()'''


def remove_not_subscriber(idCliente):
    session.query(NotSubscriber).filter(NotSubscriber.id == idCliente).delete()
    '''conn = engine.connect()
    p_query = "DELETE FROM nonabbonati WHERE id = %s"
    conn.engine.execute(p_query, idCliente)
    conn.close()'''


def remove_reservation(idSub, idSlot):
    session.query(Reservation).filter(and_(Reservation.abbonato == idSub, Reservation.slot == idSlot)).delete()
    giorno = session.query(Slot.giorno).filter(Slot.id == idSlot)
    orainizio = session.query(Slot.orainizio).filter(Slot.id == idSlot)
    id_sedutecorsi = session.query(CourseSitting.id).filter(CourseSitting.dataseduta == giorno + orainizio)
    id_sedutesalepesi = session.query(WeightRoomSitting.id).filter(WeightRoomSitting.dataseduta == giorno + orainizio)
    session.query(SubscriberCourseSession).filter(and_(SubscriberCourseSession.abbonato == idSub, SubscriberCourseSession.seduta == id_sedutecorsi)).delete()
    session.query(SubscriberWeightRoomSession).filter(and_(SubscriberWeightRoomSession.abbonato == idSub, SubscriberWeightRoomSession.seduta == id_sedutesalepesi)).delete()
    '''conn = engine.connect()
    p_query1 = "DELETE FROM prenotazioni WHERE abbonato = %s AND slot = %s"
    conn.engine.execute(p_query1, idSub, idSlot)
    p_query2 = "DELETE FROM abbonatisedutecorsi WHERE abbonato = %s AND seduta = (SELECT id FROM sedutecorsi WHERE dataseduta = ((SELECT giorno FROM slot WHERE id = %s) + (SELECT orainizio FROM slot WHERE id = %s))::timestamp)"
    conn.engine.execute(p_query2, idSub, idSlot, idSlot)
    p_query3 = "DELETE FROM abbonatisedutesalepesi WHERE abbonato = %s AND seduta = (SELECT id FROM sedutesalepesi WHERE dataseduta = ((SELECT giorno FROM slot WHERE id = %s) + (SELECT orainizio FROM slot WHERE id = %s))::timestamp)"
    conn.engine.execute(p_query3, idSub, idSlot, idSlot)
    conn.close()'''


# ADD
def add_course_slot(idCorso, giorno, orario):
    session.execute('aggiungi_corsi_slot ?, ?, ?', [idCorso, giorno, orario])
    session.commit()
    session.close()
    '''p_query = "CALL aggiungi_corsi_slot(" + str(idCorso) + ", " + str(giorno) + ", TIME '" + str(orario) + "')"
    session.execute(p_query)
    session.commit()
    session.close()'''


def add_weight_room_slot(idSala):
    session.execute('aggiungi_salapesi_slot ?', [idSala])
    session.commit()
    session.close()
    '''p_query = "CALL aggiungi_salapesi_slot(" + str(idSala) + ")"
    session.execute(p_query)
    session.commit()
    session.close()'''


# Day of week: select extract(dow from date '2021-07-30');