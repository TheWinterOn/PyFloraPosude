import config

from gui.gui import *
from databases.user_database.user_database import add_default_user
from databases.pot_database.pot_database import add_default_pot
from databases.plant_database.plant_database import add_default_plants
from sensors.generate_sensor_data import clear_sensor_database

add_default_user()
add_default_pot()
add_default_plants()
clear_sensor_database()

gui()
