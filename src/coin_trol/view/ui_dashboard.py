# ui_dashboard.py
import customtkinter as ctk


class DashboardWindow(ctk.CTk):
    def __init__(self, username="TestUser", on_logout=None):
        super().__init__()

        self.username = username
        self.on_logout = on_logout

        self.title("CoinTrol – Dashboard")
        self.geometry("900x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # ---- GRID SETUP ----
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ---- SIDEBAR ----
        sidebar = ctk.CTkFrame(self, width=200, corner_radius=10)
        sidebar.grid(row=0, column=0, sticky="nsw", padx=10, pady=10)

        ctk.CTkLabel(sidebar, text="CoinTrol", font=("Arial", 28)).pack(pady=(20, 10))
        ctk.CTkLabel(sidebar, text=f"User: {username}", font=("Arial", 16)).pack(pady=(0, 20))

        logout_btn = ctk.CTkButton(
            sidebar,
            text="Logout",
            fg_color="#b32d2d",
            command=self.logout
        )
        logout_btn.pack(side="bottom", pady=20)

        # ---- MAIN CONTENT ----
        content = ctk.CTkFrame(self, corner_radius=10)
        content.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        ctk.CTkLabel(content, text="Dashboard Übersicht", font=("Arial", 26)).pack(pady=20)

        # ---- Example Widgets ----
        balance_card = ctk.CTkFrame(content, corner_radius=10)
        balance_card.pack(padx=20, pady=10, fill="x")

        ctk.CTkLabel(balance_card, text="Kontostand", font=("Arial", 20)).pack(pady=5)
        ctk.CTkLabel(balance_card, text="30,00 €", font=("Arial", 35)).pack(pady=10)

    def logout(self):
        print("User logged out.")
        
        if self.on_logout:
            self.destroy()
            self.on_logout()
        else:
            self.destroy()
            print("Logout ohne Rückkehr zum Login.")


# -------------------------------------------
#   TEST AUSFÜHRUNG (GUI hier direkt starten)
# -------------------------------------------

if __name__ == "__main__":
    app = DashboardWindow(username="TestUser")
    app.mainloop()
