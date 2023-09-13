import sqlalchemy as db
from sqlalchemy.orm import Session, relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Pot(Base):
    __tablename__ = "pot"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    plant_id = db.Column(db.Integer, db.ForeignKey("plant.id"))


db_engine = db.create_engine("sqlite:///databases/pot_database/pot_database.db")
Base.metadata.create_all(bind=db_engine)


# CRUD Pot
def db_add_pot(name, photo, soil_moisture, ph, salinity, light_level, temperature):
    with Session(bind=db_engine) as session:
        pot_exists = session.query(Pot).filter(Pot.name == name).one_or_none()

        if pot_exists:
            return

        pot = Pot(
            name=name,
            photo=photo,
            soil_moisture=soil_moisture,
            ph=ph,
            salinity=salinity,
            light_level=light_level,
            temperature=temperature,
        )
        session.add(pot)
        session.commit()


def db_get_pot(name):
    with Session(bind=db_engine) as session:
        pot = session.query(Pot).filter(Pot.name == name).one_or_none()
        return pot


def db_get_pots():
    with Session(bind=db_engine) as session:
        pots = session.query(Pot).all()
        return pots


def db_update_pot(name, photo, soil_moisture, ph, salinity, light_level, temperature):
    with Session(bind=db_engine) as session:
        current_pot = session.query(Pot).filter(Pot.name == name)
        current_pot.update(
            values={
                "name": name,
                "photo": photo,
                "soil_moisture": soil_moisture,
                "ph": ph,
                "salinity": salinity,
                "light_level": light_level,
                "temperature": temperature,
            }
        )
        session.commit()
        print(current_pot)


def db_delete_pot(name):
    with Session(bind=db_engine) as session:
        pot = session.query(Pot).filter(Pot.name == name).one_or_none()

        if pot:
            session.delete(pot)
            session.commit()
        else:
            print("No such pot!")  # TODO write message in gui that pot doesn't exist