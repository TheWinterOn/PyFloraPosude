import tkinter as tk
from tkinter import ttk
from config import font_btn, font_header, font_label, font_title
from databases.user_database.user_database import db_login, db_get_users, db_update_user
from databases.plant_and_pot_database.plant_and_pot_database import (
    db_get_plants,
    db_add_plant,
    db_get_plant,
    db_update_plant,
    db_remove_plant_photo_uri,
    db_delete_plant,
    check_input_data,
    db_print_plant,
)
from sensors.generate_sensor_data import sync


def gui():
    class PyFloraPosude:
        def __init__(self, root):
            self.root = root
            self.create_login_screen()

        def login(self):
            self.user = db_login(self.username.get(), self.password.get())
            if self.user == None:
                print("Na postoji korisnik s tim korisnickim imenom i lozinkom.")
                return
            print(f"Dobro dosli {self.user.name}")
            self.clear_root()
            self.create_main_screen()

        def logout(self):
            self.clear_root()
            self.create_login_screen()

        def on_user_save(self):
            db_update_user(
                self.user_id,
                self.user_name.get(),
                self.user_surname.get(),
                self.user_username.get(),
                self.user_password.get(),
            )
            self.on_user_cancel()

        def on_user_cancel(self):
            self.clear_root()
            self.create_main_screen()

        def on_plant_save(self):
            (
                self.plant_soil_moisture,
                self.plant_ph,
                self.plant_salinity,
                self.plant_light_level,
                self.plant_temperature,
            ) = check_input_data(
                self.plant_soil_moisture.get(),
                self.plant_ph.get(),
                self.plant_salinity.get(),
                self.plant_light_level.get(),
                self.plant_temperature.get(),
            )
            if self.action == "add":
                db_add_plant(
                    self.plant_name.get(),
                    self.plant_photo.get(),
                    self.plant_soil_moisture,
                    self.plant_ph,
                    self.plant_salinity,
                    self.plant_light_level,
                    self.plant_temperature,
                )
            elif self.action == "edit":
                db_update_plant(
                    self.plant_id.get(),
                    self.plant_name.get(),
                    self.plant_photo.get(),
                    self.plant_soil_moisture,
                    self.plant_ph,
                    self.plant_salinity,
                    self.plant_light_level,
                    self.plant_temperature,
                )
            self.on_plant_cancel()

        def on_plant_remove(self):
            db_delete_plant(self.plant_name.get())
            self.on_plant_cancel()

        def on_plant_cancel(self):
            self.plant_management()

        def on_plant_add(self):
            self.add_plant_page()

        def on_plant_edit(self):
            self.edit_plant_page()

        def on_plant_delete(self):
            self.delete_plant_page()

        def set_default_form_values(self):
            self.plant_soil_moisture.set(None)
            self.plant_ph.set(None)
            self.plant_salinity.set(None)
            self.plant_light_level.set(None)
            self.plant_temperature.set(None)

        def clear_root(self):
            for child in self.root.winfo_children():
                child.destroy()

        def clear_body(self):
            for child in self.frame_body.winfo_children():
                child.destroy()

        def callbackFunc(self, event):
            drop_menu = event.widget.get()
            selected_plant = db_get_plant(drop_menu)
            selected_plant = db_remove_plant_photo_uri(selected_plant)
            if self.action != "delete":
                self.plant_id.set(selected_plant.id)
            self.plant_name.set(selected_plant.name)
            self.plant_photo.set(selected_plant.photo)

            self.plant_soil_moisture.set(selected_plant.soil_moisture)
            self.plant_ph.set(selected_plant.ph)
            self.plant_salinity.set(selected_plant.salinity)
            self.plant_light_level.set(selected_plant.light_level)
            self.plant_temperature.set(selected_plant.temperature)

        def get_plant_list(self):
            self.plants = db_get_plants()
            plant_names = []
            for plant in self.plants:
                plant_names.append(plant.name)
            return plant_names

        def create_header(self):
            lbl_header = tk.Label(
                self.frame_header,
                text="PyFloraPosude",
                bg="grey",
                font=font_header,
            )
            lbl_header.grid(row=0, column=0, padx=10)

            btn_plants = tk.Button(
                self.frame_header,
                text="Biljke",
                font=font_btn,
                command=self.plant_management,
            )
            btn_plants.grid(row=0, column=1, padx=5, pady=5)
            btn_profile = tk.Button(
                self.frame_header,
                text="Moj profil",
                font=font_btn,
                command=self.create_profile_screen,
            )
            btn_profile.grid(row=0, column=2, padx=5, pady=5)
            btn_logout = tk.Button(
                self.frame_header, text="Odjava", font=font_btn, command=self.logout
            )
            btn_logout.grid(row=0, column=3, padx=5, pady=5)

        def create_login_screen(self):
            self.root.geometry("500x300")
            self.frame_login = tk.Frame(
                self.root, highlightbackground="black", highlightthickness=1
            )
            self.frame_login.pack(fill=tk.BOTH, padx=10, pady=10)

            lbl_header = tk.Label(
                self.frame_login,
                text="PyFloraPosude",
                anchor="w",
                bg="grey",
                font=font_header,
                width=100,
                padx=30,
                pady=5,
            )
            lbl_header.pack(side="top")

            lbl_login = tk.Label(self.frame_login, text="Prijava", font=font_title)
            lbl_login.pack(pady=20)

            lbl_username = tk.Label(
                self.frame_login,
                text="Korisničko ime",
                font=font_header,
            )
            lbl_username.pack()

            self.username = tk.StringVar()
            ent_username = tk.Entry(self.frame_login, textvariable=self.username)
            ent_username.pack(pady=5)

            lbl_password = tk.Label(self.frame_login, text="Lozinka", font=font_header)
            lbl_password.pack()

            self.password = tk.StringVar()
            ent_password = tk.Entry(
                self.frame_login, textvariable=self.password, show="*"
            )
            ent_password.pack(pady=5)

            btn_login = tk.Button(
                self.frame_login, text="Prijavi me", command=self.login
            )
            btn_login.pack(pady=10)

        def create_main_screen(self):
            self.root.geometry("1000x600")

            self.frame_header = tk.Frame(
                self.root, bg="grey", highlightbackground="black", highlightthickness=1
            )
            self.frame_header.columnconfigure((0, 1, 2, 3), weight=1, minsize=100)
            self.frame_header.grid(row=0, column=0, columnspan=4)

            # header
            self.create_header()

            # body
            self.frame_body = tk.Frame(
                self.root,
                highlightbackground="black",
                highlightthickness=1,
            )
            self.frame_body.columnconfigure((0, 1, 2, 3), weight=1, minsize=105)
            self.frame_body.grid(row=1, column=0, columnspan=4)
            btn_sync = tk.Button(
                self.frame_body, text="Sync", font=font_btn, command=sync
            )
            btn_sync.grid(row=1, column=4, padx=5, pady=5, ipadx=5, ipady=5)

            btn_add_pot = tk.Button(
                self.frame_body,
                text="+\nDodaj novu PyPosudu",
                font=font_btn,
                justify="center",
                height=4,
            )
            btn_add_pot.grid(row=2, column=2, padx=5, pady=5)

        def create_profile_screen(self):
            self.clear_body()
            self.users = db_get_users()
            user = self.users[0]  # postoji samo jedan korisnik
            self.user_id = user.id

            lbl_profile = tk.Label(
                self.frame_body,
                text="Uredi korisničke podatke",
                font=font_title,
            )
            lbl_profile.grid(row=1, column=0, columnspan=4, pady=10)

            lbl_name = tk.Label(
                self.frame_body,
                text="Ime",
                font=font_label,
            )
            lbl_name.grid(row=2, column=1)

            self.user_name = tk.StringVar()
            self.user_name.set(user.name)
            ent_name = tk.Entry(self.frame_body, textvariable=self.user_name)
            ent_name.grid(row=3, column=1, padx=10, pady=5)

            lbl_surname = tk.Label(
                self.frame_body,
                text="Prezime",
                font=font_label,
            )
            lbl_surname.grid(row=2, column=2)

            self.user_surname = tk.StringVar()
            self.user_surname.set(user.surname)
            ent_surname = tk.Entry(self.frame_body, textvariable=self.user_surname)
            ent_surname.grid(row=3, column=2, padx=10, pady=5)

            lbl_username = tk.Label(
                self.frame_body,
                text="Korisničko ime",
                font=font_label,
            )
            lbl_username.grid(row=4, column=1)

            self.user_username = tk.StringVar()
            self.user_username.set(user.username)
            ent_username = tk.Entry(self.frame_body, textvariable=self.user_username)
            ent_username.grid(row=5, column=1, padx=10, pady=5)

            lbl_password = tk.Label(self.frame_body, text="Lozinka", font=font_label)
            lbl_password.grid(row=4, column=2)

            self.user_password = tk.StringVar()
            self.user_password.set(user.password)
            ent_password = tk.Entry(
                self.frame_body, textvariable=self.user_password, show="*"
            )
            ent_password.grid(row=5, column=2, padx=10, pady=5)

            btn_save = tk.Button(
                self.frame_body, text="Spremi", font=font_btn, command=self.on_user_save
            )
            btn_save.grid(row=6, column=1, padx=10, pady=5)

            btn_exit = tk.Button(
                self.frame_body,
                text="Odustani",
                font=font_btn,
                command=self.on_user_cancel,
            )
            btn_exit.grid(row=6, column=2, padx=10, pady=5)

        def plant_management(self):
            self.clear_body()

            lbl_plants = tk.Label(
                self.frame_body, text="Dodaj, uredi ili ukloni biljku", font=font_title
            )
            lbl_plants.grid(row=1, column=0, columnspan=4, pady=10)

            btn_add_plant = tk.Button(
                self.frame_body,
                text="Dodaj\nbiljku",
                font=font_btn,
                command=self.on_plant_add,
            )
            btn_add_plant.grid(row=2, column=0, padx=5, pady=5, ipadx=5, ipady=5)
            btn_edit_plant = tk.Button(
                self.frame_body,
                text="Uredi\nbiljke",
                font=font_btn,
                command=self.on_plant_edit,
            )
            btn_edit_plant.grid(row=2, column=1, padx=5, pady=5, ipadx=5, ipady=5)
            btn_delete_plant = tk.Button(
                self.frame_body,
                text="Ukloni\nbiljku",
                font=font_btn,
                command=self.on_plant_delete,
            )
            btn_delete_plant.grid(row=2, column=2, padx=5, pady=5, ipadx=5, ipady=5)
            btn_return = tk.Button(
                self.frame_body,
                text="Povratak",
                font=font_btn,
                command=self.on_user_cancel,
            )
            btn_return.grid(row=2, column=3, padx=5, pady=5, ipadx=5, ipady=5)

        def create_plant_form(self):
            lbl_name = tk.Label(self.frame_body, text="Naziv biljke", font=font_label)
            lbl_name.grid(row=3, column=1)
            self.plant_id = tk.IntVar()
            self.plant_name = tk.StringVar()
            ent_plant_name = tk.Entry(self.frame_body, textvariable=self.plant_name)
            ent_plant_name.grid(row=4, column=1, padx=5, pady=5)

            lbl_photo = tk.Label(self.frame_body, text="Slika", font=font_label)
            lbl_photo.grid(row=5, column=1)
            self.plant_photo = tk.StringVar()
            ent_plant_photo = tk.Entry(self.frame_body, textvariable=self.plant_photo)
            ent_plant_photo.grid(row=6, column=1, padx=5, pady=5)

            lbl_soil_moisture = tk.Label(
                self.frame_body, text="Vlažnost tla", font=font_label
            )
            lbl_soil_moisture.grid(row=7, column=1)
            self.plant_soil_moisture = tk.StringVar()
            ent_plant_soil_moisture = tk.Entry(
                self.frame_body, textvariable=self.plant_soil_moisture
            )
            ent_plant_soil_moisture.grid(row=8, column=1, padx=5, pady=5)

            lbl_ph = tk.Label(self.frame_body, text="pH vrijednost", font=font_label)
            lbl_ph.grid(row=9, column=1)
            self.plant_ph = tk.StringVar()
            ent_plant_ph = tk.Entry(self.frame_body, textvariable=self.plant_ph)
            ent_plant_ph.grid(row=10, column=1, padx=5, pady=5)

            lbl_salinity = tk.Label(self.frame_body, text="Salinitet", font=font_label)
            lbl_salinity.grid(row=3, column=2)
            self.plant_salinity = tk.StringVar()
            ent_plant_salinity = tk.Entry(
                self.frame_body, textvariable=self.plant_salinity
            )
            ent_plant_salinity.grid(row=4, column=2, padx=5, pady=5)

            lbl_light_level = tk.Label(
                self.frame_body, text="Razina svjetlosti", font=font_label
            )
            lbl_light_level.grid(row=5, column=2)
            self.plant_light_level = tk.StringVar()
            ent_plant_light_level = tk.Entry(
                self.frame_body, textvariable=self.plant_light_level
            )
            ent_plant_light_level.grid(row=6, column=2, padx=5, pady=5)

            lbl_temperature = tk.Label(
                self.frame_body, text="Temperatura", font=font_label
            )
            lbl_temperature.grid(row=7, column=2)
            self.plant_temperature = tk.StringVar()
            ent_plant_temperature = tk.Entry(
                self.frame_body, textvariable=self.plant_temperature
            )
            ent_plant_temperature.grid(row=8, column=2, padx=5, pady=5)

            if self.action == "add":
                self.set_default_form_values()

            self.create_plant_buttons()

        def create_plant_buttons(self):
            if self.action != "delete":
                btn_save = tk.Button(
                    self.frame_body,
                    text="Spremi",
                    font=font_btn,
                    command=self.on_plant_save,
                )
                btn_save.grid(row=11, column=1, padx=5, pady=5)
            else:
                btn_delete = tk.Button(
                    self.frame_body,
                    text="Ukloni",
                    font=font_btn,
                    command=self.on_plant_remove,
                )
                btn_delete.grid(row=11, column=1, padx=5, pady=5)

            btn_exit = tk.Button(
                self.frame_body,
                text="Odustani",
                font=font_btn,
                command=self.on_plant_cancel,
            )
            btn_exit.grid(row=11, column=2, padx=5, pady=5)

        def create_drop_down_menu(self):
            self.plants = db_get_plants()
            plant_names = self.get_plant_list()
            self.selected_plant = tk.StringVar()
            drop_menu = ttk.Combobox(
                self.frame_body,
                state="readonly",
                values=plant_names,
                textvariable=self.selected_plant,
            )
            drop_menu.grid(row=2, column=0, columnspan=4, pady=5)
            drop_menu.current()
            drop_menu.bind("<<ComboboxSelected>>", self.callbackFunc)

        def add_plant_page(self):
            self.clear_body()
            self.action = "add"
            lbl_plant = tk.Label(
                self.frame_body, text="Dodaj novu biljku", font=font_title
            )
            lbl_plant.grid(row=1, column=0, columnspan=4, pady=10)
            self.create_plant_form()

        def edit_plant_page(self):
            self.clear_body()
            self.action = "edit"

            lbl_profile = tk.Label(
                self.frame_body,
                text="Uredi podatke o biljkama",
                font=font_title,
            )
            lbl_profile.grid(row=1, column=0, columnspan=4, pady=10)

            self.create_drop_down_menu()
            self.create_plant_form()

        def delete_plant_page(self):
            self.clear_body()
            self.action = "delete"

            lbl_profile = tk.Label(
                self.frame_body,
                text="Ukloni biljku",
                font=font_title,
            )
            lbl_profile.grid(row=1, column=0, columnspan=4, pady=10)

            self.create_drop_down_menu()
            self.create_plant_form()

        # def create_new_pot(self):
        #     self.clear_body()
        #     plants = db_get_plants()

    root = tk.Tk()
    root.title("Py Flora Posude")
    # root.geometry("1000x600")
    py_flora_posude = PyFloraPosude(root)
    root.mainloop()
