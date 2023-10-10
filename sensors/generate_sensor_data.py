import random
import datetime as dt
import locale
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from databases.sensor_data_database.sensor_data_database import (
    db_add_data,
    db_get_all_data,
    db_delete_data,
)

# from databases.plant_and_pot_database.plant_and_pot_database import db_get_pots
import json


MIN_SOIL_MOISTURE = 1.0
MAX_SOIL_MOISTURE = 30.0
MIN_PH = 0.0
MAX_PH = 14.0
MIN_SALINITY = 0.0
MAX_SALINITY = 5.0
MIN_LIGHT_LEVEL = 200
MAX_LIGHT_LEVEL = 5000
MIN_ROOM_TEMPERATURE = 15.0
MAX_ROOM_TEMPERATURE = 35.0
MIN_TEMPERATURE_ALGEBRA = -25.0
MAX_TEMPERATURE_ALGEBRA = 45.0
N = 1

API_KEY = "WLa7rM9AAmARlu5qABakpfTmCUzdkGit"
LOCATION_KEY = "1606699"  # Crnomerec, Zagreb
URL = "http://dataservice.accuweather.com/currentconditions/v1/"


def sync_one(pot_name):
    locale.setlocale(locale.LC_TIME, "hr_HR")

    # print(dt.datetime.now().strftime("%A %d.%m.%Y %H:%M:%S").capitalize())
    # print(round(random.uniform(MIN_SOIL_MOISTURE, MAX_SOIL_MOISTURE), N))
    # print(random.randint(MIN_PH, MAX_PH))
    # print(round(random.uniform(MIN_SALINITY, MAX_SALINITY), N))
    # print(random.randint(MIN_LIGHT_LEVEL, MAX_LIGHT_LEVEL))
    # print(round(random.uniform(MIN_ROOM_TEMPERATURE, MAX_ROOM_TEMPERATURE), N))

    # status_code, current_temperature = get_meteo_data()
    # print(status_code)
    # print(current_temperature)

    timestamp = dt.datetime.now()
    soil_moisture = round(random.uniform(MIN_SOIL_MOISTURE, MAX_SOIL_MOISTURE), N)
    ph = round(random.uniform(MIN_PH, MAX_PH), N)
    salinity = round(random.uniform(MIN_SALINITY, MAX_SALINITY), N)
    light_level = random.randint(MIN_LIGHT_LEVEL, MAX_LIGHT_LEVEL)
    room_temperature = round(
        random.uniform(MIN_ROOM_TEMPERATURE, MAX_ROOM_TEMPERATURE), N
    )
    algebra_temperature = get_meteo_data()

    db_add_data(
        timestamp,
        pot_name,
        soil_moisture,
        ph,
        salinity,
        light_level,
        room_temperature,
        algebra_temperature,
    )


def get_meteo_data():
    url_meteo = f"{URL}{LOCATION_KEY}?apikey={API_KEY}"

    session = Session()

    try:
        response = session.get(url_meteo)
        json_data = json.loads(response.text)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    if response.status_code == 200:
        for item in json_data:
            current_temperature = item["Temperature"]["Metric"]["Value"]
    else:
        current_temperature = round(
            random.uniform(MIN_TEMPERATURE_ALGEBRA, MAX_TEMPERATURE_ALGEBRA), N
        )
    return current_temperature


def clear_sensor_database():
    db_delete_data()
