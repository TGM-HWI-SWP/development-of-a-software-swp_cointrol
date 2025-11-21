"""
entities.py
-----------
Beinhaltet alle Entity-Klassen (Modelle) für das CoinTrol-Projekt:
- User
- Wallet
- Transaction

Styleguide: PEP 8, Google-Style Docstrings
"""

from datetime import datetime


class User:
    """Repräsentiert einen Benutzer im CoinTrol-System.

    Attributes:
        user_id (int): Eindeutige ID des Benutzers.
        name (str): Name des Benutzers.
        email (str): E-Mail-Adresse des Benutzers.
        created_at (datetime): Zeitpunkt der Erstellung des Benutzerkontos.
    """

    def __init__(self, user_id: int, name: str, email: str, created_at: datetime | None = None) -> None:
        """Initialisiert ein neues User-Objekt.

        Args:
            user_id (int): Eindeutige Benutzer-ID.
            name (str): Name des Benutzers.
            email (str): E-Mail-Adresse.
            created_at (datetime | None): Zeitpunkt der Erstellung (optional).
        """
        self.user_id = user_id
        self.name = name
        self.email = email
        self.created_at = created_at or datetime.now()

    def __repr__(self) -> str:
        """Gibt eine lesbare Darstellung des Benutzers zurück."""
        return f"User(id={self.user_id}, name='{self.name}', email='{self.email}')"


class Wallet:
    """Repräsentiert ein Wallet (Konto) eines Benutzers.

    Attributes:
        wallet_id (int): Eindeutige ID des Wallets.
        user_id (int): Zugehöriger Benutzer (Fremdschlüssel).
        name (str): Anzeigename des Wallets.
        balance (float): Aktueller Kontostand.
        currency (str): Währung des Wallets (Standard: EUR).
    """

    def __init__(self, wallet_id: int, user_id: int, name: str, balance: float = 0.0, currency: str = "EUR") -> None:
        """Initialisiert ein Wallet-Objekt.

        Args:
            wallet_id (int): Wallet-ID.
            user_id (int): Zugehöriger Benutzer.
            name (str): Wallet-Name.
            balance (float): Anfangssaldo (optional, Standard: 0.0).
            currency (str): Währung (Standard: EUR).
        """
        self.wallet_id = wallet_id
        self.user_id = user_id
        self.name = name
        self.balance = balance
        self.currency = currency

    def __repr__(self) -> str:
        """Gibt eine formatierte Darstellung des Wallets zurück."""
        return f"Wallet('{self.name}', {self.balance:.2f} {self.currency})"


class Transaction:
    """Repräsentiert eine einzelne Transaktion im CoinTrol-System.

    Attributes:
        transaction_id (int): Eindeutige ID der Transaktion.
        wallet_id (int): Zugehöriges Wallet.
        amount (float): Betrag (+ Einnahme / - Ausgabe).
        category (str): Kategorie der Transaktion (z. B. 'Food', 'Salary').
        date (datetime): Datum der Transaktion.
        description (str): Beschreibung oder Notiz.
    """

    def __init__(
        self,
        transaction_id: int,
        wallet_id: int,
        amount: float,
        category: str,
        date: datetime | None = None,
        description: str = "",
    ) -> None:
        """Initialisiert ein Transaction-Objekt.

        Args:
            transaction_id (int): ID der Transaktion.
            wallet_id (int): Zugehöriges Wallet.
            amount (float): Betrag der Transaktion.
            category (str): Kategorie (z. B. 'Food', 'Salary').
            date (datetime | None): Datum (optional, Standard: aktuelles Datum).
            description (str): Beschreibung (optional).
        """
        self.transaction_id = transaction_id
        self.wallet_id = wallet_id
        self.amount = amount
        self.category = category
        self.description = description
        self.date = date or datetime.now()

    def __repr__(self) -> str:
        """Gibt eine kompakte Textdarstellung der Transaktion zurück."""
        sign = "+" if self.amount > 0 else ""
        return f"[{self.date.strftime('%d.%m.%Y')}] {self.category}: {sign}{self.amount:.2f}€"