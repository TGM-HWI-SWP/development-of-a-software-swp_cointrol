# src/coin_trol/view/ui_dashboard.py
"""
ui_dashboard.py
---------------
Dummy-Dashboard für das MVP (Woche 2).
"""

def calculate_balance(user_id: int) -> float:
    """Dummy-Funktion, die später echte Controller-Logik ersetzen wird."""
    print("(Dummy-Controller) Balance berechnet")
    return 30.0


def show_dashboard(user_id: int) -> None:
    """Zeigt den Dashboard-Screen mit Dummy-Daten."""
    print("\n====== DASHBOARD ======\n")
    print(f"User: {user_id}")

    balance = calculate_balance(user_id)

    print(f"Kontostand: {balance} €\n")
