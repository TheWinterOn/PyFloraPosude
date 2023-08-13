import random
import datetime as dt
import locale
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

MIN_PH = 0
MAX_PH = 14
MIN_SALINITET = 1.0
MAX_SALINITET = 5.0
MIN_VLAZNOST_ZEMLJE = 1.0
MAX_VLAZNOST_ZEMLJE = 30.0
MIN_TEMP_PROSTORIJE = 18.0
MAX_TEMP_PROSTORIJE = 35.0
MIN_TEMP_ALGEBRA = -25.0
MAX_TEMP_ALGEBRA = 45.0
N = 1

API_KEY = "WLa7rM9AAmARlu5qABakpfTmCUzdkGit"
LOCATION_KEY = "1606699"
URL = "http://dataservice.accuweather.com/currentconditions/v1/"


def sync():
    locale.setlocale(locale.LC_TIME, "hr_HR")
    print(dt.datetime.now().strftime("%A %d.%m.%Y %H:%M:%S").capitalize())
    print(random.randint(MIN_PH, MAX_PH))
    print(round(random.uniform(MIN_SALINITET, MAX_SALINITET), N))
    print(round(random.uniform(MIN_VLAZNOST_ZEMLJE, MAX_VLAZNOST_ZEMLJE), N))
    print(round(random.uniform(MIN_TEMP_PROSTORIJE, MAX_TEMP_PROSTORIJE), N))

    status_code, current_temperature = get_meteo_data()
    print(status_code)
    print(current_temperature)


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
            random.uniform(MIN_TEMP_ALGEBRA, MAX_TEMP_ALGEBRA), N
        )
    return response.status_code, current_temperature


# sync()
