<<<<<<< HEAD
# src/coin_trol/main.py
"""
main.py
-------
Startpunkt der Anwendung (MVP).
=======
"""
main.py
-------
Entry point for the CoinTrol MVP.
Executes the login process and displays the dashboard.
>>>>>>> origin/view
"""

from view.ui_login import login_screen
from view.ui_dashboard import show_dashboard


def main() -> None:
<<<<<<< HEAD
    """Führt Login und Dashboard in der richtigen Reihenfolge aus."""
=======
    """
    Runs the login process and displays the dashboard.

    Returns:
        None
    """
>>>>>>> origin/view
    user_id = login_screen()
    show_dashboard(user_id)


if __name__ == "__main__":
    main()
