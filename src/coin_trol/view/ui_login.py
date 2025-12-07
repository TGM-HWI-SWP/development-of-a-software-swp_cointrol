from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QFrame, QApplication, QMessageBox, QDialog
)
from PyQt6.QtGui import QFont, QColor, QPalette
from PyQt6.QtCore import Qt
import sys


# ------------------------------------------------------------
# Hover-Effekt (vergrößert Buttons leicht)
# Diese Funktion definiert zwei Stylesheets: Normal & Hover.
# Hover-Effekt wird später in Buttons eingesetzt.
# ------------------------------------------------------------
def apply_hover(button):
    normal = """
        QPushButton {
            background-color: #5B5CF0;
            color: white;
            border-radius: 12px;
            font-size: 18px;
            padding: 10px;
        }
    """
    hover = """
        QPushButton {
            background-color: #6D6EFA;
            color: white;
            border-radius: 12px;
            font-size: 18px;
            padding: 10px;
        }
    """

    # Setzt nur den normalen Style.
    #  funktioniert hier nur, wenn über Stylesheet definiert.
    button.setStyleSheet(normal)



# ------------------------------------------------------------
# LOGIN-FENSTER (PyQt6)
# Hauptklasse für das Login-Fenster.
# ------------------------------------------------------------
class LoginWindow(QWidget):
    def __init__(self, on_login_success=None, on_register_user=None):
        super().__init__()

        # Delegates – werden verwendet, falls keine Funktionen übergeben wurden
        self.on_login_success = on_login_success or self.default_login_success
        self.on_register_user = on_register_user or self.default_register_user

        # Fenster Einstellungen
        self.setWindowTitle("CoinTrol – Login")
        self.resize(520, 560)

        # Hintergrundfarbe des Fensters setzen
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#2B2B2B"))
        self.setPalette(palette)

        # Farbvariablen für spätere Styles
        BG_CARD = "#36363C"
        TEXT_GRAY = "#CACACA"
        ACCENT = "#5B5CF0"

        # Hauptlayout
        main = QVBoxLayout(self)
        main.setContentsMargins(60, 40, 60, 40)

        # Card Frame (optisch hervorgehobener Container)
        card = QFrame()
        card.setStyleSheet(f"background-color: {BG_CARD}; border-radius: 20px;")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(30, 30, 30, 30) # Innenabstand im Layout: links, oben, rechts, unten (je 30px)
        card_layout.setSpacing(18)

        # Titel
        title = QLabel("Willkommen bei CoinTrol")
        title.setFont(QFont("Arial", 26, QFont.Weight.Bold))
        title.setStyleSheet("color: white;")
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter)  # Zentriert den Text horizontal innerhalb des Labels
        card_layout.addWidget(title)

        # Untertitel
        subtitle = QLabel("Bitte logge dich ein")
        subtitle.setFont(QFont("Arial", 14))
        subtitle.setStyleSheet(f"color: {TEXT_GRAY};")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignHCenter)  # Zentriert den Text horizontal innerhalb des Labels
        card_layout.addWidget(subtitle)

        # Benutzername Eingabefeld
        self.username_entry = QLineEdit()
        self.username_entry.setPlaceholderText("Benutzername")
        self.username_entry.setFixedHeight(45)
        self._style_input(self.username_entry)
        card_layout.addWidget(self.username_entry)

        # Passwort Eingabefeld (versteckt Eingabe)
        self.password_entry = QLineEdit()
        self.password_entry.setPlaceholderText("Passwort")
        self.password_entry.setEchoMode(QLineEdit.EchoMode.Password)  # Versteckt die Eingabe, indem sie als •• angezeigt wird
        self.password_entry.setFixedHeight(45)
        self._style_input(self.password_entry)
        card_layout.addWidget(self.password_entry)

        # Login Button
        login_btn = QPushButton("Login")
        login_btn.setFixedHeight(45)
        apply_hover(login_btn)  # Hover Style anwenden
        login_btn.clicked.connect(self.handle_login)  # Login-Click-Handler
        card_layout.addWidget(login_btn)

        # Registrieren Button – öffnet Pop-Up
        register_btn = QPushButton("Registrieren")
        register_btn.setFixedHeight(45)
        register_btn.setStyleSheet("""
            QPushButton {
                background-color: #2C2C3A;
                color: white;
                border-radius: 12px;
                font-size: 18px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #3A3A4A;
            }
        """)
        register_btn.clicked.connect(self.open_register_window)
        card_layout.addWidget(register_btn)

        main.addWidget(card)



    # ------------------------------------------------------------
    # Styling Funktion für Eingabefelder
    # ------------------------------------------------------------
    def _style_input(self, widget):
        widget.setStyleSheet("""
            QLineEdit {
                background-color: #2B2C31;
                color: white;
                border-radius: 10px;
                padding-left: 12px;
                font-size: 16px;
            }
        """)



    # ------------------------------------------------------------
    # LOGIN LOGIK
    # Einfacher Test-Login mit statischen Werten.
    # ------------------------------------------------------------
    def handle_login(self):
        username = self.username_entry.text()
        password = self.password_entry.text()

        # Prüft, ob beide Felder ausgefüllt wurden
        if not username or not password:
            QMessageBox.warning(self, "Fehler", "Bitte alle Felder ausfüllen.")
            return

        # Beispiel-Login für Tests
        if username == "test" and password == "1234":
            self.close()
            self.on_login_success(username)  # Callback
        else:
            QMessageBox.critical(self, "Fehler", "Falsche Login-Daten!")



    # ------------------------------------------------------------
    # REGISTRIERUNG (Popup)
    # Öffnet ein eigenes Fenster für Registrierung.
    # ------------------------------------------------------------
    def open_register_window(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Registrieren")
        dialog.resize(520, 620)

        # Hintergrundfarbe auch hier setzen
        palette = dialog.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#2B2B2B"))
        dialog.setPalette(palette)

        BG_CARD = "#36363C"

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(40, 40, 40, 40)

        # Card Container
        card = QFrame()
        card.setStyleSheet(f"background-color: {BG_CARD}; border-radius: 20px;")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(25, 25, 25, 25)  # Innenabstand des Card-Layouts: links, oben, rechts, unten jeweils 25px
        card_layout.setSpacing(12)

        # Titel
        title = QLabel("Neuen Benutzer anlegen")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setStyleSheet("color: white;")
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        card_layout.addWidget(title)

        subtitle = QLabel("Bitte alle Felder ausfüllen")
        subtitle.setFont(QFont("Arial", 14))
        subtitle.setStyleSheet("color: gray;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        card_layout.addWidget(subtitle)

        # Erstelle die Felder für die Registrierung
        labels = ["Vorname", "Nachname", "E-Mail", "Benutzername", "Passwort", "Passwort wiederholen"]
        fields = []

        # Jedes Eingabefeld erstellen
        for text in labels:
            entry = QLineEdit()
            entry.setPlaceholderText(text)
            entry.setFixedHeight(40)
            self._style_input(entry)
            fields.append(entry)
            card_layout.addWidget(entry)

        # Passwort & Passwort-Wiederholung
        pw, pw2 = fields[-2], fields[-1] # Nimmt aus der Liste 'fields' die letzten zwei Einträge: Passwort und Passwort-Wiederholung

        # Registrieren Button
        save_btn = QPushButton("Registrieren")
        apply_hover(save_btn)
        save_btn.setFixedHeight(45)

        # Interne Funktion: Registrierungsvalidierung
        def submit():
            # Prüft, ob alle Felder ausgefüllt sind
            if not all(e.text() for e in fields): # Prüft, ob mindestens ein Eingabefeld leer ist (alle Felder müssen Text haben)
                QMessageBox.warning(dialog, "Fehler", "Bitte alle Felder ausfüllen.")
                return

            # Passwort-Abgleich
            if pw.text() != pw2.text():
                QMessageBox.warning(dialog, "Fehler", "Passwörter stimmen nicht überein.")
                return

            # Callback für Registrierung
            result = self.on_register_user(
                fields[0].text(), fields[1].text(),
                fields[2].text(), fields[3].text(), pw.text()
            )

            # Ergebnis prüfen
            if result is True:
                QMessageBox.information(dialog, "Erfolg", "Benutzer erfolgreich registriert.")
                dialog.close()
            else:
                QMessageBox.critical(dialog, "Fehler", str(result))

        save_btn.clicked.connect(submit)
        card_layout.addWidget(save_btn)

        layout.addWidget(card)
        dialog.exec()



    # ------------------------------------------------------------
    # Standard-Callbacks für Tests
    # Werden genutzt, wenn keine echten Funktionen übergeben wurden.
    # ------------------------------------------------------------
    def default_login_success(self, username):
        print(" Login erfolgreich:", username) # gibt Erfolgsmeldung in der Konsole aus          

    def default_register_user(self, firstname, lastname, email, username, password):
        print(" Registrieren:", firstname, lastname, email, username) 
        return True  # Meldet erfolgreiches Registrieren zurück 



# ------------------------------------------------------------
# START DES PROGRAMMS
# ------------------------------------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)      # Startet die PyQt-Anwendung und verarbeitet Kommandozeilenargumente
    win = LoginWindow()               # Erstellt das Login-Fenster
    win.show()                        # Zeigt das Fenster sichtbar an
    sys.exit(app.exec())              # Startet die Qt-Eventschleife und beendet das Programm korrekt nach Schließen

