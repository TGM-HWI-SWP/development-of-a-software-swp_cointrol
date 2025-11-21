# main_controller.py
# -------------------
# Verbindet VIEW (ui_login/ui_dashboard) mit dem MODEL (database)

from model.database import (
    get_all_users,
    get_wallets_by_user,
    get_transactions_by_wallet,
    calculate_wallet_balance,
)


# ---------------------------------------------------------
# Login-Controller
# ---------------------------------------------------------

def login(username: str, password: str) -> int:
    """
    Simuliert ein Login, indem geprüft wird,
    ob ein Benutzer mit dem Namen existiert.
    Für das MVP keine Passwortprüfung.
    """
    users = get_all_users()

    for u in users:
        if u.name.lower() == username.lower():
            print(f"[Controller] Login OK für User: {u.name}")
            return u.user_id

    print("[Controller] Login fehlgeschlagen!")
    return -1


# ---------------------------------------------------------
# Dashboard-Controller
# ---------------------------------------------------------

def get_user_balance(user_id: int) -> float:
    """
    Berechnet die Summe aller Wallet-Balances eines Users.
    """
    wallets = get_wallets_by_user(user_id)
    total = 0.0

    for w in wallets:
        total += calculate_wallet_balance(w.wallet_id)

    return total


def get_wallet_details(user_id: int):
    """
    Liefert alle Wallets + Transaktionen eines Users zurück.
    """
    wallets = get_wallets_by_user(user_id)
    data = []

    for w in wallets:
        transactions = get_transactions_by_wallet(w.wallet_id)
        wallet_info = {
            "wallet": w,
            "transactions": transactions,
            "balance": calculate_wallet_balance(w.wallet_id)
        }
        data.append(wallet_info)

    return data
