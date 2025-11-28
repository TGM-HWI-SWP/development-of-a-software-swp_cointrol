"""
ui_login.py
-----------
Dummy-Login-View für das MVP (Woche 2–4).
Simuliert einen Login-Prozess und liefert eine Test-User-ID zurück.
"""

from typing import Final

# -------------------------------------------------
# Konstanten
# -------------------------------------------------
DEFAULT_DUMMY_USERNAME: Final[str] = "testuser"
DEFAULT_DUMMY_PASSWORD: Final[str] = "1234"
DEFAULT_DUMMY_USER_ID: Final[int] = 1


# -------------------------------------------------
# Funktionen
# -------------------------------------------------
def get_user_id_by_login(username: str, password: str) -> int:
    """
    Dummy-Funktion, die eine feste User-ID zurückgibt.

    Args:
        username (str): Benutzername.
        password (str): Passwort.

    Returns:
        int: Dummy-User-ID.
    """
    # TODO: Später Controller-Logik einfügen
    print("(Dummy-Controller) Login überprüft")
    return DEFAULT_DUMMY_USER_ID


def login_screen() -> int:
    """
    Zeigt den Login-Screen an und gibt eine Dummy-User-ID zurück.

    Returns:
        int: Die eingeloggte Benutzer-ID.
    """
    print("\n====== LOGIN ======\n")

    username = DEFAULT_DUMMY_USERNAME
    password = DEFAULT_DUMMY_PASSWORD

    print(f"Benutzername: {username}")
    print("Passwort: ****")

    user_id = get_user_id_by_login(username, password)

    print(f"\nLogin erfolgreich! (User-ID: {user_id})\n")

    return user_id
