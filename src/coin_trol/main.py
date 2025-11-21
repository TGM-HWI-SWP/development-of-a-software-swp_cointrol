"""
main.py
-------
Entry point for the CoinTrol MVP.
Executes the login process and displays the dashboard.
"""

from view.ui_login import login_screen
from view.ui_dashboard import show_dashboard


def main() -> None:
    """
    Runs the login process and displays the dashboard.

    Returns:
        None
    """
    user_id = login_screen()
    show_dashboard(user_id)


if __name__ == "__main__":
    main()
