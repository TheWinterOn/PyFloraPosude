import tkinter as tk


# temp imports, delete later #TODO
CALIBRI_FONT = "Calibri"
SEGOE_UI_FONT = "Segoe UI"


class PyFloraPosude:
    def __init__(self, root):
        self.root = root
        self.create_login_screen()

    # def login(self):
    #     self.user = db_login(self.username.get(), self.password.get())
    #     if self.user == None:
    #         print("Na postoji korisnik s tim korisnickim imenom i lozinkom.")
    #         return
    #     print(f"Dobro dosli {self.user.name}")
    #     self.clear_root()
    #     self.create_main_screen()

    # def logout(self):
    #     self.clear_root()
    #     self.create_login_screen()

    def create_login_screen(self):
        self.frame_login = tk.Frame(
            self.root, highlightbackground="black", highlightthickness=1
        )
        self.frame_login.pack(fill=tk.BOTH, padx=10, pady=10)

        lbl_header = tk.Label(
            self.frame_login, text="PyFloraPosude", font=(SEGOE_UI_FONT, 14)
        )
        lbl_header.pack()

        lbl_login = tk.Label(self.frame_login, text="Prijava", font=(SEGOE_UI_FONT, 20))
        lbl_login.pack(pady=20)

        lbl_username = tk.Label(
            self.frame_login,
            text="Korisnicko ime",
            font=(SEGOE_UI_FONT, 12),
        )
        lbl_username.pack()

        self.username = tk.StringVar()
        ent_username = tk.Entry(self.frame_login, textvariable=self.username)
        ent_username.pack(pady=5)

        lbl_password = tk.Label(
            self.frame_login, text="Lozinka", font=(SEGOE_UI_FONT, 12)
        )
        lbl_password.pack()

        self.password = tk.StringVar()
        ent_password = tk.Entry(self.frame_login, textvariable=self.password, show="*")
        ent_password.pack(pady=5)

        btn_login = tk.Button(self.frame_login, text="Prijavi me")
        btn_login.pack()


root = tk.Tk()
root.geometry("700x500")
root.title("Py Flora Posude")
py_flora_posude = PyFloraPosude(root)
root.mainloop()
