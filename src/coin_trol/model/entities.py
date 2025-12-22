"""
entities.py
-----------
Dieses Modul enthält alle Entitäten (Model-Klassen) für das CoinTrol-Projekt.
Diese Klassen bilden die logische Datenstruktur für Benutzer, Wallets und Transaktionen.

Jede Klasse ist eine einfache Python-Datenstruktur (POJO – Plain Old Python Object),
die später direkt an eine echte Datenbank angebunden werden kann.

Enthaltene Klassen:
 - User
 - Wallet
 - Transaction

Styleguide: PEP 8, Google-Style Docstrings
"""


# BENÖTIGTE IMPORTS
from datetime import datetime  # für Zeitstempel in User- und Transaktionsobjekten



# KLASSE: USER
class User:
    """
    Repräsentiert einen Benutzer im CoinTrol-System.

    Diese Klasse modelliert die Basisinformationen eines Nutzers,
    der sich in der App registriert oder anmeldet.

    Attributes:
        user_id (int): Eindeutige ID des Benutzers.
        name (str): Benutzername (Anzeigename).
        email (str): E-Mail-Adresse des Benutzers.
        created_at (datetime): Zeitpunkt der Kontoerstellung.
    """

    def __init__(self, user_id: int, name: str, email: str, created_at: datetime | None = None) -> None:
        """
        Konstruktor für das User-Objekt.
        Erstellt ein neues Benutzerobjekt mit ID, Namen und E-Mail-Adresse.

        Args:
            user_id (int): Eindeutige Benutzer-ID (z. B. 1, 2, 3...).
            name (str): Name des Benutzers.
            email (str): E-Mail-Adresse.
            created_at (datetime | None): Zeitpunkt der Erstellung (optional).
                                          Wenn kein Datum angegeben wird, wird das aktuelle Datum verwendet.
        """
        # Speichert eindeutige Benutzer-ID (Primärschlüssel)
        self.user_id = user_id

        # Name und E-Mail als Zeichenketten
        self.name = name
        self.email = email

        # Wenn kein Erstellungszeitpunkt übergeben wurde → jetzt
        self.created_at = created_at or datetime.now()

    def __repr__(self) -> str:
        """
        Gibt eine kurze, lesbare Textdarstellung des Benutzers zurück.
        Wird z. B. in print() oder Debug-Ausgaben angezeigt.

        Returns:
            str: Repräsentation in der Form "User(id=1, name='Ivan', email='ivan@...')"
        """
        return f"User(id={self.user_id}, name='{self.name}', email='{self.email}')"



# KLASSE: WALLET
class Wallet:
    """
    Repräsentiert ein Wallet (Konto) eines Benutzers.

    Ein Wallet enthält immer einen Bezug zu einem Benutzer (user_id),
    eine Bezeichnung und den aktuellen Kontostand.

    Attributes:
        wallet_id (int): Eindeutige ID des Wallets.
        user_id (int): ID des Benutzers, dem das Wallet gehört (Fremdschlüssel).
        name (str): Anzeigename des Wallets.
        balance (float): Aktueller Kontostand.
        currency (str): Währung (Standard: EUR).
    """

    def __init__(self, wallet_id: int, user_id: int, name: str, balance: float = 0.0, currency: str = "EUR") -> None:
        """
        Initialisiert ein neues Wallet-Objekt.

        Args:
            wallet_id (int): Wallet-ID (eindeutige Kennung).
            user_id (int): Benutzer-ID, der das Wallet gehört.
            name (str): Name oder Bezeichnung des Wallets.
            balance (float, optional): Anfangssaldo (Standardwert 0.0).
            currency (str, optional): Währung (Standardwert 'EUR').
        """
        # Wallet-ID als eindeutiger Schlüssel
        self.wallet_id = wallet_id

        # Fremdschlüssel-Beziehung zum Benutzer
        self.user_id = user_id

        # Name für GUI-Anzeige und Identifikation
        self.name = name

        # Kontostand in der gewählten Währung
        self.balance = balance

        # Währungscode (ISO-konform, z. B. EUR, USD, RSD)
        self.currency = currency

    def __repr__(self) -> str:
        """
        Gibt eine kompakte Textdarstellung des Wallets zurück.

        Returns:
            str: Darstellung im Format "Wallet('Ivan Main', 325.50 EUR)"
        """
        return f"Wallet('{self.name}', {self.balance:.2f} {self.currency})"



# KLASSE: TRANSACTION
class Transaction:
    """
    Repräsentiert eine einzelne Transaktion (Geldbewegung) innerhalb eines Wallets.

    Jede Transaktion gehört zu genau einem Wallet und enthält Betrag, Kategorie,
    Datum und eine optionale Beschreibung.

    Attributes:
        transaction_id (int): Eindeutige ID der Transaktion.
        wallet_id (int): Zugehörige Wallet-ID (Fremdschlüssel).
        amount (float): Betrag der Transaktion (+ Einnahme / - Ausgabe).
        category (str): Kategorie der Transaktion (z. B. 'Food', 'Salary', 'Transport').
        date (datetime): Zeitpunkt der Transaktion.
        description (str): Beschreibung oder kurze Notiz.
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
        """
        Initialisiert eine neue Transaktion.

        Args:
            transaction_id (int): Eindeutige ID der Transaktion.
            wallet_id (int): ID des Wallets, zu dem die Transaktion gehört.
            amount (float): Betrag der Transaktion (positive Werte = Einnahmen, negative = Ausgaben).
            category (str): Kategoriebezeichnung (z. B. 'Food', 'Salary').
            date (datetime | None): Datum der Transaktion (Standard: aktuelles Datum).
            description (str): Optionale Beschreibung (z. B. 'Tankstelle').
        """
        # ID der Transaktion (Primärschlüssel)
        self.transaction_id = transaction_id

        # Zugehöriges Wallet (Fremdschlüssel)
        self.wallet_id = wallet_id

        # Betrag (float, positiv oder negativ)
        self.amount = amount

        # Kategorie der Transaktion (String)
        self.category = category

        # Beschreibungstext (kann leer bleiben)
        self.description = description

        # Datum – wenn keins angegeben, aktuelles Datum verwenden
        self.date = date or datetime.now()

    def __repr__(self) -> str:
        """
        Gibt eine formatierte Textdarstellung der Transaktion zurück.

        Diese Darstellung zeigt Datum, Kategorie und Betrag übersichtlich.
        Beispielausgabe:
            [03.12.2025] Salary: +1500.00€

        Returns:
            str: Kompakte Darstellung der Transaktion.
        """
        # Vorzeichen abhängig vom Betrag
        sign = "+" if self.amount > 0 else ""
        return f"[{self.date.strftime('%d.%m.%Y')}] {self.category}: {sign}{self.amount:.2f}€"