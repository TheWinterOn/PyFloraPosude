import tkinter as tk
from databases.user_database.user_database import db_login
from sensors.generate_sensor_data import sync, delete

# temp imports, delete later #TODO
CALIBRI_FONT = "Calibri"


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

        def clear_root(self):
            for child in self.root.winfo_children():
                child.destroy()

        def create_login_screen(self):
            root.geometry("500x300")
            self.frame_login = tk.Frame(
                self.root, highlightbackground="black", highlightthickness=1
            )
            self.frame_login.pack(fill=tk.BOTH, padx=10, pady=10)

            lbl_header = tk.Label(
                self.frame_login, text="PyFloraPosude", font=(CALIBRI_FONT, 14)
            )
            lbl_header.pack()

            lbl_login = tk.Label(
                self.frame_login, text="Prijava", font=(CALIBRI_FONT, 20)
            )
            lbl_login.pack(pady=20)

            lbl_username = tk.Label(
                self.frame_login,
                text="Korisničko ime",
                font=(CALIBRI_FONT, 12),
            )
            lbl_username.pack()

            self.username = tk.StringVar()
            ent_username = tk.Entry(self.frame_login, textvariable=self.username)
            ent_username.pack(pady=5)

            lbl_password = tk.Label(
                self.frame_login, text="Lozinka", font=(CALIBRI_FONT, 12)
            )
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
            root.geometry("700x600")
            self.frame_main_screen = tk.Frame(
                self.root, highlightbackground="black", highlightthickness=1
            )
            self.frame_main_screen.pack(fill=tk.BOTH, expand=True)
            btn_sync = tk.Button(self.frame_main_screen, text="SYNC", command=sync)
            btn_sync.pack(side="right", pady=10)

            btn_delete = tk.Button(
                self.frame_main_screen, text="Delete", command=delete
            )
            btn_delete.pack(side="right", pady=10)

    root = tk.Tk()
    root.title("Py Flora Posude")
    py_flora_posude = PyFloraPosude(root)
    root.mainloop()
