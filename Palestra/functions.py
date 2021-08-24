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
    subscriber = session.query(classes.Subscriber).filter(classes.Subscriber.id == id).first()
    '''conn = engine.connect()
    p_query = "SELECT * FROM abbonati WHERE id = %s"
    subscriber = conn.engine.execute(p_query, id).first()
    conn.close()'''
    return classes.Subscriber(subscriber.id, subscriber.abbonamento, subscriber.datafineabbonamento, subscriber.datafineabbonamento, subscriber.durata)


def get_user_by_email(email):
    user = session.query(classes.User).filter(classes.User.email == email).first()
    '''conn = engine.connect()
    p_query = "SELECT * FROM utenti WHERE email = %s"
    user = conn.engine.execute(p_query, email).first()
    conn.close()'''
    return classes.User(user.id, user.username, user.password, user.nome, user.cognome, user.email, user.datanascita)


# Funzione per autoincrementare id tramite query
def get_id_increment():
    user = session.query(classes.User).filter(classes.User.id >= 100).order_by(classes.User.id.desc()).first()
    '''conn = engine.connect()
    p_query = "SELECT * FROM utenti WHERE id>=100 ORDER BY id DESC"
    user = conn.engine.execute(p_query).first()
    conn.close()'''
    if user:
        return user.id + 1
    else:
        return first_id_client


def get_course_id_increment():
    course = session.query(classes.Course).order_by(classes.Course.id.desc()).first()
    '''conn = engine.connect()
    p_query = "SELECT * FROM corsi ORDER BY id DESC"
    course = conn.engine.execute(p_query).first()
    conn.close()'''
    if course:
        return course.id + 1
    else:
        return 0


def get_room_id_increment():
    room = session.query(classes.Room).order_by(classes.Room.id.desc()).first()
    '''conn = engine.connect()
    p_query = "SELECT * FROM stanze ORDER BY id DESC"
    room = conn.engine.execute(p_query).first()
    conn.close()'''
    if room:
        return room.id + 1
    else:
        return 0


def get_weight_room_id_increment():
    weight_room = session.query(classes.WeightRoom).order_by(classes.WeightRoom.id.desc()).first()
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
    user = session.query(classes.User).filter(classes.User.id == 0).first()
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
    sub = session.query(classes.Subscription).filter(classes.Subscription.tipo == subscription).first()
    '''conn = engine.connect()
    p_query = "SELECT * FROM abbonamenti WHERE tipo = %s"
    sub = conn.engine.execute(p_query, subscription).first()
    conn.close()'''
    return classes.Subscription(sub.id, sub.tipo, sub.costo)


def get_subscription_by_id(id):
    sub = session.query(classes.Subscription).filter(classes.Subscription.id == id).first()
    '''conn = engine.connect()
    p_query = "SELECT * FROM abbonamenti WHERE id = %s"
    sub = conn.engine.execute(p_query, id).first()
    conn.close()'''
    return classes.Subscription(sub.id, sub.tipo, sub.costo)


def get_courses():
    courses = session.query(classes.Course).order_by(classes.Course.id.asc()).all()
    '''conn = engine.connect()
    p_query = "SELECT * FROM corsi ORDER BY id ASC"
    courses = conn.engine.execute(p_query)
    conn.close()'''
    return courses


def get_course(idCorso):
    course = session.query(classes.Course).filter(classes.Course.id == idCorso).first()
    '''conn = engine.connect()
    p_query = "SELECT * FROM corsi WHERE id = %s"
    course = conn.engine.execute(p_query, idCorso).first()
    conn.close()'''
    return classes.Course(course.id, course.nome, course.iscrittimax, course.istruttore, course.stanza)


def get_last_id_course():
    course = session.query(classes.Course).order_by(classes.Course.id.desc()).first()
    '''conn = engine.connect()
    p_query = "SELECT * FROM corsi ORDER BY id DESC"
    course = conn.engine.execute(p_query).first()
    conn.close()'''
    return course.id


def get_rooms():
    rooms = session.query(classes.Room).order_by(classes.Room.id.asc()).all()
    '''conn = engine.connect()
    p_query = "SELECT * FROM stanze ORDER BY id ASC"
    rooms = conn.engine.execute(p_query)
    conn.close()'''
    return rooms


