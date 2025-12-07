from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QGridLayout, QFrame, QScrollArea
)
from PyQt6.QtGui import QFont, QColor, QPalette
from PyQt6.QtCore import Qt
import sys

# ------------------------------------------------------------
# IMPORTS AUS CONTROLLER UND VIEW
# ------------------------------------------------------------
from coin_trol.model.db_interface import (
    get_wallets_by_user,
    create_wallet,
    calculate_wallet_balance,
    get_transactions_by_wallet
)
from coin_trol.view.Transaktion import TransactionWindow
from coin_trol.view.Wallets import WalletsWindow


# ------------------------------------------------------------
# DASHBOARD-FENSTER
# ------------------------------------------------------------
class DashboardWindow(QWidget):
    def __init__(self, username="TestUser", on_logout=None, user_id=None):
        super().__init__()

        self.username = username
        self.user_id = user_id
        self.on_logout = on_logout
        self.wallet_id = None

        # Fenster Setup
        self.setWindowTitle("CoinTrol – Dashboard")
        self.resize(1280, 800)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#262626"))
        self.setPalette(palette)

        SIDEBAR_BG = "#1E1F26"
        CARD_BG = "#3A3A42"

        # ---------------------------------------------------
        # HAUPTLAYOUT
        # ---------------------------------------------------
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(15)

        # ---------------------------------------------------
        # SIDEBAR
        # ---------------------------------------------------
        sidebar = QFrame()
        sidebar.setFixedWidth(240)
        sidebar.setStyleSheet(f"background-color: {SIDEBAR_BG}; border-radius: 14px;")

        side_layout = QVBoxLayout(sidebar)
        side_layout.setContentsMargins(20, 20, 20, 20)
        side_layout.setSpacing(40)

        title = QLabel("CoinTrol")
        title.setFont(QFont("Arial", 36, QFont.Weight.Bold))
        title.setStyleSheet("color: white;")
        side_layout.addWidget(title)

        user_label = QLabel(f"Angemeldet als:\n{username}")
        user_label.setFont(QFont("Arial", 16))
        user_label.setStyleSheet("color: #CFCFCF;")
        side_layout.addWidget(user_label)
        side_layout.addSpacing(20)

        # BUTTONS
        buttons = {
            "Dashboard": None,
            "Transaktionen": self.open_transactions,
            "Wallets": self.open_wallet,
        }

        for name, action in buttons.items():
            btn = QPushButton(name)
            btn.setFixedHeight(65)
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
            if action:
                btn.clicked.connect(action)
            side_layout.addWidget(btn)

        side_layout.addStretch()

        logout_btn = QPushButton("Logout")
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
        logout_btn.clicked.connect(self.logout)
        side_layout.addWidget(logout_btn)

        main_layout.addWidget(sidebar)

        # ---------------------------------------------------
        # CONTENT-BEREICH MIT VERTIKALEM SCROLLEN
        # ---------------------------------------------------
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
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
                background: #5B5CF0;
                border-radius: 5px;
                min-height: 25px;
            }
            QScrollBar::handle:vertical:hover {
                background: #7678FF;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0;
            }
        """)

        # Innerer Content
        content = QWidget()
        content.setStyleSheet("background-color: #2B2B2B; border-radius: 18px;")

        self.content_layout = QVBoxLayout(content)
        self.content_layout.setContentsMargins(30, 30, 30, 30)
        self.content_layout.setSpacing(20)

        header = QLabel("Dashboard Übersicht")
        header.setFont(QFont("Arial", 34, QFont.Weight.Bold))
        header.setStyleSheet("color: white;")
        header.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.content_layout.addWidget(header)

        # Daten laden
        self.load_dashboard(CARD_BG)

        scroll_area.setWidget(content)
        main_layout.addWidget(scroll_area)

    # ------------------------------------------------------------
    # LADEN DER WALLET- UND TRANSAKTIONSDATEN
    # ------------------------------------------------------------
    def load_dashboard(self, CARD_BG):
        """Lädt Daten des eingeloggten Benutzers aus MongoDB"""
        if not self.user_id:
            print("[Dashboard Fehler] Keine User-ID übergeben.")
            return

        wallets = get_wallets_by_user(self.user_id)
        if not wallets:
            print("[Dashboard] Kein Wallet gefunden → Erstelle 'Main Wallet'")
            wallet_id = create_wallet(self.user_id, "Main Wallet", 0.0)
            self.wallet_id = wallet_id
            balance = 0.0
            transactions = []
        else:
            main_wallet = wallets[0]
            self.wallet_id = str(main_wallet["_id"])
            balance = calculate_wallet_balance(self.wallet_id)
            transactions = get_transactions_by_wallet(self.wallet_id)

        # Überschrift mit Kontostand
        welcome = QLabel(f"Willkommen, {self.username} – aktueller Kontostand: {balance:.2f} €")
        welcome.setFont(QFont("Arial", 18))
        welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome.setStyleSheet("color: #CCCCCC; margin-top: 10px; margin-bottom: 20px;")
        self.content_layout.addWidget(welcome)

        # Karten (Kontostand, Ausgaben, Einnahmen)
        grid = QGridLayout()
        grid.setSpacing(20)

        expenses = sum(abs(t["amount"]) for t in transactions if t["amount"] < 0)
        income = sum(t["amount"] for t in transactions if t["amount"] > 0)

        cards = [
            ("Kontostand", f"{balance:.2f} €"),
            ("Monatsausgaben", f"{expenses:.2f} €"),
            ("Einnahmen", f"{income:.2f} €"),
        ]

        for i, (title_text, value_text) in enumerate(cards):
            card = QFrame()
            card.setStyleSheet(f"background-color: {CARD_BG}; border-radius: 18px;")
            card_layout = QVBoxLayout(card)
            card_layout.setSpacing(5)
            card_layout.setContentsMargins(20, 20, 20, 20)

            t = QLabel(title_text)
            t.setFont(QFont("Arial", 22))
            t.setStyleSheet("color: #D0D0D0;")
            t.setAlignment(Qt.AlignmentFlag.AlignHCenter)

            v = QLabel(value_text)
            v.setFont(QFont("Arial", 42, QFont.Weight.Bold))
            v.setStyleSheet("color: white;")
            v.setAlignment(Qt.AlignmentFlag.AlignHCenter)

            card_layout.addWidget(t)
            card_layout.addWidget(v)

            grid.addWidget(card, 0, i)

        self.content_layout.addLayout(grid)

        # Letzte Aktivitäten
        info_card = QFrame()
        info_card.setStyleSheet(f"background-color: {CARD_BG}; border-radius: 18px;")
        info_layout = QVBoxLayout(info_card)
        info_layout.setContentsMargins(25, 25, 25, 25)

        header2 = QLabel("Letzte Aktivitäten")
        header2.setFont(QFont("Arial", 26, QFont.Weight.Bold))
        header2.setStyleSheet("color: white;")
        info_layout.addWidget(header2)

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

    # ------------------------------------------------------------
    # TRANSAKTIONSFENSTER
    # ------------------------------------------------------------
    def open_transactions(self):
        if not self.wallet_id:
            print("[Fehler] Keine Wallet-ID übergeben – kann Transaktionsfenster nicht öffnen.")
            return
        self.trans_window = TransactionWindow(wallet_id=self.wallet_id, dashboard_ref=self)
        self.trans_window.show()

    # ------------------------------------------------------------
    # WALLET-FENSTER
    # ------------------------------------------------------------
    def open_wallet(self):
        self.wallet_window = WalletsWindow()
        self.wallet_window.show()

    # ------------------------------------------------------------
    # LOGOUT
    # ------------------------------------------------------------
    def logout(self):
        if self.on_logout:
            self.on_logout()
        self.close()


# ------------------------------------------------------------
# TESTSTART
# ------------------------------------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    test_user_id = "674ff8b16e7b59e0c0b57d82"
    win = DashboardWindow(username="kingivan", user_id=test_user_id)
    win.show()
    sys.exit(app.exec())
