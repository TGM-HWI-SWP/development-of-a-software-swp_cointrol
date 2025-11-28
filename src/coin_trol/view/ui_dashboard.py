"""
ui_dashboard.py
---------------
Dummy-Dashboard-View für das MVP (Woche 2–4).
Zuständig für die Darstellung der Dashboard-Informationen.
"""

from typing import Final

# -------------------------------------------------
# Konstanten
# -------------------------------------------------
DEFAULT_DUMMY_BALANCE: Final[float] = 30.0


# -------------------------------------------------
# Funktionen
# -------------------------------------------------
def calculate_balance(user_id: int) -> float:
    """
    Dummy-Funktion, die eine feste Balance für den Benutzer zurückgibt.

    Args:
        user_id (int): Die ID des Benutzers.

    Returns:
        float: Der berechnete (Dummy-)Kontostand.
    """
    # TODO: Später echte Controller-Logik aufrufen
    print("(Dummy-Controller) Balance berechnet")
    return DEFAULT_DUMMY_BALANCE


def show_dashboard(user_id: int) -> None:
    """
    Zeigt das Dashboard für den angegebenen Benutzer.

    Args:
        user_id (int): Die ID des Benutzers.

    Returns:
        None
    """
    print("\n====== DASHBOARD ======\n")
    print(f"Benutzer-ID: {user_id}")

    balance = calculate_balance(user_id)

    print(f"Aktueller Kontostand: {balance:.2f} €")
    print("========================\n")
