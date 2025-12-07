from PyQt6.QtWidgets import (         # Import der GUI-Elemente (Widgets, Layouts, Frames)
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame,
    QApplication, QScrollArea
)
from PyQt6.QtGui import QFont, QColor, QPalette   # Import für Schriftarten, Farben, Paletten
from PyQt6.QtCore import Qt                       # Import allgemeiner Qt-Funktionen/Flags
import sys                                         # Für Systemargumente (z. B. sys.argv)



class WalletsWindow(QWidget):
    def __init__(self, transactions=None):
        super().__init__()

        # Liste der Transaktionen übernehmen
        # Falls keine übergeben wird → leere Liste verwenden
        self.transactions = transactions if transactions else []

        # Fenster-Einstellungen
        self.setWindowTitle("CoinTrol - Wallets")
        self.resize(1100, 700)

        # Hintergrundfarbe des Fensters setzen (dunkles Theme)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#1C1C1E"))
        self.setPalette(palette)

        # Hauptlayout (vertikal)
        main = QVBoxLayout(self)
        main.setContentsMargins(30, 30, 30, 30)   # Abstand zum Rand
        main.setSpacing(25)                       # Abstand zwischen Elementen

        # Titel-Label
        title = QLabel("Wallet Übersicht")
        title.setFont(QFont("Arial", 36, QFont.Weight.Bold))    # große Schrift
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)         # zentriert
        title.setStyleSheet("color: #FFFFFF;")                   # weißer Text
        main.addWidget(title)

        # Untertitel
        subtitle = QLabel("Alle bisherigen Transaktionen")
        subtitle.setFont(QFont("Arial", 18))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #BBBBBB; margin-bottom: 10px;")
        main.addWidget(subtitle)

        # ScrollArea, damit viele Einträge scrollbar angezeigt werden
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)             # Inhalt passt sich an
        scroll.setStyleSheet("border: none;")       # keine Umrandung
        main.addWidget(scroll)

        # Inhalt der ScrollArea
        content = QWidget()
        scroll.setWidget(content)

        # Layout für die Transaktionsliste
        self.list_layout = QVBoxLayout(content)
        self.list_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.list_layout.setSpacing(15)             # Abstand zwischen Karten

        # Daten reinladen
        self.load_transactions()


    # ------------------------------------------------------------
    # Transaktions-Liste anzeigen
    # ------------------------------------------------------------
    def load_transactions(self):
        # Wenn keine Transaktionen vorhanden sind → Hinweis anzeigen
        if not self.transactions:
            label = QLabel("Keine Transaktionen vorhanden")
            label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
            label.setStyleSheet("color: #888888; margin-top: 40px;")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.list_layout.addWidget(label)
            return

        # Für jede Transaktion eine „Karte“ erzeugen
        for t in self.transactions:

            # Container-Frame (Karte)
            card = QFrame()
            card.setStyleSheet("""
                QFrame {
                    background-color: #2C2C2E;    /* dunkle Karte */
                    border-radius: 16px;           /* abgerundete Ecken */
                }
            """)

            # Layout für die Karte
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(20, 18, 20, 18)   # Innenabstand
            card_layout.setSpacing(6)                        # Abstand innen

            # Betrag + Währung
            # :.2f → zwei Dezimalstellen
            amount_lbl = QLabel(f"{t['amount']:.2f} {t['currency']}")
            amount_lbl.setFont(QFont("Arial Black", 28))     # sehr groß
            amount_lbl.setStyleSheet("color: #FFFFFF;")
            card_layout.addWidget(amount_lbl)

            # Kategorie / Zweck (z. B. Lebensmittel, Transport)
            purpose_lbl = QLabel(f"Zweck: {t['purpose']}")
            purpose_lbl.setFont(QFont("Arial", 18))
            purpose_lbl.setStyleSheet("color: #7B87F9;")      # Akzentfarbe
            card_layout.addWidget(purpose_lbl)

            # Beschreibung (z. B. „McDonalds“)
            desc_lbl = QLabel(t["description"])
            desc_lbl.setFont(QFont("Arial", 16))
            desc_lbl.setStyleSheet("color: #DDDDDD;")
            card_layout.addWidget(desc_lbl)

            # Karte ins Listenlayout
            self.list_layout.addWidget(card)



# ------------------------------------------------------------
# Start (für Test)
# ------------------------------------------------------------
if __name__ == "__main__":
    # Beispiel-Daten zum Testen
    example_data = [
        {"amount": 15.30, "currency": "EUR", "description": "McDonalds", "purpose": "Lebensmittel"},
        {"amount": 8.00, "currency": "EUR", "description": "Öffi Ticket", "purpose": "Transport"},
        {"amount": 120.00, "currency": "EUR", "description": "Gehalt", "purpose": "Einnahmen"},
        {"amount": 8.00, "currency": "EUR", "description": "Öffi Ticket", "purpose": "Transport"},
        {"amount": 120.00, "currency": "EUR", "description": "Gehalt", "purpose": "Einnahmen"},
    ]

    # App starten
    app = QApplication(sys.argv)          # PyQt-Anwendung starten (muss immer zuerst ausgeführt werden)
    win = WalletsWindow(example_data)     # Hauptfenster erzeugen
    win.show()                            # Fenster sichtbar machen
    sys.exit(app.exec())                  # Event-Loop starten und Programm sauber beenden
