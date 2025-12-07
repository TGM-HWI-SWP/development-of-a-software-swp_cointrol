from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QFrame, QApplication, QScrollArea, QPushButton, QHBoxLayout, QMessageBox
)
from PyQt6.QtGui import QFont, QColor, QPalette
from PyQt6.QtCore import Qt
import sys

# ------------------------------------------------------------
# IMPORTS AUS DEM MODEL
# ------------------------------------------------------------
from coin_trol.model.db_interface import (
    get_wallets_by_user,
    calculate_wallet_balance,
    create_wallet,
)
# ------------------------------------------------------------
# WALLET-FENSTER
# ------------------------------------------------------------
class WalletsWindow(QWidget):
    def __init__(self, user_id=None):
        super().__init__()

        self.user_id = user_id
        self.setWindowTitle("CoinTrol – Wallets")
        self.resize(1100, 700)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#1C1C1E"))
        self.setPalette(palette)

        main = QVBoxLayout(self)
        main.setContentsMargins(30, 30, 30, 30)
        main.setSpacing(25)

        # Titel
        title = QLabel("Wallet Übersicht")
        title.setFont(QFont("Arial", 36, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #FFFFFF;")
        main.addWidget(title)

        # Untertitel
        subtitle = QLabel("Alle deine Wallets und aktuellen Kontostände")
        subtitle.setFont(QFont("Arial", 18))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #BBBBBB; margin-bottom: 10px;")
        main.addWidget(subtitle)

        # Scrollbereich
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("border: none;")
        main.addWidget(self.scroll)

        content = QWidget()
        self.scroll.setWidget(content)

        self.list_layout = QVBoxLayout(content)
        self.list_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.list_layout.setSpacing(15)

        # Add Wallet Button
        add_wallet_btn = QPushButton("Neues Wallet erstellen")
        add_wallet_btn.setFixedHeight(50)
        add_wallet_btn.setStyleSheet("""
            QPushButton {
                background-color: #5B5CF0;
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

        # Daten laden
        self.load_wallets()

    # ------------------------------------------------------------
    # WALLETS LADEN
    # ------------------------------------------------------------
    def load_wallets(self):
        # Alte Widgets entfernen
        for i in reversed(range(self.list_layout.count())):
            self.list_layout.itemAt(i).widget().deleteLater()

        if not self.user_id:
            label = QLabel("Fehler: Keine User-ID übergeben.")
            label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
            label.setStyleSheet("color: red; margin-top: 40px;")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.list_layout.addWidget(label)
            return

        wallets = get_wallets_by_user(self.user_id)
        if not wallets:
            info = QLabel("Du hast noch keine Wallets.")
            info.setFont(QFont("Arial", 20))
            info.setStyleSheet("color: #AAAAAA; margin-top: 30px;")
            info.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.list_layout.addWidget(info)
            return

        # Wallets durchgehen
        for w in wallets:
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

            name = w.get("name", "Unbekanntes Wallet")
            currency = w.get("currency", "EUR")
            wallet_id = str(w["_id"])

            # Kontostand neu berechnen
            balance = calculate_wallet_balance(wallet_id)

            name_lbl = QLabel(name)
            name_lbl.setFont(QFont("Arial Black", 26))
            name_lbl.setStyleSheet("color: white;")
            layout.addWidget(name_lbl, 2)

            balance_lbl = QLabel(f"{balance:.2f} {currency}")
            balance_lbl.setFont(QFont("Arial", 24))
            balance_lbl.setStyleSheet("color: #7B87F9;")
            layout.addWidget(balance_lbl, 1)

            id_lbl = QLabel(f"ID: {wallet_id}")
            id_lbl.setFont(QFont("Arial", 14))
            id_lbl.setStyleSheet("color: #888888;")
            layout.addWidget(id_lbl, 2)

            self.list_layout.addWidget(card)

    # ------------------------------------------------------------
    # WALLET HINZUFÜGEN
    # ------------------------------------------------------------
    def add_wallet(self):
        if not self.user_id:
            QMessageBox.critical(self, "Fehler", "Keine Benutzer-ID übergeben.")
            return

        new_name = f"Wallet {len(get_wallets_by_user(self.user_id)) + 1}"
        try:
            create_wallet(self.user_id, new_name, 0.0)
            QMessageBox.information(self, "Erfolg", f"{new_name} wurde erstellt!")
            self.load_wallets()
        except Exception as e:
            QMessageBox.critical(self, "Fehler", f"Wallet konnte nicht erstellt werden:\n{e}")


# ------------------------------------------------------------
# TESTSTART
# ------------------------------------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    test_user_id = "674ff8b16e7b59e0c0b57d82"  # Beispiel-ID aus DB
    win = WalletsWindow(user_id=test_user_id)
    win.show()
    sys.exit(app.exec())
