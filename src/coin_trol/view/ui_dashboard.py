"""
ui_dashboard.py
---------------
Dieses Modul enthält das Dashboard-Fenster von CoinTrol.
Es zeigt:
 - den aktuellen Benutzer
 - seine Wallets und Transaktionen
 - sowie eine Übersicht über Einnahmen/Ausgaben.

Von hier kann der Benutzer:
 - neue Transaktionen hinzufügen,
 - Wallets anzeigen,
 - und sich ausloggen.
"""


# BENÖTIGTE PYQT-IMPORTS

from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QGridLayout, QFrame, QScrollArea
)
from PyQt6.QtGui import QFont, QColor, QPalette
from PyQt6.QtCore import Qt
import sys


# IMPORTS AUS ANDEREN TEILEN DER APP (MODEL & VIEW)

# Diese Funktionen kommunizieren mit der Datenbank (MongoDB)
from coin_trol.model.db_interface import (
    get_wallets_by_user,          # Gibt alle Wallets eines Benutzers zurück
    create_wallet,                # Erstellt ein neues Wallet in der DB
    calculate_wallet_balance,     # Berechnet den Kontostand eines Wallets
    get_transactions_by_wallet    # Holt alle Transaktionen zu einem Wallet
)
# Import weiterer GUI-Fenster (andere Views)
from coin_trol.view.Transaktion import TransactionWindow
from coin_trol.view.Wallets import WalletsWindow



# KLASSE: DashboardWindow

