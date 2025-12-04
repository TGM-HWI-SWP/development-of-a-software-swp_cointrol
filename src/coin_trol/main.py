
from view.ui_dashboard import DashboardWindow
from view.ui_login import LoginWindow


def start_dashboard(username):
    """Startet das Dashboard und übergibt den Usernamen."""
    app = DashboardWindow(username, on_logout=start_login)
    app.mainloop()

def start_login():
    """Startet den Login-Screen erneut."""
    login = LoginWindow(on_login_success=start_dashboard)
    login.mainloop()

def main():
    start_login()
    start_dashboard()

if __name__ == "__main__":
    main()