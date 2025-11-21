"""
ui_dashboard.py
---------------
Dummy-Dashboard-View für das MVP.
Zuständig für die Darstellung der Dashboard-Informationen.
"""

from typing import Final


# Konstanten
DEFAULT_DUMMY_BALANCE: Final[float] = 30.0


def calculate_balance(user_id: int) -> float:
    """
    Returns a dummy balance for a given user.

    Args:
        user_id (int): The user identifier.

    Returns:
        float: Dummy balance value.
    """
    # TODO: Replace with real controller logic
    print("(Dummy-Controller) Balance calculated")
    return DEFAULT_DUMMY_BALANCE


def show_dashboard(user_id: int) -> None:
    """
    Displays the dashboard screen for the given user.

    Args:
        user_id (int): The user identifier.

    Returns:
        None
    """
    print("\n====== DASHBOARD ======\n")
    print(f"User: {user_id}")

    balance = calculate_balance(user_id)

    print(f"Balance: {balance} €\n")
