from gui.gui import gui
from databases.user_database.user_database import add_default_user
from databases.plant_and_pot_database.plant_and_pot_database import (
    add_default_pot,
    add_default_plants,
)
from sensors.generate_sensor_data import clear_sensor_database


def main():
    clear_sensor_database()
    add_default_user()
    add_default_pot()
    add_default_plants()

    gui()


if __name__ == "__main__":
    main()