def get_weight_rooms():
    weight_rooms = session.query(classes.WeightRoom).order_by(classes.WeightRoom.id.asc()).all()
    '''conn = engine.connect()
    p_query = "SELECT * FROM salepesi ORDER BY id ASC"
    weight_rooms = conn.engine.execute(p_query)
    conn.close()'''
    return weight_rooms


def get_trainers():
    trainers = session.query(classes.User).filter(classes.Trainer.id == classes.User.id).order_by(classes.Trainer.id.asc()).all()
    '''conn = engine.connect()
    p_query = "SELECT * FROM istruttori NATURAL JOIN utenti ORDER BY id ASC"
    trainers = conn.engine.execute(p_query)
    conn.close()'''
    return trainers


def get_clients():
    clients = session.query(classes.User).filter(classes.Client.id == classes.User.id).order_by(classes.Client.id.asc()).all()
    '''conn = engine.connect()
    p_query = "SELECT * FROM clienti NATURAL JOIN utenti ORDER BY id ASC"
    clients = conn.engine.execute(p_query)
    conn.close()'''
    return clients


def get_information():
    info = session.query(classes.Information).first()
    '''conn = engine.connect()
    p_query = "SELECT * FROM informazioni"
    info = conn.engine.execute(p_query).first()
    conn.close()'''
    return classes.Information(info.accessisettimana, info.slotgiorno, info.personemaxslot, info.personemq)


def get_checks():
    checks = session.query(classes.Checks).first()
    '''conn = engine.connect()
    p_query = "SELECT * FROM controlli"
    checks = conn.engine.execute(p_query).first()
    conn.close()'''
    return classes.Checks(checks.controllo)


def get_slot_from_date(data):
    slots = session.query(classes.Slot).filter(classes.Slot.giorno == data).all()
    '''conn = engine.connect()
    p_query = "SELECT * FROM slot WHERE giorno = DATE %s"
    slots = conn.engine.execute(p_query, data)
    conn.close()'''
    return slots


def get_slot_weight_rooms(idSlot, subscription):
    if subscription=='corsi':
        return None
    else:
        weightrooms = session.query(classes.WeightRoom).filter(classes.WeightRoom.id.in_(
            session.query(classes.WeightRoomSlot.salapesi).filter(classes.WeightRoomSlot.slot == idSlot)
        )).all()
        '''conn = engine.connect()
        
        p_query = "SELECT * FROM salepesi WHERE id IN (SELECT salapesi FROM salapesislot WHERE slot= %s)"
        weightrooms = conn.engine.execute(p_query, idSlot)
        conn.close()'''
        return weightrooms


def get_slot_courses(idSlot, subscription):
    if subscription=='sala_pesi':
        return None
    else:
        courses = session.query(classes.Course).filter(classes.Course.id.in_(
            session.query(classes.CourseSlot.corso).filter(classes.CourseSlot.slot == idSlot)
        )).all()
        '''conn = engine.connect()
        p_query = "SELECT * FROM corsi WHERE id IN (SELECT corso FROM corsislot WHERE slot= %s)"
        courses = conn.engine.execute(p_query, idSlot)
        conn.close()'''
        return courses


def get_coursesitting_id(idSlot, idCorso):
    giorno = session.query(classes.Slot.giorno).filter(classes.Slot.id == idSlot)
    id_sitting = session.query(classes.CourseSitting.id).filter(and_(func.DATE(classes.CourseSitting.dataseduta) == giorno, classes.CourseSitting.corso == idCorso)).first()
    '''conn = engine.connect()
    p_query = "SELECT id FROM sedutecorsi WHERE (dataseduta::date)=(SELECT giorno FROM slot WHERE id = %s) AND corso = %s"
    id_sitting = conn.engine.execute(p_query, idSlot, idCorso).first()
    conn.close()'''
    return id_sitting


def get_weightroomsitting_id(idSlot, idSala):
    giorno = session.query(classes.Slot.giorno).filter(classes.Slot.id == idSlot)
    id_sitting = session.query(classes.WeightRoomSitting.id).filter(and_(func.DATE(classes.WeightRoomSitting.dataseduta) == giorno, classes.WeightRoomSitting.salapesi == idSala)).first()
    '''conn = engine.connect()
    p_query = "SELECT id FROM sedutesalepesi WHERE (dataseduta::date)=(SELECT giorno FROM slot WHERE id = %s) AND salapesi = %s"
    id_sitting = conn.engine.execute(p_query, idSlot, idSala).first()
    conn.close()'''
    return id_sitting


