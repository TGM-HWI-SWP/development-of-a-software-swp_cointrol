from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QComboBox, QApplication, QScrollArea, QFrame, QGridLayout, QDialog
)  # PyQt6-Widgets: Fenster, Layouts, Eingabefelder, Buttons, Scroll-Bereiche, Dialoge
from PyQt6.QtGui import QFont, QColor, QPalette  # GUI: Schriftarten, Farben, Hintergrund-Paletten
from PyQt6.QtCore import Qt                      # Qt-Basisfunktionen, z. B. Alignments
import sys                                       # Systemfunktionen für Start/Beenden der Anwendung
import datetime                                  # Für Datum-Auswahl (Tag/Monat/Jahr)



# ------------------------------------------------------------
# Hover-Effekt
# ------------------------------------------------------------
def apply_hover(button, normal_color, hover_color):  # Funktion, die Hover-Effekt für Buttons erzeugt
    button.setStyleSheet(f"""
        QPushButton {{
            background-color: {normal_color};
            color: white;
            border-radius: 10px;
            font-size: 16px;
            padding: 8px;
        }}
    """)  # Setzt den normalen Button-Style

    def enterEvent(event):  # Wird ausgeführt, wenn Maus über den Button fährt
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {hover_color};
                color: white;
                border-radius: 10px;
                font-size: 16px;
                padding: 8px;
            }}
        """)  # Setzt Hover-Style

    def leaveEvent(event):  # Wird ausgeführt, wenn Maus den Button verlässt
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {normal_color};
                color: white;
                border-radius: 10px;
                font-size: 16px;
                padding: 8px;
            }}
        """)  # Setzt wieder normalen Style zurück

    button.enterEvent = enterEvent  # Überschreibt das enterEvent des Buttons
    button.leaveEvent = leaveEvent  # Überschreibt das leaveEvent des Buttons




