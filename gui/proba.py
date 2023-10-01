import tkinter as tk
from PIL import Image, ImageTk
from config import IMAGE_SIZE
from databases.plant_and_pot_database.plant_and_pot_database import (
    db_get_plants,
    db_add_plant,
    db_get_plant_by_id,
    db_get_plant_by_name,
    db_update_plant,
    db_remove_plant_photo_uri,
    db_delete_plant,
    check_input_data,
    db_add_pot,
    db_delete_pot,
    db_get_pots,
)


def zovi():
    root = tk.Tk()

    pots = db_get_pots()
    for pot in pots:
        lbl_frm_pot = tk.LabelFrame(root)

        lbl_frm_pot.grid(row=0, rowspan=4, column=0, columnspan=2, padx=5, pady=5)

        plant = db_get_plant_by_id(pot.plant_id)
        plant_photo = Image.open(plant.photo)
        plant_photo = plant_photo.resize(IMAGE_SIZE)
        image = ImageTk.PhotoImage(plant_photo)
        lbl_image = tk.Label(lbl_frm_pot, image=image)
        lbl_image.grid(row=0, rowspan=4, column=0)

        lbl_pot_name = tk.Label(lbl_frm_pot, text="Naziv")
        lbl_pot_name.grid(row=0, column=1)
        btn_pot_name = tk.Button(lbl_frm_pot, text=pot.name)
        btn_pot_name.grid(row=1, column=1)
        pot_status = tk.StringVar()
        pot_status.set("Status\n" + "OK")
        lbl_pot_status = tk.Label(lbl_frm_pot, textvariable=pot_status)
        lbl_pot_status.grid(row=3, column=1)

    root.mainloop()
