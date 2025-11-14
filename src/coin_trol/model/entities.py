# ==============================
# CoinTrol – Entity Classes
# ==============================

"""
entities.py
-----------
Beinhaltet alle Entity-Klassen (Modelle) für das CoinTrol-Projekt:
- User
- Wallet
- Transaction
"""

from datetime import datetime


class User:
    """
    Repräsentiert einen Benutzer im CoinTrol-System.

    Attributes:
        user_id (int): Eindeutige ID des Benutzers.
        name (str): Name des Benutzers.
        email (str): E-Mail-Adresse des Benutzers.
        created_at (datetime): Zeitpunkt der Erstellung des Benutzerkontos.
    """

    def __init__(self, user_id: int, name: str, email: str, created_at: datetime = None):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.created_at = created_at or datetime.now()

    def __repr__(self):
        """Gibt eine lesbare Darstellung des Benutzers zurück."""
        return f"User({self.user_id}, {self.name}, {self.email})"


class Wallet:
    """
    Repräsentiert ein Wallet (Konto) eines Benutzers.

    Attributes:
        wallet_id (int): Eindeutige ID des Wallets.
        user_id (int): Zugehöriger Benutzer (Fremdschlüssel).
        name (str): Anzeigename des Wallets.
        balance (float): Aktueller Kontostand.
        currency (str): Währung des Wallets (Standard: EUR).
    """

    def __init__(self, wallet_id: int, user_id: int, name: str, balance: float = 0.0, currency: str = "EUR"):
        self.wallet_id = wallet_id
        self.user_id = user_id
        self.name = name
        self.balance = balance
        self.currency = currency

    def __repr__(self):
        """Gibt eine lesbare Darstellung des Wallets zurück."""
        return f"Wallet({self.name}, {self.balance:.2f} {self.currency})"


class Transaction:
    """
    Repräsentiert eine einzelne Transaktion im CoinTrol-System.

    Attributes:
        transaction_id (int): Eindeutige ID der Transaktion.
        wallet_id (int): Zugehöriges Wallet.
        amount (float): Betrag (+ Einnahme / - Ausgabe).
        category (str): Kategorie der Transaktion (z. B. 'Food', 'Salary').
        date (datetime): Datum der Transaktion.
        description (str): Kurze Beschreibung oder Notiz.
    """

    def __init__(self, transaction_id: int, wallet_id: int, amount: float, category: str, date: datetime = None, description: str = ""):
        self.transaction_id = transaction_id
        self.wallet_id = wallet_id
        self.amount = amount
        self.category = category
        self.description = description
        self.date = date or datetime.now()

    def __repr__(self):
        """Gibt eine kompakte Textdarstellung der Transaktion zurück."""
        sign = "+" if self.amount > 0 else ""
        return f"[{self.date.strftime('%d.%m.%Y')}] {self.category}: {sign}{self.amount:.2f}€"
