"""
main.py
-------
Startpunkt der Anwendung (MVP).
Führt den Login-Prozess aus und öffnet anschließend das Dashboard.
"""

import sys
from PyQt6.QtWidgets import QApplication

# GUI-Module (View)
from coin_trol.view.ui_login import LoginWindow
from coin_trol.view.ui_dashboard import DashboardWindow


# ------------------------------------------------------------
# HAUPTANWENDUNG
# ------------------------------------------------------------
class CoinTrolApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.login_window = None
        self.dashboard_window = None
        self.logged_in_user_id = None  # <-- speichert User-ID nach Login

    def start_login(self):
        """Zeigt das Login-Fenster an."""
        from coin_trol.controller.main_controller import login  # lazy import, um zyklische Abhängigkeiten zu vermeiden

        # LoginWindow erwartet Callback mit (username, user_id)
        self.login_window = LoginWindow(on_login_success=self.start_dashboard)
        self.login_window.show()

    def start_dashboard(self, username: str, user_id: str):
        """Öffnet das Dashboard nach erfolgreichem Login."""
        self.logged_in_user_id = user_id  # <-- speichere User-ID global
        if self.login_window:
            self.login_window.close()

        # Dashboard bekommt sowohl username als auch user_id
        self.dashboard_window = DashboardWindow(
            username=username,
            user_id=user_id,
            on_logout=self.start_login
        )
        self.dashboard_window.show()

    def run(self):
        """Startet die Anwendung."""
        self.start_login()
        sys.exit(self.app.exec())


# ------------------------------------------------------------
# PROGRAMMSTART
# ------------------------------------------------------------
if __name__ == "__main__":
    app = CoinTrolApp()
    app.run()
