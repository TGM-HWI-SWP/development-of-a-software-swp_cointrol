# main_controller.py
# -------------------
# Verbindet VIEW (ui_login/ui_dashboard) mit dem MODEL (db_interface)

from coin_trol.model.db_interface import (
    get_user_by_login,
    create_user,
    create_wallet,
    add_transaction,
    get_wallets_by_user,
    get_transactions_by_wallet,
    calculate_wallet_balance,
    update_wallet_balance,
    delete_transaction,
)

# ---------------------------------------------------------
# LOGIN
# ---------------------------------------------------------

def login(username: str, password: str) -> str | None:
    """
    Prüft den Login gegen MongoDB.
    Gibt die Benutzer-ID als String zurück, falls erfolgreich.
    """
    user_id = get_user_by_login(username, password)

    if user_id:
        print(f"[Controller] Login erfolgreich – User-ID: {user_id}")
        return user_id
    else:
        print("[Controller] Login fehlgeschlagen!")
        return None


# ---------------------------------------------------------
# DASHBOARD / WALLET
# ---------------------------------------------------------

def get_user_balance(user_id: str) -> float:
    """Berechnet die Summe aller Wallets eines Users."""
    wallets = get_wallets_by_user(user_id)
    total = 0.0
    for w in wallets:
        total += calculate_wallet_balance(str(w["_id"]))
    print(f"[Controller] Gesamtbalance: {total} €")
    return total


def get_wallet_details(user_id: str):
    """Liefert alle Wallets + Transaktionen eines Users."""
    wallets = get_wallets_by_user(user_id)
    data = []
    for w in wallets:
        wallet_id = str(w["_id"])
        transactions = get_transactions_by_wallet(wallet_id)
        wallet_info = {
            "wallet": w,
            "transactions": transactions,
            "balance": calculate_wallet_balance(wallet_id)
        }
        data.append(wallet_info)
    print(f"[Controller] {len(data)} Wallets geladen.")
    return data


# ---------------------------------------------------------
# CRUD-FUNKTIONEN
# ---------------------------------------------------------

def add_new_transaction(wallet_id: str, amount: float, category: str, description: str = ""):
    """Fügt über den Controller eine Transaktion hinzu."""
    trans_id = add_transaction(wallet_id, amount, category, description)
    new_balance = calculate_wallet_balance(wallet_id)
    print(f"[Controller] Neue Transaktion {trans_id} hinzugefügt. Neuer Kontostand: {new_balance} €")
    return trans_id


def remove_transaction(transaction_id: str):
    """Löscht eine Transaktion."""
    success = delete_transaction(transaction_id)
    print(f"[Controller] Transaktion gelöscht: {success}")
    return success
