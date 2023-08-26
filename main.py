import config

from gui.gui import *
from databases.user_database.user_database import add_default_user
from sensors.generate_sensor_data import clear_sensor_database

add_default_user()
clear_sensor_database()
gui()
