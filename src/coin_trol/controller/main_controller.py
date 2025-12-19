# main_controller.py
# ------------------
# Verbindet VIEW mit MODEL (Database)

from model.database import (
    get_all_users,
    get_wallets_by_user,
    get_transactions_by_wallet,
    calculate_wallet_balance,
)

# --------------------------------------------------------
# Login-Controller
# --------------------------------------------------------

def login(username: str, password: str) -> int:
    """
    Prüft, ob ein Benutzer mit dem Namen existiert.
    Passwort wird im MVP ignoriert.
    """
    users = get_all_users()

    for user in users:
        if user.name.lower() == username.lower():
            print("[Controller] Login erfolgreich:", user.name)
            return user.user_id

    print("[Controller] Login fehlgeschlagen")
    return -1


# --------------------------------------------------------
# Dashboard-Controller
# --------------------------------------------------------

def get_user_balance(user_id: int) -> float:
    """
    Gibt das Gesamtguthaben aller Wallets eines Users zurück.
    """
    wallets = get_wallets_by_user(user_id)
    balance = 0.0

    for wallet in wallets:
        balance += calculate_wallet_balance(wallet.wallet_id)

    return balance


def get_wallet_details(user_id: int) -> list:
    """
    Gibt alle Wallets inkl. Transaktionen und Kontostand zurück.
    """
    wallets = get_wallets_by_user(user_id)
    result = []

    for wallet in wallets:
        wallet_data = {
            "wallet": wallet,
            "transactions": get_transactions_by_wallet(wallet.wallet_id),
            "balance": calculate_wallet_balance(wallet.wallet_id)
        }
        result.append(wallet_data)

    return result
