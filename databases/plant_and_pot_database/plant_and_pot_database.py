import sqlalchemy as db
from sqlalchemy.orm import Session, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sensors.generate_sensor_data import sync_one

URI = "databases/plant_and_pot_database/plant_photos/"

Base = declarative_base()


class Plant(Base):
    __tablename__ = "plant"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    photo = db.Column(db.String, nullable=False)
    soil_moisture = db.Column(db.Float)
    ph = db.Column(db.Float)
    salinity = db.Column(db.Float)
    light_level = db.Column(db.Integer)
    temperature = db.Column(db.Float)
    pots = relationship("Pot", backref=backref("plant"))


class Pot(Base):
    __tablename__ = "pot"
    id = db.Column(db.Integer, primary_key=True)
    plant_id = db.Column(db.Integer, db.ForeignKey("plant.id"))
    name = db.Column(db.String, nullable=False)


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


def db_get_plant_by_name(name):
    with Session(bind=db_engine) as session:
        plant = session.query(Plant).filter(Plant.name == name).one_or_none()
        return plant


def db_get_plant_by_id(id):
    with Session(bind=db_engine) as session:
        plant = session.query(Plant).filter(Plant.id == id).one_or_none()
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


# # TODO delete this, for testing purposes only
# def db_print_plant(
#     id, name, photo, soil_moisture, ph, salinity, light_level, temperature
# ):
#     print(id)
#     print(name)
#     print(photo)
#     print(soil_moisture)
#     print(ph)
#     print(salinity)
#     print(light_level)
#     print(temperature)


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
        ["Kaktus", "kaktus.jpg"],
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
def db_add_pot(pot_name, plant_name):
    with Session(bind=db_engine) as session:
        # Imena posuda su unikatna osim ako je posuda prazna. Sve prazne posude imaju ime PRAZNA posuda.
        # Provjera da li posuda prazna
        if not pot_name:
            pot = Pot(name="PRAZNA posuda")
        elif "prazna" in pot_name.lower() or not plant_name:
            pot = Pot(name="PRAZNA posuda")
        else:
            pot = session.query(Pot).filter(Pot.name == pot_name).one_or_none()
            if pot:
                print("Posuda s tim imenom vec postoji! Odaberite drugo ime!")
                return
            else:
                pot = Pot(name=pot_name)

        # Biljka se bira iz padajuceg izbornika, tako da sigurno postoji u bazi
        # Ako nije odabrana ni jedna biljka iz izbornika onda se ovaj korak preskace
        if plant_name and pot.name != "PRAZNA posuda":
            plant = session.query(Plant).filter(Plant.name == plant_name).one_or_none()
        else:
            plant = None

        pot.plant = plant
        session.add(pot)
        session.commit()


def db_get_pot(name):
    with Session(bind=db_engine) as session:
        pot = session.query(Pot).filter(Pot.name == name).first()
        return pot


def db_get_pots():
    with Session(bind=db_engine) as session:
        pots = session.query(Pot).all()
        return pots


def db_update_pot(pot_name, plant_name):
    with Session(bind=db_engine) as session:
        if not plant_name or not pot_name:
            return
        elif "prazan" in pot_name.lower():
            return
        pot = session.query(Pot).filter(Pot.name == pot_name).one_or_none()
        if pot:
            print("Posuda s tim imenom vec postoji! Odaberite drugo ime!")
            return

        current_pot = db_get_pot("PRAZNA posuda")
        plant = db_get_plant_by_name(plant_name)

        pot = session.query(Pot).filter(
            db.and_(Pot.id == current_pot.id, Pot.name == "PRAZNA posuda")
        )
        pot.update(values={"name": pot_name, "plant_id": plant.id})
        session.commit()


def db_remove_plant_from_pot(pot_name):
    with Session(bind=db_engine) as session:
        current_pot = db_get_pot(pot_name)
        pot = session.query(Pot).filter(Pot.id == current_pot.id)
        pot.update(values={"name": "PRAZNA posuda", "plant_id": None})
        session.commit()


def db_delete_pot(pot_name):
    with Session(bind=db_engine) as session:
        pot = session.query(Pot).filter(Pot.name == pot_name).first()

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
    db_add_pot(pot_name="PRAZNA posuda", plant_name=None)
    db_add_pot(pot_name="Boravak", plant_name="Kaktus")
    db_add_pot(pot_name="Kuhinja", plant_name="Hoya")
    sync_all()


# Handling bad input data
def check_input_data(soil_moisture, ph, salinity, light_level, temperature):
    soil_moisture = check_if_float(soil_moisture)
    ph = check_if_float(ph)
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


# Funkcija Sync gumba na glavnoj stranici. Uzima mjerenja senzora za sve postojece posude koje u sebi imaju biljku i nisu potrgane i zapisuje ih u bazu
def sync_all():
    pots = db_get_pots()
    for pot in pots:
        if pot.name != "PRAZNA posuda":  # TODO dodati uvijet za potrganu posudu
            sync_one(pot.name)
