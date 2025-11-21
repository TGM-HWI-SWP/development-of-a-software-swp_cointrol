# src/coin_trol/main.py
"""
main.py
-------
Startpunkt der Anwendung (MVP).
"""

from view.ui_login import login_screen
from view.ui_dashboard import show_dashboard


def main() -> None:
    """Führt Login und Dashboard in der richtigen Reihenfolge aus."""
    user_id = login_screen()
    show_dashboard(user_id)


if __name__ == "__main__":
    main()
