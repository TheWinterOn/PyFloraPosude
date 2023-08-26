import sqlalchemy as db
from sqlalchemy.orm import Session, relationship, backref
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Plant(Base):
    __tablename__ = "plant"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    photo = db.Column(db.String, nullable=False)
    soil_moisture = db.Column(db.Float)
    ph = db.Column(db.Integer)
    salinity = db.Column(db.Float)
    light_level = db.Column(db.Integer)
    temperature = db.Column(db.Float)
    pots = relationship("Pot", backref=backref("plant"))


db_engine = db.create_engine("sqlite:///databases/plant_database/plant_database.db")
Base.metadata.create_all(bind=db_engine)


# CRUD Plant
def db_add_plant(name, photo, soil_moisture, ph, salinity, light_level, temperature):
    with Session(bind=db_engine) as session:
        plant_exists = session.query(Plant).filter(Plant.name == name).one_or_none()

        if plant_exists:
            return

        plant = Plant(
            name=name,
            photo=photo,
            soil_moisture=soil_moisture,
            ph=ph,
            salinity=salinity,
            light_level=light_level,
            temperature=temperature,
        )
        session.add(plant)
        session.commit()


def db_get_plant(name):
    with Session(bind=db_engine) as session:
        plant = session.query(Plant).filter(Plant.name == name).one_or_none()
        return plant


def db_get_plants():
    with Session(bind=db_engine) as session:
        plants = session.query(Plant).all()
        return plants


def db_update_plant(name, photo, soil_moisture, ph, salinity, light_level, temperature):
    with Session(bind=db_engine) as session:
        current_plant = session.query(Plant).filter(Plant.name == name)
        current_plant.update(
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
        print(current_plant)


def db_delete_plant(name):
    with Session(bind=db_engine) as session:
        plant = session.query(Plant).filter(Plant.name == name).one_or_none()

        if plant:
            session.delete(plant)
            session.commit()
        else:
            print(
                "No such plant!"
            )  # TODO write message in gui that plant doesn't exist


# name, photo, soil_moisture, ph, salinity, light_level, temperature
predefined_plants = [
    ["Aglaonema", "databases/plant_database/plant_photos/aglaonema.jpg"],
    ["Aloe Vera", "databases/plant_database/plant_photos/aloe_vera.jpg"],
    ["Biljka pauk", "databases/plant_database/plant_photos/biljka_pauk.jpg"],
    ["Hoya", "databases/plant_database/plant_photos/hoya.jpg"],
    ["Kaktus", "databases/plant_database/plant_photos/kaktua.jpg"],
    ["Kalanhoa", "databases/plant_database/plant_photos/kalanhoa.jpg"],
    ["Sansevijerija", "databases/plant_database/plant_photos/sansevijerija.jpg"],
    ["Slonova noga", "databases/plant_database/plant_photos/slonova_noga.jpg"],
    ["Zebra Haworthija", "databases/plant_database/plant_photos/zebra_haworthija.jpg"],
    ["Zamija", "databases/plant_database/plant_photos/zamija.jpg"],
    ["Zlatni puzavac", "databases/plant_database/plant_photos/zlatni_puzavac.jpg"],
]


for plant in predefined_plants:
    db_add_plant(
        name=plant[0],
        photo=plant[1],
        soil_moisture=plant[2],
        ph=plant[3],
        salinity=plant[4],
        light_level=plant[5],
        temperature=plant[6],
    )
