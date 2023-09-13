import tkinter as tk
from databases.user_database.user_database import db_login, db_get_users
from sensors.generate_sensor_data import sync


# temp imports, delete later #TODO
CALIBRI_FONT = "Calibri"
font_header = (CALIBRI_FONT, 14)
font_btn = (CALIBRI_FONT, 12)
font_label = (CALIBRI_FONT, 12)


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
            pass

        def on_user_cancel(self):
            self.clear_body()
            self.create_main_screen()

        def clear_root(self):
            for child in self.root.winfo_children():
                child.destroy()

        def clear_body(self):
            for child in self.frame_body.winfo_children():
                child.destroy()

        def create_header(self):
            lbl_app_name = tk.Label(
                self.frame_header,
                text="PyFloraPosude",
                bg="grey",
                font=font_header,
            )
            lbl_app_name.grid(row=0, column=0, padx=10)
            lbl_plants = tk.Label(
                self.frame_header, text="Biljke", bg="grey", font=font_header
            )
            lbl_plants.grid(row=0, column=1, padx=10)
            btn_profile = tk.Button(
                self.frame_header,
                text="Moj profil",
                font=font_btn,
                command=self.create_profile_screen,
            )
            btn_profile.grid(row=0, column=4, padx=5, pady=5)

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

            lbl_login = tk.Label(
                self.frame_login, text="Prijava", font=(CALIBRI_FONT, 20)
            )
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
            self.root.geometry("700x600")

            self.frame_header = tk.Frame(
                self.root, bg="grey", highlightbackground="black", highlightthickness=1
            )
            self.frame_header.grid(row=0, column=0, columnspan=4, sticky=tk.W + tk.E)

            self.frame_header.columnconfigure(0, weight=1)
            self.frame_header.rowconfigure(0, weight=1)

            # header
            self.create_header()

            # body
            self.frame_body = tk.Frame(
                self.root,
                highlightbackground="black",
                highlightthickness=1,
                padx=30,
                pady=5,
            )
            self.frame_body.grid(
                row=1,
                column=0,
                columnspan=4,
                sticky=tk.E + tk.W + tk.N + tk.S,
            )
            btn_sync = tk.Button(self.frame_body, font=font_btn, text="Sync")
            btn_sync.grid(row=1, column=4, padx=5, pady=5)

            self.frame_body.rowconfigure(0, weight=1)
            self.frame_body.columnconfigure(1, weight=1)

        def create_profile_screen(self):
            self.clear_body()
            self.users = db_get_users()
            user = self.users[0]

            lbl_profile = tk.Label(
                self.frame_body,
                text="Uredi korisničke podatke",
                font=(CALIBRI_FONT, 16),
            )
            lbl_profile.grid(row=1, column=0, columnspan=4, pady=10)

            lbl_name = tk.Label(
                self.frame_body,
                text="Ime",
                font=font_label,
            )
            lbl_name.grid(row=2, column=0)

            self.name = tk.StringVar()
            self.name.set(user.name)
            ent_name = tk.Entry(self.frame_body, textvariable=self.name)
            ent_name.grid(row=3, column=0, padx=5, pady=5)

            lbl_surname = tk.Label(
                self.frame_body,
                text="Prezime",
                font=font_label,
            )
            lbl_surname.grid(row=2, column=2)

            self.surname = tk.StringVar()
            self.surname.set(user.surname)
            ent_surname = tk.Entry(self.frame_body, textvariable=self.surname)
            ent_surname.grid(row=3, column=2, padx=5, pady=5)

            lbl_username = tk.Label(
                self.frame_body,
                text="Korisničko ime",
                font=font_label,
            )
            lbl_username.grid(row=4, column=0)

            self.username = tk.StringVar()
            self.username.set(user.username)
            ent_username = tk.Entry(self.frame_body, textvariable=self.username)
            ent_username.grid(row=5, column=0, padx=5, pady=5)

            lbl_password = tk.Label(self.frame_body, text="Lozinka", font=font_label)
            lbl_password.grid(row=4, column=2)

            self.password = tk.StringVar()
            self.password.set(user.password)
            ent_password = tk.Entry(
                self.frame_body, textvariable=self.password, show="*"
            )
            ent_password.grid(row=5, column=2, padx=5, pady=5)

            btn_save = tk.Button(self.frame_body, text="Spremi", font=font_btn, command=self.on_user_save)
            btn_save.grid(row=6, column=0, padx=5, pady=5)

            btn_exit = tk.Button(
                self.frame_body, text="Odustani", font=font_btn, command= self.on_user_cancel)
            btn_exit.grid(row=6, column=2, padx=5, pady=5)

    root = tk.Tk()
    root.title("Py Flora Posude")
    py_flora_posude = PyFloraPosude(root)
    root.mainloop()


