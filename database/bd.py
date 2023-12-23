from sqlalchemy import MetaData, Integer, String, ForeignKey, Table, Column, Date, Time, create_engine, func
from sqlalchemy.orm import sessionmaker, relationship, declarative_base


metadata = MetaData()
Base = declarative_base()
engine = None
Session = None
session = None

def init_db():
    global engine, Session, session
    engine = create_engine('sqlite:///db.sqlite3')
    Session = sessionmaker(bind=engine)
    session = Session()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    reservations = relationship('Reservation', back_populates='user')


class Reservation(Base):
    __tablename__ = 'reservation'
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    event = Column(String, nullable=False)
    status = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='reservations')



def get_booking_info():
    booking = session.query(Reservation).all()
    return booking


def add_user(user):
    new_id = session.query(func.max(User.id)).scalar() + 1
    new_user = User(id=new_id, full_name=user[0], email=user[1], password=user[2])
    session.add(new_user)
    session.commit()


def is_user_present(user_data):
    user_with_email = session.query(User).filter_by(email=user_data).first()
    if user_with_email:
        return True
    else:
        return False


def is_user_data_correct(user_data):
    user_with_email = session.query(User).filter_by(email=user_data[0]).first()
    if user_with_email:
        return user_with_email.password == user_data[1]
    return False


def add_booking(new_event_data, user_info):
    new_id = session.query(func.max(Reservation.id)).scalar() + 1
    user_name = session.query(User).filter_by(email=user_info).first()
    new_event = Reservation(id=new_id, date=new_event_data[0], time=new_event_data[1], event=new_event_data[2], status=new_event_data[3], user_id=user_name)
    session.add(new_event)
    session.commit()



def is_event_present(event_data):
    event = session.query(Reservation).filter_by(date=event_data[0]).first()
    if event:
        return event.time == event_data[1]
    return False

#new_event = Reservation(id=1, date="12-25", time="12:00", event="Film watching", status="waiting for correct time", user_id=1)
#new_usr = User(id=1, full_name="Nick Dom", email="nicolasdomashke@gmail.com", password="Aasdghg1f")
#user_to_delete = session.query(User).filter_by(id=0).first()
#session.delete(user_to_delete)
#session.add(new_event)
#session.commit()

#users = session.query(User).all()

#for user in users:
#    print(f"User ID: {user.id}, Name: {user.full_name}, Email: {user.email}, Password: {user.password}")