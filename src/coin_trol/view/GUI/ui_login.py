import customtkinter as ctk
from view.data.user_storage import UserStorage
from view.GUI.ui_dashboard import DashboardWindow


class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("CoinTrol Login / Register")
        self.geometry("500x550")

        self.frame = ctk.CTkFrame(self)
        self.frame.pack(fill="both", expand=True)

        self.title_label = ctk.CTkLabel(self.frame, text="Login", font=("Arial", 28))
        self.title_label.pack(pady=20)

        btn_frame = ctk.CTkFrame(self.frame)
        btn_frame.pack(pady=10)

        ctk.CTkButton(btn_frame, text="Login", command=self.show_login).grid(row=0, column=0, padx=10)
        ctk.CTkButton(btn_frame, text="Registrieren", command=self.show_register).grid(row=0, column=1, padx=10)

        self.message = ctk.CTkLabel(self.frame, text="", text_color="red")
        self.message.pack(pady=10)

        self.username = ctk.CTkEntry(self.frame, placeholder_text="Username")
        self.username.pack(pady=10)

        self.password = ctk.CTkEntry(self.frame, placeholder_text="Password", show="*")
        self.password.pack(pady=10)

        self.password_repeat = ctk.CTkEntry(self.frame, placeholder_text="Passwort wiederholen", show="*")

        self.action_btn = ctk.CTkButton(self.frame, text="Login", command=self.handle_login)
        self.action_btn.pack(pady=20)

        self.current_mode = "login"


    def show_login(self):
        self.current_mode = "login"
        self.title_label.configure(text="Login")
        self.message.configure(text="")

        self.password_repeat.pack_forget()
        self.username.pack(pady=10)
        self.password.pack(pady=10)

        self.action_btn.configure(text="Login", command=self.handle_login)

        # <<< WICHTIG für Logout
        self.frame.pack(fill="both", expand=True)


    def show_register(self):
        self.current_mode = "register"
        self.title_label.configure(text="Registrieren")
        self.message.configure(text="")

        self.username.pack(pady=10)
        self.password.pack(pady=10)
        self.password_repeat.pack(pady=10)

        self.action_btn.configure(text="Registrieren", command=self.handle_register)

        self.frame.pack(fill="both", expand=True)


    def handle_login(self):
        user = self.username.get()
        pw = self.password.get()

        if UserStorage.validate_login(user, pw):
            self.frame.pack_forget()
            dashboard = DashboardWindow(self, user)
            dashboard.pack(fill="both", expand=True)
        else:
            self.message.configure(text="Falsche Login-Daten!", text_color="red")


    def handle_register(self):
        user = self.username.get()
        pw1 = self.password.get()
        pw2 = self.password_repeat.get()

        if not user or not pw1 or not pw2:
            self.message.configure(text="Bitte alle Felder ausfüllen!")
            return

        if pw1 != pw2:
            self.message.configure(text="Passwörter stimmen nicht überein!")
            return

        if UserStorage.register_user(user, pw1):
            self.message.configure(text="Registriert! Du kannst dich jetzt einloggen.", text_color="green")
            self.show_login()
        else:
            self.message.configure(text="Benutzer existiert bereits!", text_color="red")


    def run(self):
        self.mainloop()
