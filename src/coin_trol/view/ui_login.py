"""
ui_login.py
-----------
Dieses Modul enthält das Login- und Registrierungsfenster der App "CoinTrol".
Es ist das Einstiegspunkt-GUI-Fenster der Anwendung.

Hauptfunktionen:
- Benutzer kann sich anmelden (Login)
- oder einen neuen Account erstellen (Registrierung)
- Verbindung mit der Datenbank über den Controller
- Popup-Fenster wurden durch eine Statusleiste ersetzt
"""


# BENÖTIGTE IMPORTS

from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton,
    QFrame, QHBoxLayout, QStatusBar
)
from PyQt6.QtGui import QFont, QColor, QPalette
from PyQt6.QtCore import Qt

# Controller und Model werden importiert
from coin_trol.controller.main_controller import login       # Login-Funktion (Überprüfung gegen DB)
from coin_trol.model.db_interface import create_user         # Neue Benutzererstellung (DB-Eintrag)


# KLASSE: LoginWindow

class LoginWindow(QWidget):
    """
    Fenster für Anmeldung und Registrierung.
    Wechselt dynamisch zwischen Login- und Registriermodus.
    """

    def __init__(self, on_login_success=None):
        """
        Initialisiert das Login-Fenster.
        :param on_login_success: Callback-Funktion, die beim erfolgreichen Login aufgerufen wird.
        """
        super().__init__()  # Basisklasse QWidget initialisieren

        # Übergabeparameter speichern
        self.on_login_success = on_login_success  # Callback an Main
        self.is_register_mode = False             # Start im Login-Modus (nicht Registrierung)

        
        # Fenster-Eigenschaften
        
        self.setWindowTitle("CoinTrol – Login / Registrierung")  # Fenstertitel oben
        self.resize(480, 520)  # Fenstergröße

        
        # Hintergrundfarbe einstellen (Dark Mode)
        
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#1E1F26"))  # Dunkles Grau/Blau
        self.setPalette(palette)

        
        # Hauptlayout erstellen
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(40, 40, 40, 40)
        self.layout.setSpacing(25)

        # Benutzeroberfläche aufbauen
        self._build_ui()

    
    # GUI-AUFBAU
    
    def _build_ui(self):
        """Erstellt alle sichtbaren GUI-Elemente."""
        # Rahmen (Container für Eingabefelder und Buttons)
        self.frame = QFrame()
        self.frame.setStyleSheet("background-color: #2A2B31; border-radius: 16px;")
        frame_layout = QVBoxLayout(self.frame)
        frame_layout.setContentsMargins(30, 30, 30, 30)
        frame_layout.setSpacing(20)

        
        # TITEL (oben)
        
        self.title = QLabel("Anmeldung")
        self.title.setFont(QFont("Arial Black", 26))
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("color: white;")
        frame_layout.addWidget(self.title)

        
        # BENUTZERNAME
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Benutzername")  # Platzhaltertext
        self._style_input(self.username_input)
        frame_layout.addWidget(self.username_input)

        
        # E-MAIL (nur bei Registrierung sichtbar)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("E-Mail-Adresse")
        self._style_input(self.email_input)
        self.email_input.hide()  # versteckt, da Login-Modus Standard ist
        frame_layout.addWidget(self.email_input)

        
        # PASSWORT
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Passwort")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)  # versteckte Eingabe
        self._style_input(self.password_input)
        frame_layout.addWidget(self.password_input)

        
        # PASSWORT BESTÄTIGEN (nur bei Registrierung sichtbar)
        
        self.password_confirm_input = QLineEdit()
        self.password_confirm_input.setPlaceholderText("Passwort bestätigen")
        self.password_confirm_input.setEchoMode(QLineEdit.EchoMode.Password)
        self._style_input(self.password_confirm_input)
        self.password_confirm_input.hide()  # standardmäßig unsichtbar
        frame_layout.addWidget(self.password_confirm_input)

        
        # HAUPT-AKTIONSBUTTON (Login/Registrieren)
        
        self.action_btn = QPushButton("Einloggen")
        self.action_btn.setFixedHeight(45)
        self._style_button(self.action_btn, "#5B5CF0", "#6D6EFA")  # Farbschema Blau/Violett
        self.action_btn.clicked.connect(self._handle_action)
        frame_layout.addWidget(self.action_btn)

        
        # MODUS-UMSCHALTER (Login ↔ Registrierung)
        
        toggle_layout = QHBoxLayout()
        toggle_label = QLabel("Noch kein Konto?")
        toggle_label.setStyleSheet("color: #CCCCCC; font-size: 15px;")

        toggle_btn = QPushButton("Registrieren")
        toggle_btn.setStyleSheet("""
            QPushButton {
                background: none;
                color: #5B5CF0;
                border: none;
                font-size: 15px;
                text-decoration: underline;
            }
            QPushButton:hover { color: #7777FF; }
        """)
        toggle_btn.clicked.connect(self._toggle_mode)  # wechselt Modus
        toggle_layout.addWidget(toggle_label)
        toggle_layout.addWidget(toggle_btn)
        toggle_layout.addStretch()
        frame_layout.addLayout(toggle_layout)

        # Frame ins Hauptlayout einfügen
        self.layout.addWidget(self.frame)

        
        # STATUSLEISTE (unten statt Popups)
        
        self.status_bar = QStatusBar()
        self.status_bar.setStyleSheet("color: white; background-color: #1E1F26; border-radius: 6px; padding: 3px;")
        self.status_bar.showMessage("Bereit.")
        self.layout.addWidget(self.status_bar)

    
    # LOGIN / REGISTRIERUNG – LOGIK
    
    def _handle_action(self):
        """Verarbeitet Login oder Registrierung, abhängig vom Modus."""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        
        # LOGIN
        
        if not self.is_register_mode:
            # Eingaben prüfen
            if not username or not password:
                self.status_bar.showMessage("Fehler: Bitte Benutzername und Passwort eingeben.")
                return

            # Login über Controller prüfen
            user_id = login(username, password)
            if user_id:
                self.status_bar.showMessage(f"Erfolg: Willkommen, {username}!")
                if self.on_login_success:
                    # Wenn Login erfolgreich → Dashboard öffnen
                    self.on_login_success(username, user_id)
                self.close()  # Login-Fenster schließen
            else:
                self.status_bar.showMessage("Fehler: Ungültige Anmeldedaten.")

        
        # REGISTRIERUNG
        
        else:
            email = self.email_input.text().strip()
            password_confirm = self.password_confirm_input.text().strip()

            # Pflichtfelder prüfen
            if not username or not email or not password or not password_confirm:
                self.status_bar.showMessage("Fehler: Bitte alle Felder ausfüllen.")
                return

            # Passwortübereinstimmung prüfen
            if password != password_confirm:
                self.status_bar.showMessage("Fehler: Passwörter stimmen nicht überein.")
                return

            try:
                # Benutzer in der Datenbank anlegen
                new_user_id = create_user(username, email, password)
                self.status_bar.showMessage(f"Nutzer '{username}' erfolgreich erstellt! (ID: {new_user_id})")

                # Nach erfolgreicher Registrierung → zurück zum Login
                self._toggle_mode()
                self.username_input.setText(username)
                self.password_input.clear()
                self.email_input.clear()
                self.password_confirm_input.clear()

            except Exception as e:
                self.status_bar.showMessage(f"Fehler: Registrierung fehlgeschlagen ({e})")

    
    # MODUS WECHSELN (LOGIN <-> REGISTRIERUNG)
    
    def _toggle_mode(self):
        """Wechselt zwischen Login- und Registriermodus."""
        self.is_register_mode = not self.is_register_mode

        
        # REGISTRIERUNGSMODUS
        
        if self.is_register_mode:
            self.title.setText("Registrierung")             # Titel anpassen
            self.email_input.show()                         # E-Mail anzeigen
            self.password_confirm_input.show()              # Passwort-Bestätigung anzeigen
            self.action_btn.setText("Registrieren")         # Buttontext ändern
            self.status_bar.showMessage("Registrierungsmodus aktiviert.")
        else:
            
            # LOGINMODUS
            
            self.title.setText("Anmeldung")                 # Titel zurücksetzen
            self.email_input.hide()                         # E-Mail-Feld verstecken
            self.password_confirm_input.hide()              # Passwortbestätigung ausblenden
            self.action_btn.setText("Einloggen")            # Buttontext zurücksetzen
            self.status_bar.showMessage("Loginmodus aktiviert.")

    
    # STYLING-HILFSMETHODEN
    
    def _style_input(self, widget):
        """Standard-Styling für Eingabefelder."""
        widget.setFixedHeight(42)
        widget.setStyleSheet("""
            QLineEdit {
                background-color: #3A3B42;
                color: white;
                border-radius: 8px;
                padding-left: 12px;
                font-size: 16px;
            }
        """)

    def _style_button(self, button, color_normal, color_hover):
        """Standard-Styling für Buttons."""
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color_normal};
                color: white;
                font-size: 18px;
                border-radius: 10px;
            }}
            QPushButton:hover {{
                background-color: {color_hover};
            }}
        """)



# TESTSTART (Nur für direkten Start)

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    win = LoginWindow()
    win.show()
    sys.exit(app.exec())