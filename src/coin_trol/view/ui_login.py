# src/coin_trol/view/ui_login.py
"""
ui_login.py
-----------
Dummy-Login-Screen für das MVP (Woche 2).
"""

def get_user_id_by_login(username: str, password: str) -> int:
    """Dummy-Funktion, die später durch echte Controller-Logik ersetzt wird."""
    print("(Dummy-Controller) Login überprüft")
    return 1


def login_screen() -> int:
    """Zeigt den Login-Screen an und gibt eine Dummy-User-ID zurück."""
    print("\n====== LOGIN ======\n")

    username = "testuser"
    password = "1234"

    print(f"Benutzer: {username}")
    print("Passwort: ****")

    user_id = get_user_id_by_login(username, password)

    print(f"\nLogin erfolgreich! (User-ID: {user_id})\n")
    return user_id
