import sys  # Für Systemargumente und sauberes Beenden der Anwendung
from PyQt6.QtWidgets import QApplication 
from ui_dashboard import DashboardWindow  
from ui_login import LoginWindow  

app_instance = None        # Globale Referenz auf die QApplication (nur eine erlaubt)
login_window = None        # Globale Referenz auf das Login-Fenster
dashboard_window = None    # Globale Referenz auf das Dashboard-Fenster

def start_dashboard(username): 
    global dashboard_window, login_window  # Zugriff auf globale Fenster-Variablen
    login_window.close()  # Login-Fenster schließen
    dashboard_window = DashboardWindow(username, on_logout=start_login)  # Neues Dashboard erzeugen
    dashboard_window.show()  # Dashboard anzeigen

def start_login():  # Zeigt Login-Fenster an (z. B. nach Logout)
    global login_window, dashboard_window  # Zugriff auf globale Fenster
    if dashboard_window:
        dashboard_window.close()  # Dashboard schließen, falls offen
    login_window = LoginWindow(on_login_success=start_dashboard)  # Neues Login erzeugen
    login_window.show()  # Login anzeigen

def main():  # Hauptstartfunktion für die App
    global app_instance
    app_instance = QApplication(sys.argv)  # PyQt-App initialisieren
    start_login()  # Login anzeigen
    sys.exit(app_instance.exec())  # Eventloop starten und sauber beenden

if __name__ == "__main__":  # Wird nur ausgeführt, wenn Datei direkt gestartet wird
    main()  # Hauptfunktion starten
