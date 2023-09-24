import sqlalchemy as db
from sqlalchemy.orm import Session, relationship, backref
from sqlalchemy.ext.declarative import declarative_base

URI = "databases/plant_and_pot_database/plant_photos/"

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


class Pot(Base):
    __tablename__ = "pot"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    plant_id = db.Column(db.Integer, db.ForeignKey("plant.id"))


db_engine = db.create_engine(
    "sqlite:///databases/plant_and_pot_database/plant_and_pot_database.db"
)
Base.metadata.create_all(bind=db_engine)


# CRUD Plant
def db_add_plant(name, photo, soil_moisture, ph, salinity, light_level, temperature):
    with Session(bind=db_engine) as session:
        plant_exists = session.query(Plant).filter(Plant.name == name).one_or_none()
        if plant_exists:
            print("Plant already exists in database!")
            return

        plant = Plant(
            name=name,
            photo=f"{URI}{photo}",
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


def db_update_plant(
    id, name, photo, soil_moisture, ph, salinity, light_level, temperature
):
    with Session(bind=db_engine) as session:
        plant = session.query(Plant).filter(Plant.id == id)
        plant.update(
            values={
                "name": name,
                "photo": f"{URI}{photo}",
                "soil_moisture": soil_moisture,
                "ph": ph,
                "salinity": salinity,
                "light_level": light_level,
                "temperature": temperature,
            }
        )
        session.commit()


# TODO delete this, for testing purposes only
def db_print_plant(
    id, name, photo, soil_moisture, ph, salinity, light_level, temperature
):
    print(id)
    print(name)
    print(photo)
    print(soil_moisture)
    print(ph)
    print(salinity)
    print(light_level)
    print(temperature)


def db_delete_plant(name):
    with Session(bind=db_engine) as session:
        plant = session.query(Plant).filter(Plant.name == name).one_or_none()

        if plant:
            session.delete(plant)
            session.commit()
        else:
            print("No such plant!")


def db_delete_plants():
    with Session(bind=db_engine) as session:
        session.query(Plant).delete()
        session.commit()


def db_remove_plant_photo_uri(plant):
    if URI in plant.photo:
        plant.photo = plant.photo.replace(URI, "")
    return plant


def add_default_plants():
    db_delete_plants()

    predefined_plants = [
        ["Aglaonema", "aglaonema.jpg"],
        ["Aloe Vera", "aloe_vera.jpg"],
        ["Biljka pauk", "biljka_pauk.jpg"],
        ["Hoya", "hoya.jpg"],
        ["Kaktus", "kaktua.jpg"],
        ["Kalanhoa", "kalanhoa.jpg"],
        ["Sansevijerija", "sansevijerija.jpg"],
        ["Slonova noga", "slonova_noga.jpg"],
        ["Zebra Haworthija", "zebra_haworthija.jpg"],
        ["Zamija", "zamija.jpg"],
        ["Zlatni puzavac", "zlatni_puzavac.jpg"],
    ]

    for plant in predefined_plants:
        db_add_plant(
            name=plant[0],
            photo=plant[1],
            # soil_moisture=plant[2],
            # ph=plant[3],
            # salinity=plant[4],
            # light_level=plant[5],
            # temperature=plant[6],
            soil_moisture=None,
            ph=None,
            salinity=None,
            light_level=None,
            temperature=None,
        )


# CRUD Pot
def db_add_pot(name):
    with Session(bind=db_engine) as session:
        # Jedina unikatna stvar u pot bazi su id-evi. Imena nisu unikatna te zbog toga nema provjere.
        pot = Pot(name=name)
        session.add(pot)
        session.commit()


def db_get_pot(id):
    with Session(bind=db_engine) as session:
        pot = session.query(Pot).filter(Pot.id == id).one_or_none()
        return pot


def db_get_pots():
    with Session(bind=db_engine) as session:
        pots = session.query(Pot).all()
        return pots


def db_update_pot(id, name):
    with Session(bind=db_engine) as session:
        current_pot = session.query(Pot).filter(Pot.id == id)
        current_pot.update(
            values={
                "name": name,
            }
        )
        session.commit()


def db_delete_pot(name):
    with Session(bind=db_engine) as session:
        pot = session.query(Pot).filter(Pot.name == name).one_or_none()

        if pot:
            session.delete(pot)
            session.commit()
        else:
            print("No such pot!")


def db_delete_pots():
    with Session(bind=db_engine) as session:
        session.query(Pot).delete()
        session.commit()


def add_default_pot():
    db_delete_pots()
    db_add_pot(name="PRAZNA posuda")


# Handling bad input data
def check_input_data(soil_moisture, ph, salinity, light_level, temperature):
    soil_moisture = check_if_float(soil_moisture)
    ph = check_if_int(ph)
    salinity = check_if_float(salinity)
    light_level = check_if_int(light_level)
    temperature = check_if_float(temperature)
    return soil_moisture, ph, salinity, light_level, temperature


def check_if_int(value):
    try:
        int(value)
        return value
    except ValueError:
        a = None
        return a
    except TypeError:
        a = None
        return a


def check_if_float(value):
    try:
        float(value)
        return value
    except ValueError:
        a = None
        return a
    except TypeError:
        a = None
        return a
