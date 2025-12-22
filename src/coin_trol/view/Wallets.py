"""
Wallets.py
----------
GUI-Fenster zur Verwaltung von Wallets in der CoinTrol-App.

Hauptfunktionen:
 - Anzeigen aller Wallets eines Benutzers
 - Berechnen aktueller Kontostände
 - Erstellen neuer Wallets
 - Anzeige vollständig scrollbar (für viele Wallets)
 - Sofortige Rückmeldung über Statusleiste (statt Popup-Fenster)
"""


# BENÖTIGTE PYQT-IMPORTS

from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QFrame, QApplication,
    QScrollArea, QPushButton, QHBoxLayout, QStatusBar
)
from PyQt6.QtGui import QFont, QColor, QPalette
from PyQt6.QtCore import Qt
import sys


# IMPORTS AUS DEM MODEL (DB-FUNKTIONEN)

from coin_trol.model.db_interface import (
    get_wallets_by_user,         # Holt alle Wallets eines Benutzers
    calculate_wallet_balance,    # Berechnet aktuellen Kontostand eines Wallets
    create_wallet,               # Erstellt ein neues Wallet in der Datenbank
)



# KLASSE: WalletsWindow

class WalletsWindow(QWidget):
    """
    Fenster zur Anzeige und Verwaltung von Wallets.
    Dieses Fenster zeigt eine Liste aller Wallets eines Benutzers und erlaubt das
    Erstellen neuer Wallets über einen Button am unteren Rand.
    """

    def __init__(self, user_id=None):
        """
        Konstruktor – erstellt das Wallet-Fenster.
        :param user_id: Benutzer-ID, wird benötigt um Wallets aus der DB zu laden.
        """
        super().__init__()

        # Benutzer-ID speichern (wichtig für alle DB-Abfragen)
        self.user_id = user_id

        
        # FENSTER-EIGENSCHAFTEN
        
        self.setWindowTitle("CoinTrol – Wallets")
        self.resize(1100, 700)

        # Hintergrundfarbe (Dark Mode)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#1C1C1E"))  # sehr dunkles Grau
        self.setPalette(palette)

        
        # HAUPTLAYOUT
        
        main = QVBoxLayout(self)
        main.setContentsMargins(30, 30, 30, 30)
        main.setSpacing(25)

        
        # TITEL
        
        title = QLabel("Wallet Übersicht")
        title.setFont(QFont("Arial", 36, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #FFFFFF;")  # weißer Text
        main.addWidget(title)

        # Untertitel zur Erklärung
        subtitle = QLabel("Alle deine Wallets und aktuellen Kontostände")
        subtitle.setFont(QFont("Arial", 18))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #BBBBBB; margin-bottom: 10px;")
        main.addWidget(subtitle)

        
        # SCROLLBEREICH (dynamisch für beliebig viele Wallets)
        
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("border: none;")  # kein sichtbarer Rahmen
        main.addWidget(self.scroll)

        # Innerer Inhalt (Container für Wallet-Karten)
        content = QWidget()
        self.scroll.setWidget(content)

        # Layout für Wallet-Liste (alle Karten)
        self.list_layout = QVBoxLayout(content)
        self.list_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.list_layout.setSpacing(15)

        
        # BUTTON: NEUES WALLET ERSTELLEN
        
        add_wallet_btn = QPushButton("Neues Wallet erstellen")
        add_wallet_btn.setFixedHeight(50)
        add_wallet_btn.setStyleSheet("""
            QPushButton {
                background-color: #5B5CF0;  /* CoinTrol Blau-Violett */
                color: white;
                font-size: 18px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #6D6EFA;
            }
        """)
        add_wallet_btn.clicked.connect(self.add_wallet)
        main.addWidget(add_wallet_btn)

        
        # STATUSLEISTE (unten, statt Popup-Meldungen)
        
        self.status_bar = QStatusBar()
        self.status_bar.setStyleSheet("color: white; background-color: #1E1F26; border-radius: 6px; padding: 3px;")
        self.status_bar.showMessage("Wallet-Fenster geöffnet. Bereit.")
        main.addWidget(self.status_bar)

        
        # DATEN LADEN UND ANZEIGEN
        
        self.load_wallets()

    
    # FUNKTION: WALLETS LADEN UND ANZEIGEN
    
    def load_wallets(self):
        """
        Lädt alle Wallets des Benutzers aus der Datenbank
        und zeigt sie im Scrollbereich an.
        """
        # Zuerst alte Widgets entfernen (z. B. bei Refresh)
        for i in reversed(range(self.list_layout.count())):
            self.list_layout.itemAt(i).widget().deleteLater()

        # Wenn keine User-ID übergeben → Fehler
        if not self.user_id:
            label = QLabel("Fehler: Keine User-ID übergeben.")
            label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
            label.setStyleSheet("color: red; margin-top: 40px;")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.list_layout.addWidget(label)
            self.status_bar.showMessage("Fehler: Benutzer-ID fehlt. Wallets können nicht geladen werden.")
            return

        # Wallets aus DB abrufen
        wallets = get_wallets_by_user(self.user_id)

        # Wenn Benutzer keine Wallets hat
        if not wallets:
            info = QLabel("Du hast noch keine Wallets.")
            info.setFont(QFont("Arial", 20))
            info.setStyleSheet("color: #AAAAAA; margin-top: 30px;")
            info.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.list_layout.addWidget(info)
            self.status_bar.showMessage("Keine Wallets gefunden. Erstelle ein neues Wallet, um zu starten.")
            return

        
        # ALLE WALLETS ANZEIGEN (als Karten)
        
        for w in wallets:
            # Eine "Card" für jedes Wallet
            card = QFrame()
            card.setStyleSheet("""
                QFrame {
                    background-color: #2C2C2E;
                    border-radius: 16px;
                }
            """)
            layout = QHBoxLayout(card)
            layout.setContentsMargins(25, 20, 25, 20)
            layout.setSpacing(20)

            # Wallet-Infos abrufen
            name = w.get("name", "Unbekanntes Wallet")
            currency = w.get("currency", "EUR")
            wallet_id = str(w["_id"])

            # Aktuellen Kontostand neu berechnen
            balance = calculate_wallet_balance(wallet_id)

            
            # NAME LABEL
            
            name_lbl = QLabel(name)
            name_lbl.setFont(QFont("Arial Black", 26))
            name_lbl.setStyleSheet("color: white;")
            layout.addWidget(name_lbl, 2)  # mehr Platz für Name

            
            # KONTOSTAND LABEL
            
            balance_lbl = QLabel(f"{balance:.2f} {currency}")
            balance_lbl.setFont(QFont("Arial", 24))
            balance_lbl.setStyleSheet("color: #7B87F9;")  # blau-violett
            layout.addWidget(balance_lbl, 1)

            
            # WALLET-ID LABEL
            
            id_lbl = QLabel(f"ID: {wallet_id}")
            id_lbl.setFont(QFont("Arial", 14))
            id_lbl.setStyleSheet("color: #888888;")  # hellgrau
            layout.addWidget(id_lbl, 2)

            
            # CARD ZUM LAYOUT HINZUFÜGEN
            
            self.list_layout.addWidget(card)

        # Rückmeldung an Benutzer
        self.status_bar.showMessage(f"{len(wallets)} Wallet(s) erfolgreich geladen.")

    
    # FUNKTION: NEUES WALLET HINZUFÜGEN
    
    def add_wallet(self):
        """
        Erstellt ein neues Wallet in der Datenbank und lädt
        anschließend die Wallet-Liste neu.
        """
        # Wenn keine Benutzer-ID vorhanden → Fehler
        if not self.user_id:
            self.status_bar.showMessage("Fehler: Keine Benutzer-ID übergeben. Wallet kann nicht erstellt werden.")
            return

        # Automatischer Name: Wallet + Nummer
        existing_wallets = get_wallets_by_user(self.user_id)
        new_name = f"Wallet {len(existing_wallets) + 1}"

        try:
            # Wallet erstellen (Startbalance = 0.0)
            create_wallet(self.user_id, new_name, 0.0)
            self.status_bar.showMessage(f"{new_name} wurde erfolgreich erstellt.")
            self.load_wallets()  # Ansicht aktualisieren
        except Exception as e:
            self.status_bar.showMessage(f"Fehler: Wallet konnte nicht erstellt werden ({e}).")

    
    # BEIM SCHLIESSEN DES FENSTERS
    
    def closeEvent(self, event):
        """
        Wird ausgeführt, wenn das Fenster geschlossen wird.
        Gibt Rückmeldung in der Konsole + Statusleiste.
        """
        print("[Wallets] Fenster wurde geschlossen.")
        self.status_bar.showMessage("Wallet-Fenster geschlossen.")
        event.accept()



# TESTSTART (nur für lokale Ausführung)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    test_user_id = "674ff8b16e7b59e0c0b57d82"  # Beispiel-User-ID aus DB
    win = WalletsWindow(user_id=test_user_id)
    win.show()
    sys.exit(app.exec())