# main_controller.py
# -------------------
# Verbindet VIEW (ui_login/ui_dashboard) mit dem MODEL (database)

from typing import List, Dict, Any
from model.database import (
    get_all_users,
    get_wallets_by_user,
    get_transactions_by_wallet,
    calculate_wallet_balance,
)
import logging

# Logging konfigurieren
logging.basicConfig(level=logging.INFO, format='[Controller] %(message)s')


# ---------------------------------------------------------
# Login-Controller
# ---------------------------------------------------------

def login(username: str, password: str = "") -> int:
    """
    Simuliert ein Login, indem geprüft wird,
    ob ein Benutzer mit dem Namen existiert.
    Für das MVP keine Passwortprüfung.
    
    :param username: Benutzername
    :param password: Passwort (derzeit ungenutzt)
    :return: user_id oder -1 bei Fehlschlag
    """
    users = get_all_users()
    user = next((u for u in users if u.name.lower() == username.lower()), None)

    if user:
        logging.info(f"Login OK für User: {user.name}")
        return user.user_id
    else:
        logging.warning("Login fehlgeschlagen!")
        return -1


# ---------------------------------------------------------
# Dashboard-Controller
# ---------------------------------------------------------

def get_user_balance(user_id: int) -> float:
    """
    Berechnet die Summe aller Wallet-Balances eines Users.

    :param user_id: ID des Users
    :return: Gesamtsaldo aller Wallets
    """
    wallets = get_wallets_by_user(user_id)
    total_balance = sum(calculate_wallet_balance(w.wallet_id) for w in wallets)
    logging.info(f"Gesamtbalance für User {user_id}: {total_balance}")
    return total_balance


def get_wallet_details(user_id: int) -> List[Dict[str, Any]]:
    """
    Liefert alle Wallets + Transaktionen eines Users zurück.

    :param user_id: ID des Users
    :return: Liste von Dicts mit Wallet, Transactions und Balance
    """
    wallets = get_wallets_by_user(user_id)
    wallet_data = []

    for w in wallets:
        transactions = get_transactions_by_wallet(w.wallet_id)
        wallet_data.append({
            "wallet": w,
            "transactions": transactions,
            "balance": calculate_wallet_balance(w.wallet_id)
        })

    logging.info(f"Wallet-Details für User {user_id} geladen: {len(wallet_data)} Wallet(s)")
    return wallet_data
