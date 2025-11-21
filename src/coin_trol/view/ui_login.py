"""
ui_login.py
-----------
Dummy-Login-View für das MVP.
Simuliert einen Login-Prozess und liefert eine Test-User-ID.
"""

from typing import Final


# Konstanten
DEFAULT_DUMMY_USERNAME: Final[str] = "testuser"
DEFAULT_DUMMY_PASSWORD: Final[str] = "1234"
DEFAULT_DUMMY_USER_ID: Final[int] = 1


def get_user_id_by_login(username: str, password: str) -> int:
    """
    Returns a dummy user ID for testing purposes.

    Args:
        username (str): The username entered.
        password (str): The password entered.

    Returns:
        int: Dummy user ID.
    """
    # TODO: Replace with real controller logic
    print("(Dummy-Controller) Login checked")
    return DEFAULT_DUMMY_USER_ID


def login_screen() -> int:
    """
    Displays the login screen and returns a dummy user ID.

    Returns:
        int: The logged-in user ID.
    """
    print("\n====== LOGIN ======\n")

    username = DEFAULT_DUMMY_USERNAME
    password = DEFAULT_DUMMY_PASSWORD

    print(f"Username: {username}")
    print("Password: ****")

    user_id = get_user_id_by_login(username, password)

    print(f"\nLogin successful! (User-ID: {user_id})\n")
    return user_id