def get_reservations(idSub):
    reservations = session.query(classes.Reservation.slot, classes.Slot.giorno, classes.Slot.orainizio, classes.Slot.orafine).filter(and_(classes.Reservation.slot == classes.Slot.id, classes.Reservation.abbonato == idSub, classes.Slot.giorno > func.current_date())).all()
    '''conn = engine.connect()
    p_query = "SELECT * FROM prenotazioni p JOIN slot s ON p.slot=s.id WHERE p.abbonato = %s AND s.giorno > CURRENT_DATE"
    reservations = conn.engine.execute(p_query, idSub)
    conn.close()'''
    return reservations


def get_last_seven_days():
    days = session.query(classes.Day).filter(and_(classes.Day.data > func.current_date() - 7, classes.Day.data <= func.current_date()))
    return days


def get_infected(giorno, infetto):
    '''
     (SELECT abbonato
      FROM prenotazioni
      WHERE abbonato <> infetto AND slot IN (SELECT slot
                                            FROM prenotazioni JOIN slot
                                            WHERE abbonato = infetto AND slot.giorno >= giorno))
     UNION
     SELECT nonabbonato
     FORM prenotazioninonabbonati
     WHERE nonabbonato <> infetto   AND slot IN (SELECT slot
                                                FROM prenotazioni JOIN slot
                                                WHERE abbonato = infetto AND slot.giorno >= giorno))

    '''
    if is_subscriber(infetto):
        slots = session.query(classes.Reservation.slot).filter(
            and_(classes.Reservation.abbonato == infetto, classes.Reservation.slot == classes.Slot.id, classes.Slot.giorno >= giorno))
    else:
        slots = session.query(classes.NSReservation.slot).filter(
            and_(classes.NSReservation.nonabbonato == infetto, classes.NSReservation.slot == classes.Slot.id, classes.Slot.giorno >= giorno))
    sub_infected = session.query(classes.User).filter(
        and_(classes.User.id == classes.Client.id, classes.Client.id != infetto, classes.Client.id == classes.Subscriber.id, classes.Client.id == classes.Reservation.abbonato, classes.Reservation.slot.in_(slots)))
    notsub_infected = session.query(classes.User).filter(
        and_(classes.User.id == classes.Client.id, classes.Client.id != infetto, classes.Client.id == classes.NotSubscriber.id, classes.Client.id == classes.NSReservation.nonabbonato, classes.NSReservation.slot.in_(slots)))
    infected = sub_infected.union(notsub_infected)
    return infected


# BOOLEANS
def is_subscriber(user_id):
    p_query = session.query(classes.Subscriber).filter(classes.Subscriber.id == user_id).first()
    '''conn = engine.connect()
    p_query = "SELECT * FROM abbonati WHERE id = %s"
    sub = conn.engine.execute(p_query, user_id).first()
    conn.close()'''
    if p_query:
        return True
    else:
        return False


def is_reserved(user_id, idSlot):
    res = session.query(classes.Reservation).filter(and_(classes.Reservation.abbonato == user_id, classes.Reservation.slot == idSlot)).first()
    '''conn = engine.connect()
    p_query = "SELECT * FROM prenotazioni WHERE abbonato = %s AND slot = %s"
    res = conn.engine.execute(p_query, user_id, idSlot).first()
    conn.close()'''
    if res:
        return True
    else:
        return False


