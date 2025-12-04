# ui_login.py
import customtkinter as ctk
from tkinter import messagebox


class LoginWindow(ctk.CTk):
    def __init__(self, on_login_success=None):
        super().__init__()

        # Falls Datei direkt gestartet wird → Dummy-Funktion
        if on_login_success is None:
            on_login_success = self.default_login_success

        self.on_login_success = on_login_success

        self.title("CoinTrol – Login")
        self.geometry("400x350")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # ---- Layout ----
        frame = ctk.CTkFrame(self, corner_radius=15)
        frame.pack(padx=30, pady=30, fill="both", expand=True)

        title = ctk.CTkLabel(frame, text="Login", font=("Arial", 28))
        title.pack(pady=(10, 20))

        self.username_entry = ctk.CTkEntry(frame, placeholder_text="Benutzername")
        self.username_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(frame, placeholder_text="Passwort", show="*")
        self.password_entry.pack(pady=10)

        login_btn = ctk.CTkButton(frame, text="Login", command=self.handle_login)
        login_btn.pack(pady=20)

    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Fehler", "Bitte alle Felder ausfüllen.")
            return

        # Dummy check – später Controller ersetzen
        if username == "test" and password == "1234":
            self.destroy()
            self.on_login_success(username)  # Übergibt Username an Dashboard
        else:
            messagebox.showerror("Fehler", "Falsche Login-Daten!")

    def default_login_success(self, username):
        """Wird benutzt, wenn ui_login.py direkt gestartet wird."""
        print(f"Login erfolgreich! (User: {username})")
        print("Aber kein Dashboard definiert.")
        print("Starte stattdessen nur Login Testmodus.")


# -------------------------------------------------
#   DIREKT AUSBAR — Nur zu Testzwecken!
# -------------------------------------------------
if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()