class DashboardWindow(QWidget):
    """
    Hauptfenster der CoinTrol-App nach erfolgreichem Login.
    Zeigt eine Übersicht aller relevanten Finanzdaten des Benutzers an.
    """

    def __init__(self, username="TestUser", on_logout=None, user_id=None):
        """
        Konstruktor – erstellt das Dashboard-Fenster.

        :param username: Name des eingeloggten Benutzers (wird im Dashboard angezeigt)
        :param on_logout: Funktion, die beim Klick auf "Logout" aufgerufen wird
        :param user_id: Eindeutige Benutzer-ID (MongoDB)
        """
        super().__init__()  # Basisklasse initialisieren

        
        # BENUTZERDATEN
        
        self.username = username        # z. B. "Gabriel"
        self.user_id = user_id          # MongoDB-ID des Users
        self.on_logout = on_logout      # Callback für Logout
        self.wallet_id = None           # aktuelle Wallet-ID (wird später gesetzt)

        
        # FENSTERKONFIGURATION
        
        self.setWindowTitle("CoinTrol – Dashboard")  # Fenstertitel oben
        self.resize(1280, 800)                       # Standardgröße des Dashboards

        # Hintergrundfarbe des Fensters setzen (dunkles Theme)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#262626"))  # dunkles Grau
        self.setPalette(palette)

        
        # DESIGNFARBEN FÜR SPÄTERE ELEMENTE
        
        SIDEBAR_BG = "#1E1F26"  # linke Navigationsleiste
        CARD_BG = "#3A3A42"     # Hintergrundfarbe der Infokarten

        
        # HAUPTLAYOUT DES FENSTERS
        
        # Hauptlayout besteht aus 2 Spalten → Sidebar links, Inhalt rechts
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)  # äußerer Rand
        main_layout.setSpacing(15)                      # Abstand zwischen Sidebar und Inhalt

        
        # LINKER BEREICH: SIDEBAR (Navigation)
        
        sidebar = QFrame()  # Container für die Sidebar
        sidebar.setFixedWidth(240)  # feste Breite
        sidebar.setStyleSheet(f"background-color: {SIDEBAR_BG}; border-radius: 14px;")

        # Vertikales Layout für Sidebar
        side_layout = QVBoxLayout(sidebar)
        side_layout.setContentsMargins(20, 20, 20, 20)
        side_layout.setSpacing(40)

        # Titel / Logo
        title = QLabel("CoinTrol")
        title.setFont(QFont("Arial", 36, QFont.Weight.Bold))  # große, fette Schrift
        title.setStyleSheet("color: white;")
        side_layout.addWidget(title)

        # Benutzername-Anzeige
        user_label = QLabel(f"Angemeldet als:\n{username}")
        user_label.setFont(QFont("Arial", 16))
        user_label.setStyleSheet("color: #CFCFCF;")  # hellgrauer Text
        side_layout.addWidget(user_label)
        side_layout.addSpacing(20)

        
        # NAVIGATIONSBUTTONS
        
        buttons = {
            "Dashboard": None,                   # Kein Klick nötig (bereits hier)
            "Transaktionen": self.open_transactions,  # öffnet Transaktionsfenster
            "Wallets": self.open_wallet,         # öffnet Wallet-Verwaltung
        }

        # Buttons dynamisch erzeugen
        for name, action in buttons.items():
            btn = QPushButton(name)
            btn.setFixedHeight(65)  # Höhe der Buttons
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #2E2E36;  /* Grundfarbe */
                    color: white;
                    font-size: 20px;
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background-color: #3A3A48;  /* Hover-Farbe */
                }
            """)
            # Wenn Button eine Aktion hat (z. B. open_wallet), wird sie verknüpft
            if action:
                btn.clicked.connect(action)
            side_layout.addWidget(btn)  # Button zur Sidebar hinzufügen

        # Platzhalter → schiebt Logout nach unten
        side_layout.addStretch()

        
        # LOGOUT-BUTTON (unten)
        
        logout_btn = QPushButton("Logout")
        logout_btn.setFixedHeight(45)
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #C13535;  /* Rot: Warn-/Abmeldefarbe */
                color: white;
                font-size: 17px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #D64242;
            }
        """)
        logout_btn.clicked.connect(self.logout)  # Logout-Funktion ausführen
        side_layout.addWidget(logout_btn)

        # Sidebar zum Hauptlayout hinzufügen
        main_layout.addWidget(sidebar)

        
        # RECHTER BEREICH: SCROLLBAR + INHALT
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # passt Größe automatisch an
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Scrollbar-Design
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background: #1E1F26;
                width: 10px;
                margin: 4px 0 4px 0;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #5B5CF0;  /* Akzentfarbe (blau-violett) */
                border-radius: 5px;
                min-height: 25px;
            }
            QScrollBar::handle:vertical:hover {
                background: #7678FF;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0;  /* keine Pfeile anzeigen */
            }
        """)

        
        # INHALTSBEREICH (rechte Seite)
        
        content = QWidget()
        content.setStyleSheet("background-color: #2B2B2B; border-radius: 18px;")

        # Layout für den Content
        self.content_layout = QVBoxLayout(content)
        self.content_layout.setContentsMargins(30, 30, 30, 30)
        self.content_layout.setSpacing(20)

        # Überschrift (Titel)
        header = QLabel("Dashboard Übersicht")
        header.setFont(QFont("Arial", 34, QFont.Weight.Bold))
        header.setStyleSheet("color: white;")
        header.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.content_layout.addWidget(header)

        
        # Daten laden und anzeigen
        
        self.load_dashboard(CARD_BG)

        # Scrollbar + Inhalt kombinieren
        scroll_area.setWidget(content)
        main_layout.addWidget(scroll_area)

    
    # FUNKTION: WALLET- UND TRANSAKTIONSDATEN LADEN
    
    def load_dashboard(self, CARD_BG):
        """
        Lädt alle relevanten Benutzerdaten:
         - Wallets
         - Transaktionen
         - Summen (Balance, Einnahmen, Ausgaben)
        """
        if not self.user_id:
            # Kein Benutzer-ID → kein Zugriff auf DB
            print("[Dashboard Fehler] Keine User-ID übergeben.")
            return

        # Alle Wallets dieses Benutzers abrufen
        wallets = get_wallets_by_user(self.user_id)

        # Wenn Benutzer keine Wallets hat → automatisch eine erstellen
        if not wallets:
            print("[Dashboard] Kein Wallet gefunden → Erstelle 'Main Wallet'")
            wallet_id = create_wallet(self.user_id, "Main Wallet", 0.0)
            self.wallet_id = wallet_id
            balance = 0.0
            transactions = []  # noch keine Transaktionen vorhanden
        else:
            # Erstes Wallet als Standardwallet verwenden
            main_wallet = wallets[0]
            self.wallet_id = str(main_wallet["_id"])
            balance = calculate_wallet_balance(self.wallet_id)
            transactions = get_transactions_by_wallet(self.wallet_id)

        
        # Anzeige: Willkommen + Kontostand
        
        welcome = QLabel(f"Willkommen, {self.username} – aktueller Kontostand: {balance:.2f} €")
        welcome.setFont(QFont("Arial", 18))
        welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome.setStyleSheet("color: #CCCCCC; margin-top: 10px; margin-bottom: 20px;")
        self.content_layout.addWidget(welcome)

        
        # Statistik-Karten (Balance / Ausgaben / Einnahmen)
        
        grid = QGridLayout()
        grid.setSpacing(20)

        # Summen aus Transaktionen berechnen
        expenses = sum(abs(t["amount"]) for t in transactions if t["amount"] < 0)
        income = sum(t["amount"] for t in transactions if t["amount"] > 0)

        # Drei Anzeigekarten
        cards = [
            ("Kontostand", f"{balance:.2f} €"),
            ("Monatsausgaben", f"{expenses:.2f} €"),
            ("Einnahmen", f"{income:.2f} €"),
        ]

        # Jede Karte als eigenes UI-Element
        for i, (title_text, value_text) in enumerate(cards):
            card = QFrame()
            card.setStyleSheet(f"background-color: {CARD_BG}; border-radius: 18px;")
            card_layout = QVBoxLayout(card)
            card_layout.setSpacing(5)
            card_layout.setContentsMargins(20, 20, 20, 20)

            # Titel (z. B. "Kontostand")
            t = QLabel(title_text)
            t.setFont(QFont("Arial", 22))
            t.setStyleSheet("color: #D0D0D0;")
            t.setAlignment(Qt.AlignmentFlag.AlignHCenter)

            # Wert (z. B. "123.45 €")
            v = QLabel(value_text)
            v.setFont(QFont("Arial", 42, QFont.Weight.Bold))
            v.setStyleSheet("color: white;")
            v.setAlignment(Qt.AlignmentFlag.AlignHCenter)

            card_layout.addWidget(t)
            card_layout.addWidget(v)
            grid.addWidget(card, 0, i)

        self.content_layout.addLayout(grid)

        
        # Letzte Aktivitäten (Transaktionen)
        
        info_card = QFrame()
        info_card.setStyleSheet(f"background-color: {CARD_BG}; border-radius: 18px;")
        info_layout = QVBoxLayout(info_card)
        info_layout.setContentsMargins(25, 25, 25, 25)

        header2 = QLabel("Letzte Aktivitäten")
        header2.setFont(QFont("Arial", 26, QFont.Weight.Bold))
        header2.setStyleSheet("color: white;")
        info_layout.addWidget(header2)

        # Wenn Transaktionen vorhanden sind → zeige letzte 5
        if transactions:
            last_5 = transactions[-5:]
            text_lines = [
                f"• {t['amount']:.2f} € – {t.get('description', 'Keine Beschreibung')}"
                for t in reversed(last_5)
            ]
            activities_text = "\n".join(text_lines)
        else:
            activities_text = "Keine Transaktionen vorhanden."

        activities = QLabel(activities_text)
        activities.setFont(QFont("Arial", 20))
        activities.setStyleSheet("color: #DDDDDD;")
        info_layout.addWidget(activities)
        self.content_layout.addWidget(info_card)

    
    # TRANSAKTIONSFENSTER ÖFFNEN
    
    def open_transactions(self):
        """Öffnet das Fenster zur Transaktionsverwaltung."""
        if not self.wallet_id:
            print("[Fehler] Keine Wallet-ID übergeben – kann Transaktionsfenster nicht öffnen.")
            return
        self.trans_window = TransactionWindow(wallet_id=self.wallet_id, dashboard_ref=self)
        self.trans_window.show()

    
    # WALLET-FENSTER ÖFFNEN
    
    def open_wallet(self):
        """Öffnet das Fenster zur Wallet-Verwaltung."""
        if not self.user_id:
            print("[Fehler] Keine User-ID - kann Wallets-Fenster nicht öffnen.")
            return
        self.wallet_window = WalletsWindow(user_id=self.user_id)
        self.wallet_window.show()

    
    # LOGOUT
    
    def logout(self):
        """Beendet aktuelle Sitzung und schließt das Fenster."""
        if self.on_logout:
            self.on_logout()
        self.close()



# TESTSTART (Nur beim direkten Start ausführen)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    test_user_id = "674ff8b16e7b59e0c0b57d82"  # Beispiel-User-ID zum Testen
    win = DashboardWindow(username="kingivan", user_id=test_user_id)
    win.show()
    sys.exit(app.exec())