# ------------------------------------------------------------
# TRANSAKTIONS-FENSTER
# ------------------------------------------------------------
class TransactionWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("COINTROL – TRANSAKTIONEN")
        self.resize(1200, 900)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#111215"))
        self.setPalette(palette)

        self.transactions = []

        main = QVBoxLayout(self)
        main.setContentsMargins(30, 25, 30, 25)
        main.setSpacing(20)

        # ------------------------------------------------------------
        # Titel
        # ------------------------------------------------------------
        title = QLabel("TRANSAKTIONEN")
        title.setFont(QFont("Arial Black", 38))
        title.setStyleSheet("color: #5B5CF0;")
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        main.addWidget(title)

        # ------------------------------------------------------------
        # INPUT-KARTE
        # ------------------------------------------------------------
        card = QFrame()
        card.setStyleSheet("background-color: #1A1B1F; border-radius: 16px;")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(12, 12, 12, 12)
        card_layout.setSpacing(10)

        # ============================================================
        # REIHE 1: DATUM — BETRAG — WÄHRUNG
        # ============================================================
        row1 = QHBoxLayout()
        row1.setSpacing(12)

        # ----------------- Datum -----------------
        left_block = QHBoxLayout()
        left_block.setSpacing(6)

        self.day = QComboBox()  # Dropdown für den Tag
        self.day.addItems([str(i) for i in range(1, 32)])  # Tage 1–31 einfügen
        self.day.setFixedWidth(75)  # Breite des Tages-Dropdowns
        self._style_combo(self.day)  # Einheitliches Styling für ComboBox
        left_block.addWidget(self.day)  # In linken Block einfügen

        self.month = QComboBox()  # Dropdown für den Monat
        self.month.addItems([
            "Jänner", "Februar", "März", "April", "Mai", "Juni",
            "Juli", "August", "September", "Oktober", "November", "Dezember"
        ])  # Monatsnamen einfügen
        self.month.setFixedWidth(140)  # Breite des Monats-Dropdowns
        self._style_combo(self.month)  # Styling anwenden
        left_block.addWidget(self.month)  # In linken Block einfügen

        year_now = datetime.datetime.now().year  # Aktuelles Jahr ermitteln
        self.year = QComboBox()  # Dropdown für Jahr
        self.year.addItems([str(year_now - 1), str(year_now), str(year_now + 1)])  # Vorjahr, aktuelles Jahr, nächstes Jahr
        self.year.setFixedWidth(100)  # Breite des Jahres-Dropdowns
        self._style_combo(self.year)  # Styling anwenden
        left_block.addWidget(self.year)  # In linken Block einfügen


        row1.addLayout(left_block)
        row1.addStretch()

        # ----------------- Betrag -----------------
        middle_block = QHBoxLayout()
        middle_block.setSpacing(5)

        self.euro_input = QLineEdit()
        self.euro_input.setPlaceholderText("Euro")
        self.euro_input.setFixedWidth(100)
        self._style_input(self.euro_input)
        middle_block.addWidget(self.euro_input)

        self.cent_input = QLineEdit()
        self.cent_input.setPlaceholderText("Cent")
        self.cent_input.setFixedWidth(60)
        self._style_input(self.cent_input)
        middle_block.addWidget(self.cent_input)

        row1.addLayout(middle_block)
        row1.addStretch()

        # ----------------- Währung -----------------
        right_block = QHBoxLayout()

        self.currency = QComboBox()
        self.currency.addItems(["EUR", "USD", "CHF", "GBP"])
        self.currency.setFixedWidth(95)
        self._style_combo(self.currency)
        right_block.addWidget(self.currency)

        row1.addLayout(right_block)
        card_layout.addLayout(row1)

        # ============================================================
        # REIHE 2: Beschreibung + Zweck
        # ============================================================
        row2 = QHBoxLayout()
        row2.setSpacing(8)

        self.description = QLineEdit()
        self.description.setPlaceholderText("Beschreibung")
        self.description.setFixedWidth(280)
        self._style_input(self.description)
        row2.addWidget(self.description)

        self.purpose = QComboBox()
        self.purpose.addItems([
            "Lebensmittel", "Privat", "Transport", "Freizeit",
            "Fixkosten", "Sparen", "Sonstiges"
        ])
        self.purpose.setFixedWidth(180)
        self._style_combo(self.purpose)
        row2.addWidget(self.purpose)

        row2.addStretch()
        card_layout.addLayout(row2)

        # ============================================================
        # HINZUFÜGEN BUTTON
        # ============================================================
        add_btn = QPushButton("TRANSAKTION HINZUFÜGEN")
        apply_hover(add_btn, "#2968FF", "#3A7BFF")
        add_btn.setFixedHeight(42)
        add_btn.clicked.connect(self.add_transaction)
        card_layout.addWidget(add_btn)

        main.addWidget(card)

        # ------------------------------------------------------------
        # SCROLL-BEREICH
        # ------------------------------------------------------------
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.scroll_area.setWidget(self.scroll_widget)
        main.addWidget(self.scroll_area)



    # ============================================================
    # Styling
    # ============================================================
    def _style_input(self, widget):
        widget.setFixedHeight(40)
        widget.setStyleSheet("""
            QLineEdit {
                background-color: #2B2C31;
                color: white;
                border-radius: 8px;
                padding-left: 12px;
                font-size: 16px;
            }
        """)

    def _style_combo(self, combo):
        combo.setFixedHeight(40)
        combo.setStyleSheet("""
            QComboBox {
                background-color: #2B2C31;
                color: white;
                border-radius: 8px;
                padding-left: 10px;
                font-size: 16px;
            }
            QComboBox QAbstractItemView {
                background-color: #1A1B1F;
                color: white;
            }
        """)


    # ============================================================
    # TRANSAKTION HINZUFÜGEN
    # ============================================================
    def add_transaction(self):
        euro = self.euro_input.text()
        cent = self.cent_input.text()
        desc = self.description.text()

        if not euro.isdigit() or not cent.isdigit() or desc.strip() == "":  # Prüft: Euro und Cent müssen Zahlen sein, Beschreibung darf nicht leer sein
            return  # Wenn ungültig → Vorgang abbrechen


        amount = float(f"{euro}.{cent}")

        t = {
            "amount": amount,  # Betrag (Euro + Cent als Float)
            "currency": self.currency.currentText(),  # Gewählte Währung
            "description": desc,  # Beschreibungstext der Transaktion
            "purpose": self.purpose.currentText(),  # Gewählter Zweck/Kategorie
            "day": self.day.currentText(),  # Ausgewählter Tag
            "month": self.month.currentText(),  # Ausgewählter Monat
            "year": self.year.currentText()  # Ausgewähltes Jahr
        }  


        self.transactions.append(t)
        self.refresh_list()

        self.euro_input.clear()
        self.cent_input.clear()
        self.description.clear()



    # ============================================================
    # LISTE ANZEIGEN
    # ============================================================
    def refresh_list(self):  # Aktualisiert die komplette Transaktionsliste im Scroll-Bereich
        for i in reversed(range(self.scroll_layout.count())):  # Alle bestehenden Widgets rückwärts durchgehen
            # reversed: löscht Widgets von hinten nach vorne, damit die Indexe nicht verrutschen
            self.scroll_layout.itemAt(i).widget().deleteLater()  # Widget löschen, um die Liste zu leeren


        for t in self.transactions:  # Jede gespeicherte Transaktion durchgehen
            card = QFrame()  # Eine neue Karten-Box für die Transaktion
            card.setStyleSheet("background-color: #2F3038; border-radius: 12px;")  # Optische Gestaltung der Karte
            card_layout = QGridLayout(card)  # Rasterlayout für die Inhalte der Karte
            card_layout.setContentsMargins(16, 16, 16, 16)  # Innenabstand der Karte

            lbl_amount = QLabel(f"{t['amount']:.2f} {t['currency']}")  # Betrag + Währung anzeigen
            lbl_amount.setFont(QFont("Arial Black", 22))  # Große Schrift für Betrag
            lbl_amount.setStyleSheet("color: white;")  # Weißer Text
            card_layout.addWidget(lbl_amount, 0, 0)  # Position oben links

            lbl_date = QLabel(f"{t['day']}. {t['month']} {t['year']}")  # Datum anzeigen
            lbl_date.setFont(QFont("Arial", 14))  # Kleinere Schrift
            lbl_date.setStyleSheet("color: #8A8B99;")  # Dezente graue Farbe
            card_layout.addWidget(lbl_date, 0, 1)  # Position oben rechts

            lbl_purpose = QLabel(f"Zweck: {t['purpose']}")  # Zweck/Kategorie anzeigen
            lbl_purpose.setFont(QFont("Arial Black", 16))  # Mittelgroße Schrift
            lbl_purpose.setStyleSheet("color: #5B5CF0;")  # Blaue Akzentfarbe
            card_layout.addWidget(lbl_purpose, 1, 0)  # Unter dem Betrag

            lbl_desc = QLabel(t["description"])  # Beschreibungstext anzeigen
            lbl_desc.setFont(QFont("Arial", 14))  # Normale Schriftgröße
            lbl_desc.setStyleSheet("color: #CFCFCF;")  # Helles Grau für gute Lesbarkeit
            card_layout.addWidget(lbl_desc, 2, 0)  # Unter dem Zweck


            # ÄNDERN BUTTON
            edit_btn = QPushButton("ÄNDERN")  # Button zum Bearbeiten einer Transaktion
            edit_btn.setFixedWidth(95)  # Feste Breite für ein einheitliches Layout
            apply_hover(edit_btn, "#4A4EE8", "#6A6CFF")  # Hover-Effekt hinzufügen
            edit_btn.clicked.connect(lambda event, tr=t: self.edit_transaction(tr))  # Beim Klicken spezifische Transaktion bearbeiten
            card_layout.addWidget(edit_btn, 0, 2)  # Button oben rechts in die Karte einfügen

            # LÖSCHEN BUTTON
            del_btn = QPushButton("LÖSCHEN")  # Button zum Löschen der Transaktion
            del_btn.setFixedWidth(95)  # Feste Breite
            apply_hover(del_btn, "#B12E2E", "#D93838")  # Hover-Effekt für roten Button
            del_btn.clicked.connect(lambda event, tr=t: self.delete_transaction(tr))  # Beim Klicken diese Transaktion löschen
            card_layout.addWidget(del_btn, 1, 2)  # Löschen-Button unter Edit-Button

            self.scroll_layout.addWidget(card)  # Die fertige Transaktionskarte zur Scroll-Liste hinzufügen




    # ============================================================
    # EDIT (inkl. DATUM!)
    # ============================================================
    def edit_transaction(self, t):
        dialog = QDialog(self)
        dialog.setWindowTitle("Transaktion bearbeiten")
        dialog.resize(420, 520)

        v = QVBoxLayout(dialog)
        v.setSpacing(12)

        # ------------------ DATUM ------------------
        date_row = QHBoxLayout()

        day_edit = QComboBox()
        day_edit.addItems([str(i) for i in range(1, 32)])
        day_edit.setCurrentText(t["day"])
        self._style_combo(day_edit)
        date_row.addWidget(day_edit)

        month_edit = QComboBox()
        month_edit.addItems([
            "Jänner", "Februar", "März", "April", "Mai", "Juni",
            "Juli", "August", "September", "Oktober", "November", "Dezember"
        ])
        month_edit.setCurrentText(t["month"])
        self._style_combo(month_edit)
        date_row.addWidget(month_edit)

        year_now = datetime.datetime.now().year
        year_edit = QComboBox()
        year_edit.addItems([str(year_now - 1), str(year_now), str(year_now + 1)])
        year_edit.setCurrentText(t["year"])
        self._style_combo(year_edit)
        date_row.addWidget(year_edit)

        v.addLayout(date_row)

        # ------------------ Betrag ------------------
        euro = QLineEdit()
        cent = QLineEdit()

        euro.setText(str(int(t["amount"])))
        cent.setText(str(int((t["amount"] % 1) * 100)).zfill(2)) # mit zfill(2) auf 2 Stellen auffüllen

        self._style_input(euro)
        self._style_input(cent)

        v.addWidget(euro)
        v.addWidget(cent)

        # ------------------ Beschreibung ------------------
        desc = QLineEdit()
        desc.setText(t["description"])
        self._style_input(desc)
        v.addWidget(desc)

        # ------------------ Zweck ------------------
        purpose_combo = QComboBox()
        purpose_combo.addItems([
            "Lebensmittel", "Privat", "Transport", "Freizeit",
            "Fixkosten", "Sparen", "Sonstiges"
        ])
        purpose_combo.setCurrentText(t["purpose"])
        self._style_combo(purpose_combo)
        v.addWidget(purpose_combo)

        # ------------------ Speichern Button ------------------
        save_btn = QPushButton("Speichern")
        apply_hover(save_btn, "#2968FF", "#3A7BFF")
        v.addWidget(save_btn)

        def save():
            if euro.text().isdigit() and cent.text().isdigit():
                t["amount"] = float(f"{euro.text()}.{cent.text()}")
                t["description"] = desc.text()
                t["purpose"] = purpose_combo.currentText()
                t["day"] = day_edit.currentText()
                t["month"] = month_edit.currentText()
                t["year"] = year_edit.currentText()

                self.refresh_list()
                dialog.close()

        save_btn.clicked.connect(save)
        dialog.exec()


    # ============================================================
    # DELETE
    # ============================================================
    def delete_transaction(self, t):
        self.transactions.remove(t)
        self.refresh_list()




# ------------------------------------------------------------
# START
# ------------------------------------------------------------
if __name__ == "__main__":  # Startpunkt, wenn die Datei direkt ausgeführt wird
    app = QApplication(sys.argv)  # Erstellt die PyQt-Anwendung (verarbeitet Systemargumente)
    win = TransactionWindow()  # Erstellt das Transaktionsfenster
    win.show()  # Zeigt das Fenster auf dem Bildschirm an
    sys.exit(app.exec())  # Startet die Event-Schleife und beendet sauber bei Programmende

