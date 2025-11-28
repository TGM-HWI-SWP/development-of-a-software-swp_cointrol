"""
database.py
------------
Beinhaltet Dummy-Daten und Basisfunktionen (Stubs) für das CoinTrol-Projekt.
Dient als Platzhalter für zukünftige Datenbankanbindung (z. B. SQLite oder MySQL).
"""

from datetime import datetime
from .entities import User, Wallet, Transaction

# =====================================================
# DUMMY-DATEN (vorläufig, bis echte DB implementiert ist)
# =====================================================

# --- Benutzer ---
USERS = [
    User(1, "Ivan", "ivan@cointrol.at"),
    User(2, "Gabriel", "gabriel@cointrol.at"),
    User(3, "Aleksej", "aleksej@cointrol.at"),
]

# --- Wallets ---
WALLETS = [
    Wallet(1, 1, "Ivan Main", 325.50),
    Wallet(2, 2, "Gabriel Wallet", 780.00),
    Wallet(3, 3, "Aleksej Wallet", 120.25),
]

# --- Transaktionen ---
TRANSACTIONS = [
    Transaction(1, 1, +1500.0, "Salary", datetime(2025, 11, 1), "Monthly salary"),
    Transaction(2, 1, -45.5, "Groceries", datetime(2025, 11, 2), "Spar Einkauf"),
    Transaction(3, 1, -20.0, "Transport", datetime(2025, 11, 3), "Wiener Linien Monatskarte"),
    Transaction(4, 2, +2000.0, "Salary", datetime(2025, 11, 1), "Full-time job"),
    Transaction(5, 2, -150.0, "Electronics", datetime(2025, 11, 2), "New keyboard"),
    Transaction(6, 3, +300.0, "Gift", datetime(2025, 11, 1), "Birthday money"),
    Transaction(7, 3, -50.0, "Food", datetime(2025, 11, 3), "McDonalds"),
]

# =====================================================
# STUB-FUNKTIONEN (API zwischen Controller und Model)
# =====================================================

def get_all_users():
    """
    Gibt alle Benutzer zurück.
    Returns:
        list[User]: Liste aller Benutzerobjekte.
    """
    return USERS


def get_wallets_by_user(user_id: int):
    """
    Gibt alle Wallets eines bestimmten Benutzers zurück.
    Args:
        user_id (int): ID des Benutzers.
    Returns:
        list[Wallet]: Liste der Wallets des Benutzers.
    """
    return [w for w in WALLETS if w.user_id == user_id]


def get_transactions_by_wallet(wallet_id: int):
    """
    Gibt alle Transaktionen eines bestimmten Wallets zurück.
    Args:
        wallet_id (int): ID des Wallets.
    Returns:
        list[Transaction]: Liste der Transaktionen.
    """
    return [t for t in TRANSACTIONS if t.wallet_id == wallet_id]


def add_transaction(wallet_id: int, amount: float, category: str, description: str = ""):
    """
    Fügt eine neue Dummy-Transaktion hinzu.
    Args:
        wallet_id (int): ID des Wallets, dem die Transaktion zugeordnet wird.
        amount (float): Betrag der Transaktion (positiv = Einnahme, negativ = Ausgabe).
        category (str): Kategorie (z. B. 'Food', 'Salary').
        description (str): Optionale Beschreibung.
    Returns:
        Transaction: Das neu erstellte Transaktionsobjekt.
    """
    new_id = len(TRANSACTIONS) + 1
    t = Transaction(new_id, wallet_id, amount, category, datetime.now(), description)
    TRANSACTIONS.append(t)
    return t


def calculate_wallet_balance(wallet_id: int):
    """
    Berechnet den aktuellen Kontostand auf Basis der Dummy-Transaktionen.
    Args:
        wallet_id (int): ID des Wallets.
    Returns:
        float: Summe aller Transaktionen für dieses Wallet.
    """
    transactions = get_transactions_by_wallet(wallet_id)
    total = sum(t.amount for t in transactions)
    return total
