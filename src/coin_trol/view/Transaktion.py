"""
Transaktion.py
---------------
GUI-Fenster zur Verwaltung von Transaktionen (Einnahmen & Ausgaben).
Ermöglicht:
 - Hinzufügen neuer Transaktionen
 - Bearbeiten bestehender Transaktionen
 - Löschen von Transaktionen
 - Sofortige Aktualisierung des Dashboards

Dieses Fenster wird vom Dashboard geöffnet.
"""


# BENÖTIGTE PYQT-IMPORTS

from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QComboBox, QScrollArea, QFrame, QDialog, QStatusBar
)
from PyQt6.QtGui import QFont, QColor, QPalette
from PyQt6.QtCore import Qt
import datetime


# IMPORT AUS DEM MODEL – Datenbankfunktionen

from coin_trol.model.db_interface import (
    get_transactions_by_wallet,   # Alle Transaktionen eines Wallets abrufen
    add_transaction,              # Neue Transaktion speichern
    delete_transaction,           # Transaktion entfernen
    update_wallet_balance         # Kontostand nach Änderungen neu berechnen
)



# KLASSE: TRANSAKTIONSFENSTER

class TransactionWindow(QWidget):
    """
    Fenster zur Verwaltung von Transaktionen.
    Es zeigt alle bisherigen Transaktionen an und erlaubt,
    neue hinzuzufügen, zu ändern oder zu löschen.
    """

    def __init__(self, wallet_id=None, dashboard_ref=None):
        """
        Konstruktor – erstellt das Transaktionsfenster.

        :param wallet_id: ID des Wallets (notwendig für DB-Abfragen)
        :param dashboard_ref: Referenz auf das Dashboard zur Aktualisierung
        """
        super().__init__()

        # Übergabeparameter speichern
        self.wallet_id = wallet_id
        self.dashboard_ref = dashboard_ref  # Dashboard-Referenz für späteres Reload

        
        # FENSTERKONFIGURATION
        
        self.setWindowTitle("CoinTrol – Transaktionen")
        self.resize(1100, 720)

        # Dunkles Design
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#1C1C1E"))
        self.setPalette(palette)

        
        # HAUPTLAYOUT (enthält alles)
        
        self.main = QVBoxLayout(self)
        self.main.setContentsMargins(30, 30, 30, 30)
        self.main.setSpacing(25)

        
        # TITEL
        
        title = QLabel("Transaktionen")
        title.setFont(QFont("Arial Black", 34))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #6D6EFA;")  # Violetter Akzent
        self.main.addWidget(title)

        
        # EINGABEBEREICH OBEN
        
        input_frame = QFrame()
        input_layout = QHBoxLayout(input_frame)
        input_layout.setSpacing(10)

        # Datum (automatisch)
        self.date_label = QLabel(datetime.datetime.now().strftime("%d.%m.%Y"))
        self.date_label.setFont(QFont("Arial", 16))
        self.date_label.setStyleSheet("color: white;")
        input_layout.addWidget(self.date_label)

        # Betrag (Euro + Cent)
        self.euro_input = QLineEdit()
        self.euro_input.setPlaceholderText("Euro")
        self._style_input(self.euro_input)
        input_layout.addWidget(self.euro_input)

        self.cent_input = QLineEdit()
        self.cent_input.setPlaceholderText("Cent")
        self._style_input(self.cent_input)
        input_layout.addWidget(self.cent_input)

        # Richtung (Ausgabe oder Einnahme)
        self.direction_box = QComboBox()
        self.direction_box.addItems(["Ausgabe (-)", "Einnahme (+)"])
        self.direction_box.setStyleSheet("""
            QComboBox {
                background-color: #2E2E36;
                color: white;
                border-radius: 6px;
                padding: 6px;
                font-size: 16px;
            }
        """)
        input_layout.addWidget(self.direction_box)

        # Kategorieauswahl
        self.category = QComboBox()
        self.category.addItems(["Lebensmittel", "Transport", "Freizeit", "Sonstiges"])
        self.category.setStyleSheet("""
            QComboBox {
                background-color: #2E2E36;
                color: white;
                border-radius: 6px;
                padding: 6px;
                font-size: 16px;
            }
        """)
        input_layout.addWidget(self.category)

        # Währungsauswahl
        self.currency_box = QComboBox()
        self.currency_box.addItems(["EUR", "USD", "RSD", "CHF"])
        self.currency_box.setStyleSheet("""
            QComboBox {
                background-color: #2E2E36;
                color: white;
                border-radius: 6px;
                padding: 6px;
                font-size: 16px;
            }
        """)
        input_layout.addWidget(self.currency_box)

        # Beschreibung (frei)
        self.desc_input = QLineEdit()
        self.desc_input.setPlaceholderText("Beschreibung (z. B. McDonalds, Tanken …)")
        self._style_input(self.desc_input)
        input_layout.addWidget(self.desc_input)

        # Button – neue Transaktion hinzufügen
        add_btn = QPushButton("Transaktion hinzufügen")
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #5B5CF0;
                color: white;
                border-radius: 8px;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #6D6EFA;
            }
        """)
        add_btn.clicked.connect(self.add_transaction)
        input_layout.addWidget(add_btn)

        # Eingabeframe dem Hauptlayout hinzufügen
        self.main.addWidget(input_frame)

        
        # SCROLLBARE TRANSAKTIONSLISTE
        
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("border: none;")
        self.main.addWidget(self.scroll)

        # Inhalt der ScrollArea
        self.content = QWidget()
        self.scroll.setWidget(self.content)
        self.list_layout = QVBoxLayout(self.content)
        self.list_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.list_layout.setSpacing(15)

        
        # STATUSLEISTE UNTEN
        
        self.status_bar = QStatusBar()
        self.status_bar.setStyleSheet("color: white; background-color: #1E1F26; border-radius: 6px; padding: 3px;")
        self.status_bar.showMessage("Bereit – Transaktionen können verwaltet werden.")
        self.main.addWidget(self.status_bar)

        # Beim Start alle Transaktionen laden
        self.load_transactions()

    
    # TRANSAKTION HINZUFÜGEN
    
    def add_transaction(self):
        """Liest Eingaben aus, speichert neue Transaktion und aktualisiert Dashboard."""
        if not self.wallet_id:
            self.status_bar.showMessage("Fehler: Keine Wallet-ID übergeben.")
            return

        # Betrag berechnen (Euro + Cent)
        euro = self.euro_input.text().strip() or "0"
        cent = self.cent_input.text().strip() or "0"
        try:
            amount = float(euro) + float(cent) / 100
        except ValueError:
            self.status_bar.showMessage("Fehler: Ungültiger Betrag.")
            return

        # Richtung prüfen → Ausgabe = negativ
        direction = self.direction_box.currentText()
        amount = -abs(amount) if "Ausgabe" in direction else abs(amount)

        # Felder auslesen
        category = self.category.currentText()
        currency = self.currency_box.currentText()
        desc = self.desc_input.text().strip() or "Keine Beschreibung"

        # Neue Transaktion in DB speichern
        add_transaction(self.wallet_id, amount, category, desc, currency)

        # Kontostand neu berechnen
        update_wallet_balance(self.wallet_id)

        # Dashboard aktualisieren
        if self.dashboard_ref:
            self.dashboard_ref.load_dashboard("#3A3A42")

        # Benutzer-Feedback
        self.status_bar.showMessage("Transaktion erfolgreich gespeichert.")

        # Eingabefelder leeren
        self.euro_input.clear()
        self.cent_input.clear()
        self.desc_input.clear()

        # Transaktionsliste neu laden
        self.load_transactions()

    
    # TRANSAKTIONEN LADEN UND ANZEIGEN
    
    def load_transactions(self):
        """Lädt alle Transaktionen aus der DB und zeigt sie als Liste an."""

        # Vorherige Widgets entfernen (verhindert doppelte Anzeige)
        for i in reversed(range(self.list_layout.count())):
            self.list_layout.itemAt(i).widget().setParent(None)

        # Transaktionen holen
        transactions = get_transactions_by_wallet(self.wallet_id)

        # Wenn keine vorhanden
        if not transactions:
            lbl = QLabel("Noch keine Transaktionen vorhanden.")
            lbl.setStyleSheet("color: #AAAAAA; font-size: 20px;")
            self.list_layout.addWidget(lbl)
            return

        # Jede Transaktion als eigenes Element anzeigen
        for t in transactions:
            frame = QFrame()
            frame.setStyleSheet("background-color: #2E2E36; border-radius: 12px;")
            lay = QHBoxLayout(frame)
            lay.setContentsMargins(15, 10, 15, 10)

            # Vorzeichen und Farbe je nach Richtung
            sign = "+" if t["amount"] > 0 else "-"
            color = "#47E47B" if t["amount"] > 0 else "#E45757"

            # Beschriftung
            text = QLabel(
                f"{sign}{abs(t['amount']):.2f} {t.get('currency', 'EUR')} – "
                f"{t['category']} – {t.get('description', '')}"
            )
            text.setStyleSheet(f"color: {color}; font-size: 18px;")
            lay.addWidget(text)

            # Button: Ändern
            edit_btn = QPushButton("Ändern")
            edit_btn.setStyleSheet("background-color: #3A3A48; color: white; border-radius: 6px; padding: 6px;")
            edit_btn.clicked.connect(lambda _, tid=t["_id"]: self.edit_transaction(tid))
            lay.addWidget(edit_btn)

            # Button: Löschen
            del_btn = QPushButton("Löschen")
            del_btn.setStyleSheet("background-color: #C13535; color: white; border-radius: 6px; padding: 6px;")
            del_btn.clicked.connect(lambda _, tid=t["_id"]: self.delete_transaction(tid))
            lay.addWidget(del_btn)

            # Zeile in Liste einfügen
            self.list_layout.addWidget(frame)

    
    # TRANSAKTION BEARBEITEN
    
    def edit_transaction(self, trans_id):
        """
        Öffnet ein Dialogfenster zum Bearbeiten einer Transaktion.
        Änderungen werden direkt in der Datenbank gespeichert.
        """
        transactions = get_transactions_by_wallet(self.wallet_id)
        trans = next((t for t in transactions if str(t["_id"]) == str(trans_id)), None)
        if not trans:
            self.status_bar.showMessage("Fehler: Transaktion nicht gefunden.")
            return

        # Dialog erstellen
        dialog = QDialog(self)
        dialog.setWindowTitle("Transaktion bearbeiten")
        dialog.resize(400, 340)
        layout = QVBoxLayout(dialog)
        layout.setSpacing(10)

        # Eingabefelder
        euro_input = QLineEdit(str(abs(int(trans["amount"]))))
        cent_input = QLineEdit("0")
        self._style_input(euro_input)
        self._style_input(cent_input)

        dir_box = QComboBox()
        dir_box.addItems(["Ausgabe (-)", "Einnahme (+)"])
        dir_box.setCurrentIndex(1 if trans["amount"] > 0 else 0)

        cat_box = QComboBox()
        cat_box.addItems(["Lebensmittel", "Transport", "Freizeit", "Sonstiges"])
        cat_box.setCurrentText(trans.get("category", "Sonstiges"))

        curr_box = QComboBox()
        curr_box.addItems(["EUR", "USD", "RSD", "CHF", "GBP"])
        curr_box.setCurrentText(trans.get("currency", "EUR"))

        desc_input = QLineEdit(trans.get("description", ""))
        desc_input.setPlaceholderText("Beschreibung")
        self._style_input(desc_input)

        # Layout zusammensetzen
        h1 = QHBoxLayout()
        h1.addWidget(euro_input)
        h1.addWidget(cent_input)
        layout.addLayout(h1)
        layout.addWidget(dir_box)
        layout.addWidget(cat_box)
        layout.addWidget(curr_box)
        layout.addWidget(desc_input)

        # Buttons (Speichern / Abbrechen)
        save_btn = QPushButton("Speichern")
        save_btn.setStyleSheet("background-color: #5B5CF0; color: white; border-radius: 8px; padding: 8px;")
        cancel_btn = QPushButton("Abbrechen")
        cancel_btn.setStyleSheet("background-color: #3A3A48; color: white; border-radius: 8px; padding: 8px;")
        layout.addWidget(save_btn)
        layout.addWidget(cancel_btn)

        
        # SAVE-FUNKTION (innerhalb des Dialogs)
        
        def save_changes():
            """Speichert Änderungen in der Datenbank."""
            try:
                euro = float(euro_input.text() or "0")
                cent = float(cent_input.text() or "0")
                amount = euro + cent / 100
                if "Ausgabe" in dir_box.currentText():
                    amount = -abs(amount)
                else:
                    amount = abs(amount)

                from coin_trol.model.db_interface import transactions_col
                transactions_col.update_one(
                    {"_id": trans["_id"]},
                    {"$set": {
                        "amount": amount,
                        "category": cat_box.currentText(),
                        "currency": curr_box.currentText(),
                        "description": desc_input.text().strip() or "Keine Beschreibung"
                    }}
                )

                update_wallet_balance(self.wallet_id)

                if self.dashboard_ref:
                    self.dashboard_ref.load_dashboard("#3A3A42")

                dialog.accept()
                self.status_bar.showMessage("Transaktion erfolgreich geändert.")
                self.load_transactions()

            except Exception as e:
                self.status_bar.showMessage(f"Fehler: Änderung fehlgeschlagen ({e})")

        save_btn.clicked.connect(save_changes)
        cancel_btn.clicked.connect(dialog.reject)
        dialog.exec()

    
    # TRANSAKTION LÖSCHEN
    
    def delete_transaction(self, trans_id):
        """Löscht Transaktion nach Bestätigung."""
        delete_transaction(str(trans_id))
        update_wallet_balance(self.wallet_id)
        if self.dashboard_ref:
            self.dashboard_ref.load_dashboard("#3A3A42")
        self.load_transactions()
        self.status_bar.showMessage("Transaktion erfolgreich gelöscht.")

    
    # STYLING-HILFSMETHODE
    
    def _style_input(self, widget):
        """Einheitliches Styling für Eingabefelder."""
        widget.setFixedHeight(44)
        widget.setStyleSheet("""
            QLineEdit {
                background-color: #2E2E36;
                color: white;
                border-radius: 8px;
                padding-left: 12px;
                font-size: 17px;
                min-width: 100px;
            }
        """)

    
    # BEIM SCHLIESSEN DES FENSTERS
    
    def closeEvent(self, event):
        """Aktualisiert Dashboard automatisch beim Schließen."""
        if self.dashboard_ref:
            try:
                self.dashboard_ref.load_dashboard("#3A3A42")
                self.status_bar.showMessage("Dashboard wurde aktualisiert.")
            except Exception as e:
                self.status_bar.showMessage(f"Fehler beim Aktualisieren: {e}")
        event.accept()