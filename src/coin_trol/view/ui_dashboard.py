from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QGridLayout, QFrame
)
from PyQt6.QtGui import QFont, QColor, QPalette
from PyQt6.QtCore import Qt
import sys

# WICHTIG: Importiere dein Transaktionsfenster
from Transaktion import TransactionWindow   # Importiert das Fenster für Transaktionen
from Wallets import WalletsWindow           # Importiert das Fenster für Wallets


class DashboardWindow(QWidget):
    def __init__(self, username="TestUser", on_logout=None):
        super().__init__()

        self.username = username                     # Speichert den Benutzernamen
        self.on_logout = on_logout                   # Callback-Funktion für Logout
        self.trans_window = None                     # Platzhalter für Transaktionsfenster

        # Fenster Setup
        self.setWindowTitle("CoinTrol – Dashboard")  # Titel des Fensters
        self.resize(1280, 800)                       # Fenstergröße setzen

        # Hintergrundfarbe
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#262626"))  # Hintergrundfarbe
        self.setPalette(palette)

        SIDEBAR_BG = "#1E1F26"   # Sidebar-Farbe
        CARD_BG = "#3A3A42"      # Kartenfarbe im Dashboard

        # ---------------------------------------------------
        # HAUPTLAYOUT
        # ---------------------------------------------------
        main_layout = QHBoxLayout(self)              # Horizontaler Aufbau: Sidebar links, Content rechts
        main_layout.setContentsMargins(10, 10, 10, 10)  # Außenabstand des Layouts
        main_layout.setSpacing(15)                      # Abstand zwischen Sidebar und Content

        # ---------------------------------------------------
        # SIDEBAR
        # ---------------------------------------------------
        sidebar = QFrame()                            # Linker Container für Navigation
        sidebar.setFixedWidth(240)                    # Sidebar Breite
        sidebar.setStyleSheet(f"background-color: {SIDEBAR_BG}; border-radius: 14px;")  # Sidebar-Design

        side_layout = QVBoxLayout(sidebar)            # Vertikales Layout für Sidebar
        side_layout.setContentsMargins(20, 20, 20, 20)
        side_layout.setSpacing(40)

        title = QLabel("CoinTrol")                    # Überschrift
        title.setFont(QFont("Arial", 36, QFont.Weight.Bold))  # Schriftgröße
        title.setStyleSheet("color: white;")
        side_layout.addWidget(title)

        user_label = QLabel(f"Angemeldet als:\n{username}")   # Benutzerinfo
        user_label.setFont(QFont("Arial", 16))
        user_label.setStyleSheet("color: #CFCFCF;")
        side_layout.addWidget(user_label)

        side_layout.addSpacing(20)                    # Extra Abstand

        # --------------------------------------------------------
        # BUTTON-MAPPING
        # --------------------------------------------------------
        buttons = {
            "Dashboard": None,                        # Kein Click-Event
            "Transaktionen": self.open_transactions,  # Öffnet Transaktionsfenster
            "Wallets": self.open_wallet,              # Öffnet Walletfenster
        }

        for name, action in buttons.items():          # Jede Schaltfläche erzeugen
            btn = QPushButton(name)
            btn.setFixedHeight(65)                    # Einheitliche Höhe
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #2E2E36;
                    color: white;
                    font-size: 20px;
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background-color: #3A3A48;
                }
            """)
            if action is not None:                    # Click-Event nur wenn vorhanden
                btn.clicked.connect(action)
            side_layout.addWidget(btn)

        side_layout.addStretch()                      # Füllt verbleibenden Platz

        logout_btn = QPushButton("Logout")            # Logout Button
        logout_btn.setFixedHeight(45)
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #C13535;
                color: white;
                font-size: 17px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #D64242;
            }
        """)
        logout_btn.clicked.connect(self.logout)       # Logout Event
        side_layout.addWidget(logout_btn)

        main_layout.addWidget(sidebar)                # Sidebar in Hauptlayout einsetzen

        # ---------------------------------------------------
        # CONTENT-BEREICH
        # ---------------------------------------------------
        content = QFrame()                            # Rechter Content-Bereich
        content.setStyleSheet("background-color: #2B2B2B; border-radius: 18px;")

        content_layout = QVBoxLayout(content)         # Vertikale Anordnung des Inhalts
        content_layout.setContentsMargins(30, 30, 30, 30)
        content_layout.setSpacing(20)

        # HEADER
        header = QLabel("Dashboard Übersicht")        # Überschrift für Content
        header.setFont(QFont("Arial", 34, QFont.Weight.Bold))
        header.setStyleSheet("color: white;")
        header.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        content_layout.addWidget(header)

        # STATISTIK-KARTEN
        grid = QGridLayout()                          # Rasterlayout für drei Karten
        grid.setSpacing(20)

        cards = [
            ("Kontostand", "30,00 €"),
            ("Monatsausgaben", "91,40 €"),
            ("Einnahmen", "120,00 €"),
        ]

        for i, (title_text, value_text) in enumerate(cards):  # Jede Karte erzeugen
             # enumerate liefert den Index (i) und das Element (Titel, Wert) jeder Karte
            card = QFrame()
            card.setStyleSheet(f"""
                background-color: {CARD_BG};
                border-radius: 18px;
            """)
            card_layout = QVBoxLayout(card)
            card_layout.setSpacing(5)
            card_layout.setContentsMargins(20, 20, 20, 20)

            t = QLabel(title_text)                   # Titel der Karte
            t.setFont(QFont("Arial", 22))
            t.setStyleSheet("color: #D0D0D0;")
            t.setAlignment(Qt.AlignmentFlag.AlignHCenter)

            v = QLabel(value_text)                   # Wert der Karte
            v.setFont(QFont("Arial", 42, QFont.Weight.Bold))
            v.setStyleSheet("color: white;")
            v.setAlignment(Qt.AlignmentFlag.AlignHCenter)

            card_layout.addWidget(t)
            card_layout.addWidget(v)

            grid.addWidget(card, 0, i)               # Reihen 0, Spalten 0–2

        content_layout.addLayout(grid)

        # LETZTE AKTIVITÄTEN
        info_card = QFrame()                          # Rahmen für Aktivitätenliste
        info_card.setStyleSheet(f"background-color: {CARD_BG}; border-radius: 18px;") # CARD_BG ist die zuvor definierte Hintergrundfarbe für Karten (z. B. #3A3A42)

        info_layout = QVBoxLayout(info_card)
        info_layout.setContentsMargins(25, 25, 25, 25)

        header2 = QLabel("Letzte Aktivitäten")        # Titel Liste
        header2.setFont(QFont("Arial", 26, QFont.Weight.Bold))
        header2.setStyleSheet("color: white;")
        info_layout.addWidget(header2)

        activities = QLabel("• 15 € – McDonalds\n• 8 € – Öffi Ticket\n• 120 € – Gehalt")
        activities.setFont(QFont("Arial", 20))
        activities.setStyleSheet("color: #DDDDDD;")
        info_layout.addWidget(activities)

        content_layout.addWidget(info_card)

        main_layout.addWidget(content)                 # Content ins Hauptlayout

    # ------------------------------------------------------------
    # TRANSAKTIONS-FENSTER ÖFFNEN
    # ------------------------------------------------------------
    def open_transactions(self):
        self.trans_window = TransactionWindow()        # Neue Instanz des Transaktionsfensters
        self.trans_window.show()                       # Fenster anzeigen

    def open_wallet(self):
        self.wallet_window = WalletsWindow()           # Neue Instanz des Wallet-Fensters
        self.wallet_window.show()                      # Fenster anzeigen

    # ------------------------------------------------------------
    # LOGOUT
    # ------------------------------------------------------------
    def logout(self):
        if self.on_logout:                             # Callback nur ausführen, wenn vorhanden
            self.on_logout()
        self.close()                                   # Fenster schließen


# ------------------------------------------------------------
# Direktstart für Tests
# ------------------------------------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)                      # PyQt App starten
    win = DashboardWindow("TestUser")                 # Dashboard erstellen
    win.show()                                        # Anzeigen
    sys.exit(app.exec())                              # Eventloop starten