def is_available_slot(idSlot):
    res = session.query(func.count(classes.Reservation.abbonato)).filter(classes.Reservation.slot == idSlot).first()
    personemax = session.query(classes.Slot.personemax).filter(classes.Slot.id == idSlot).first()
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
    res = session.query(func.count()).filter(classes.SubscriberCourseSession.seduta == idSeduta).first()
    corso = session.query(classes.CourseSitting.corso).filter(classes.CourseSitting.id == idSeduta)
    iscrittimax_corso = session.query(classes.Course.iscrittimax).filter(classes.Course.id == corso).first()
    iscrittimax_corsislot = session.query(classes.CourseSlot.iscrittimax).filter(and_(classes.CourseSlot.corso == corso, classes.CourseSlot.slot == idSlot)).first()
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
    res = session.query(func.count()).filter(classes.SubscriberWeightRoomSession.seduta == idSeduta).first()
    sala = session.query(classes.WeightRoomSitting.salapesi).filter(classes.WeightRoomSitting.id == idSeduta)
    iscrittimax_sala = session.query(classes.WeightRoom.iscrittimax).filter(classes.WeightRoom.id == sala).first()
    iscrittimax_salapesislot = session.query(classes.WeightRoomSlot.iscrittimax).filter(and_(classes.WeightRoomSlot.salapesi == sala, classes.WeightRoomSlot.slot == idSlot)).first()
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
    res1 = session.query(func.extract('dow', func.DATE(giorno))).first()
    if int(str(res1)[1:2]) > 0:
        res2 = session.query(func.count(classes.Slot.giorno.distinct())).filter(
            and_(classes.Reservation.slot == classes.Slot.id, classes.Reservation.abbonato == user_id, classes.Slot.giorno > func.DATE(giorno) - int(str(res1)[1:2]),
                 classes.Slot.giorno <= func.DATE(giorno) + (7 - int(str(res1)[1:2])), classes.Slot.giorno != func.DATE(giorno))).first()
    else:
        res2 = session.query(func.count(classes.Slot.giorno.distinct())).filter(
            and_(classes.Reservation.slot == classes.Slot.id, classes.Reservation.abbonato == user_id, classes.Slot.giorno >= func.DATE(giorno) - 6,
                 classes.Slot.giorno <= func.DATE(giorno), classes.Slot.giorno != func.DATE(giorno))).first()
    res3 = session.query(classes.Information.accessisettimana).first()

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
    res1 = session.query(func.count()).filter(and_(classes.Reservation.slot == classes.Slot.id, classes.Reservation.abbonato == user_id, classes.Slot.giorno == func.DATE(giorno))).first()
    res2 = session.query(classes.Information.slotgiorno).first()
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
    session.query(classes.Checks).update({"controllo": controlliGiornalieri})
    '''conn = engine.connect()
    p_query = "UPDATE controlli SET controllo = %s"
    conn.engine.execute(p_query, controlliGiornalieri)
    conn.close()'''


def set_information_accessisettimana(accessiSettimana):
    session.query(classes.Information).update({"accessisettimana": accessiSettimana})
    '''conn = engine.connect()
    p_query = "UPDATE informazioni SET accessisettimana = %s"
    conn.engine.execute(p_query, accessiSettimana)
    conn.close()'''


def set_information_slotgiorno(slotGiorno):
    session.query(classes.Information).update({"slotgiorno": slotGiorno})
    '''conn = engine.connect()
    p_query = "UPDATE informazioni SET slotgiorno = %s"
    conn.engine.execute(p_query, slotGiorno)
    conn.close()'''


def set_information_personemaxslot(personeMax):
    session.query(classes.Information).update({"personemaxslot": personeMax})
    '''conn = engine.connect()
    p_query = "UPDATE informazioni SET personemaxslot = %s"
    conn.engine.execute(p_query, personeMax)
    conn.close()'''


def set_information_personemq(personeMq):
    session.query(classes.Information).update({"personemq": personeMq})
    '''conn = engine.connect()
    p_query = "UPDATE informazioni SET personemq = %s"
    conn.engine.execute(p_query, personeMq)
    conn.close()'''


def update_weight_room(idSala, dimensione):
    pmq = get_information().personemq
    session.query(classes.WeightRoom).filter(classes.WeightRoom.id == idSala).update({"dimensione": dimensione, "iscrittimax": int(dimensione)/pmq})
    '''conn = engine.connect()
    pmq = get_information().personemq
    p_query = "UPDATE salepesi SET dimensione = %s, iscrittimax = %s WHERE id = %s"
    conn.engine.execute(p_query, dimensione, int(dimensione)/pmq, idSala)
    conn.close()'''


def update_room(idStanza, nome, dimensione):
    session.query(classes.Room).filter(classes.Room.id == idStanza).update({"nome": nome, "dimensione": dimensione})
    '''conn = engine.connect()
    p_query = "UPDATE stanze SET nome = %s, dimensione = %s WHERE id = %s"
    conn.engine.execute(p_query, nome, dimensione, idStanza)
    conn.close()'''


