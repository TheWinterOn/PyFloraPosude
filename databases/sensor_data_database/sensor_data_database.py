import sqlalchemy as db
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Data(Base):
    __tablename__ = "data"
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    pot_name = db.Column(db.String)
    soil_moisture = db.Column(db.Float)
    ph = db.Column(db.Float)
    salinity = db.Column(db.Float)
    light_level = db.Column(db.Integer)
    room_temperature = db.Column(db.Float)
    algebra_temperature = db.Column(db.Float)


db_engine = db.create_engine(
    "sqlite:///databases/sensor_data_database/sensor_data_database.db"
)
Base.metadata.create_all(bind=db_engine)


# CRUD Data
def db_add_data(
    timestamp,
    pot_name,
    soil_moisture,
    ph,
    salinity,
    light_level,
    room_temperature,
    algebra_temperature,
):
    with Session(bind=db_engine) as session:
        data_exists = (
            session.query(Data)
            .filter(db.and_(Data.timestamp == timestamp, Data.pot_name == pot_name))
            .one_or_none()
        )

        if data_exists:
            db_update_data(
                timestamp,
                pot_name,
                soil_moisture,
                ph,
                salinity,
                light_level,
                room_temperature,
                algebra_temperature,
            )
            return

        data = Data(
            timestamp=timestamp,
            pot_name=pot_name,
            soil_moisture=soil_moisture,
            ph=ph,
            salinity=salinity,
            light_level=light_level,
            room_temperature=room_temperature,
            algebra_temperature=algebra_temperature,
        )
        session.add(data)
        session.commit()


def db_get_data():
    with Session(bind=db_engine) as session:
        data = session.query(Data).all()
        return data


def db_update_data(
    timestamp,
    pot_name,
    soil_moisture,
    ph,
    salinity,
    light_level,
    room_temperature,
    algebra_temperature,
):
    with Session(bind=db_engine) as session:
        current_data = session.query(Data).filter(
            db.and_(Data.timestamp == timestamp, Data.pot_name == pot_name)
        )
        current_data.update(
            values={
                # "timestamp": timestamp,
                "pot": pot_name,
                "soil_moisture": soil_moisture,
                "ph": ph,
                "salinity": salinity,
                "light_level": light_level,
                "room_temperature": room_temperature,
                "algebra_temperature": algebra_temperature,
            }
        )
        session.commit()
        print(current_data)


def db_delete_data():
    with Session(bind=db_engine) as session:
        session.query(Data).delete()
        session.commit()
