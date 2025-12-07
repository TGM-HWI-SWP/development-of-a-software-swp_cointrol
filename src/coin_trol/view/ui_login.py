"""
ui_login.py
-----------
Login- und Registrierfenster für CoinTrol.
Verbindet sich mit MongoDB über den Controller.
"""

from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton,
    QFrame, QMessageBox, QHBoxLayout
)
from PyQt6.QtGui import QFont, QColor, QPalette
from PyQt6.QtCore import Qt
from coin_trol.controller.main_controller import login
from coin_trol.model.db_interface import create_user


class LoginWindow(QWidget):
    def __init__(self, on_login_success=None):
        super().__init__()
        self.on_login_success = on_login_success
        self.is_register_mode = False  # Start im Login-Modus

        self.setWindowTitle("CoinTrol – Login / Registrierung")
        self.resize(480, 500)

        # Hintergrundfarbe
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#1E1F26"))
        self.setPalette(palette)

        # Hauptlayout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(40, 40, 40, 40)
        self.layout.setSpacing(25)

        # UI aufbauen
        self._build_ui()

    # -------------------------------------------------------
    # GUI-Aufbau
    # -------------------------------------------------------
    def _build_ui(self):
        # Frame (Container)
        self.frame = QFrame()
        self.frame.setStyleSheet("background-color: #2A2B31; border-radius: 16px;")
        frame_layout = QVBoxLayout(self.frame)
        frame_layout.setContentsMargins(30, 30, 30, 30)
        frame_layout.setSpacing(20)

        # Titel
        self.title = QLabel("Anmeldung")
        self.title.setFont(QFont("Arial Black", 26))
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("color: white;")
        frame_layout.addWidget(self.title)

        # Benutzername
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Benutzername")
        self._style_input(self.username_input)
        frame_layout.addWidget(self.username_input)

        # E-Mail (nur bei Registrierung sichtbar)
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("E-Mail-Adresse")
        self._style_input(self.email_input)
        self.email_input.hide()
        frame_layout.addWidget(self.email_input)

        # Passwort
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Passwort")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self._style_input(self.password_input)
        frame_layout.addWidget(self.password_input)

        # Bestätigungs-Passwort (nur bei Registrierung sichtbar)
        self.password_confirm_input = QLineEdit()
        self.password_confirm_input.setPlaceholderText("Passwort bestätigen")
        self.password_confirm_input.setEchoMode(QLineEdit.EchoMode.Password)
        self._style_input(self.password_confirm_input)
        self.password_confirm_input.hide()
        frame_layout.addWidget(self.password_confirm_input)

        # Hauptaktion-Button
        self.action_btn = QPushButton("Einloggen")
        self.action_btn.setFixedHeight(45)
        self._style_button(self.action_btn, "#5B5CF0", "#6D6EFA")
        self.action_btn.clicked.connect(self._handle_action)
        frame_layout.addWidget(self.action_btn)

        # Umschalt-Button
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
        toggle_btn.clicked.connect(self._toggle_mode)
        toggle_layout.addWidget(toggle_label)
        toggle_layout.addWidget(toggle_btn)
        toggle_layout.addStretch()
        frame_layout.addLayout(toggle_layout)

        self.layout.addWidget(self.frame)

    # -------------------------------------------------------
    # LOGIN / REGISTRIERUNG Logik
    # -------------------------------------------------------
    def _handle_action(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        # ------------------------------
        # LOGIN
        # ------------------------------
        if not self.is_register_mode:
            if not username or not password:
                QMessageBox.warning(self, "Fehler", "Bitte Benutzername und Passwort eingeben.")
                return

            user_id = login(username, password)
            if user_id:
                QMessageBox.information(self, "Erfolg", f"Willkommen, {username}!")
                if self.on_login_success:
                    # Übergibt username + user_id an main.py
                    self.on_login_success(username, user_id)
                self.close()
            else:
                QMessageBox.critical(self, "Fehler", "Ungültige Anmeldedaten.")

        # ------------------------------
        # REGISTRIERUNG
        # ------------------------------
        else:
            email = self.email_input.text().strip()
            password_confirm = self.password_confirm_input.text().strip()

            if not username or not email or not password or not password_confirm:
                QMessageBox.warning(self, "Fehler", "Bitte alle Felder ausfüllen.")
                return

            if password != password_confirm:
                QMessageBox.warning(self, "Fehler", "Passwörter stimmen nicht überein.")
                return

            try:
                new_user_id = create_user(username, email, password)
                QMessageBox.information(
                    self,
                    "Erfolg",
                    f"Nutzer '{username}' wurde erfolgreich erstellt!\n"
                    f"(User-ID: {new_user_id})"
                )
                # Nach erfolgreicher Registrierung zurück zu Login
                self._toggle_mode()
                self.username_input.setText(username)
                self.password_input.clear()
                self.email_input.clear()
                self.password_confirm_input.clear()
            except Exception as e:
                QMessageBox.critical(self, "Fehler", f"Registrierung fehlgeschlagen:\n{e}")

    # -------------------------------------------------------
    # Modus wechseln (Login <-> Registrierung)
    # -------------------------------------------------------
    def _toggle_mode(self):
        self.is_register_mode = not self.is_register_mode
        if self.is_register_mode:
            self.title.setText("Registrierung")
            self.email_input.show()
            self.password_confirm_input.show()
            self.action_btn.setText("Registrieren")
        else:
            self.title.setText("Anmeldung")
            self.email_input.hide()
            self.password_confirm_input.hide()
            self.action_btn.setText("Einloggen")

    # -------------------------------------------------------
    # Styling-Helfer
    # -------------------------------------------------------
    def _style_input(self, widget):
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


# -------------------------------------------------------
# Direktstart (Test)
# -------------------------------------------------------
if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    win = LoginWindow()
    win.show()
    sys.exit(app.exec())