def update_course(idCorso, nome, iscrittiMax, idIstruttore, idStanza):
    session.query(classes.Course).filter(classes.Course.id == idCorso).update({"nome": nome, "iscrittimax": iscrittiMax, "istruttore": idIstruttore, "stanza": idStanza})
    '''conn = engine.connect()
    p_query = "UPDATE corsi SET nome = %s, iscrittimax = %s, istruttore = %s, stanza = %s WHERE id = %s"
    conn.engine.execute(p_query, nome, iscrittiMax, idIstruttore, idStanza, idCorso)
    conn.close()'''


# REMOVE
def remove_room(idStanza):
    session.query(classes.Room).filter(classes.Room.id == idStanza).delete()
    '''conn = engine.connect()
    p_query = "DELETE FROM stanze WHERE id = %s"
    conn.engine.execute(p_query, idStanza)
    conn.close()'''


def remove_weight_room(idSala):
    session.query(classes.WeightRoom).filter(classes.WeightRoom.id == idSala).delete()
    '''conn = engine.connect()
    p_query = "DELETE FROM salepesi WHERE id = %s"
    conn.engine.execute(p_query, idSala)
    conn.close()'''


def remove_course(idCorso):
    session.query(classes.Course).filter(classes.Course.id == idCorso).delete()
    '''conn = engine.connect()
    p_query = "DELETE FROM corsi WHERE id = %s"
    conn.engine.execute(p_query, idCorso)
    conn.close()'''


def remove_not_subscriber(idCliente):
    session.query(classes.NotSubscriber).filter(classes.NotSubscriber.id == idCliente).delete()
    '''conn = engine.connect()
    p_query = "DELETE FROM nonabbonati WHERE id = %s"
    conn.engine.execute(p_query, idCliente)
    conn.close()'''


def is_reserved_course(idSub, idSlot):
    res = session.query(classes.SubscriberCourseSession.abbonato).filter(
        and_(classes.SubscriberCourseSession.abbonato == idSub, classes.SubscriberCourseSession.seduta == classes.CourseSitting.id,
             classes.CourseSitting.corso == classes.Course.id, classes.Course.id == classes.CourseSlot.corso, classes.CourseSlot.slot == idSlot)).first()
    if res is not None:
        return True
    else:
        return False


def remove_reservation(idSub, idSlot):
    session.query(classes.Reservation).filter(and_(classes.Reservation.abbonato == idSub, classes.Reservation.slot == idSlot)).delete()
    if is_reserved_course(idSub, idSlot):
        session.query(classes.SubscriberCourseSession).filter(
            and_(classes.SubscriberCourseSession.abbonato == idSub, classes.SubscriberCourseSession.seduta == classes.CourseSitting.id,
                 classes.CourseSitting.corso == classes.Course.id, classes.Course.id == classes.CourseSlot.corso, classes.CourseSlot.slot == idSlot)).delete(synchronize_session='fetch')
    else:
        session.query(classes.SubscriberWeightRoomSession).filter(
            and_(classes.SubscriberWeightRoomSession.abbonato == idSub, classes.SubscriberWeightRoomSession.seduta == classes.WeightRoomSitting.id,
                 classes.WeightRoomSitting.salapesi == classes.WeightRoom.id, classes.WeightRoom.id == classes.WeightRoomSlot.salapesi,
                 classes.WeightRoomSlot.slot == idSlot)).delete(synchronize_session='fetch')
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
    '''db.session.execute('aggiungi_corsi_slot(:idcorso, :giorno, :slot)', (idCorso, giorno, orario))
    session.execute('aggiungi_corsi_slot ?, ?, ?', (idCorso), (giorno), (orario))
    session.commit()
    session.close()'''
    p_query = "CALL aggiungi_corsi_slot(" + str(idCorso) + ", " + str(giorno) + ", TIME '" + str(orario) + "')"
    session.execute(p_query)
    session.commit()
    session.close()


def add_weight_room_slot(idSala):
    '''session.execute('aggiungi_salapesi_slot ?', (idSala))
    session.commit()
    session.close()'''
    p_query = "CALL aggiungi_salapesi_slot(" + str(idSala) + ")"
    session.execute(p_query)
    session.commit()
    session.close()


# Day of week: select extract(dow from date '2021-07-30');