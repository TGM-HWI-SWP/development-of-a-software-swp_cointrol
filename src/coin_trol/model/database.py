"""
database.py
------------
Dieses Modul enthält Dummy-Daten und einfache Funktionen (Stubs), 
um die grundlegende Datenlogik der CoinTrol-App zu simulieren.

Es dient als Platzhalter, bis eine echte Datenbank (z. B. SQLite oder MongoDB)
integriert wird. 
Alle Daten (Benutzer, Wallets, Transaktionen) liegen hier in Form
einfacher Python-Listen vor.

Styleguide: PEP 8, Google-Style Docstrings
"""

# -------------------------------------------------------------
# BENÖTIGTE IMPORTS
# -------------------------------------------------------------
from datetime import datetime  # für Zeitstempel in Transaktionen
from .entities import User, Wallet, Transaction  # Import eigener Klassen (Model-Ebene)

# ===================================================================
# DUMMY-DATEN (werden zur Laufzeit im RAM gehalten, keine DB-Verbindung)
# ===================================================================

# -------------------------------------------------------------
# BENUTZER (User)
# -------------------------------------------------------------
# Diese Liste simuliert eine Tabelle mit Benutzerkonten.
# Jeder User hat eine ID, einen Namen und eine E-Mail-Adresse.
USERS: list[User] = [
    User(1, "Ivan", "ivan@cointrol.at"),        # Benutzer 1
    User(2, "Gabriel", "gabriel@cointrol.at"),  # Benutzer 2
    User(3, "Aleksej", "aleksej@cointrol.at"),  # Benutzer 3
]

# -------------------------------------------------------------
# WALLETS (Konten)
# -------------------------------------------------------------
# Diese Liste repräsentiert alle vorhandenen Wallets.
# Jedes Wallet gehört genau einem Benutzer (user_id) und hat ein Startguthaben.
WALLETS: list[Wallet] = [
    Wallet(1, 1, "Ivan Main", 325.50),         # Wallet von Ivan
    Wallet(2, 2, "Gabriel Wallet", 780.00),    # Wallet von Gabriel
    Wallet(3, 3, "Aleksej Wallet", 120.25),    # Wallet von Aleksej
]

# -------------------------------------------------------------
# TRANSAKTIONEN
# -------------------------------------------------------------
# Diese Liste simuliert alle Bewegungen auf den Wallets.
# Positive Werte = Einnahmen, Negative Werte = Ausgaben.
TRANSACTIONS: list[Transaction] = [
    Transaction(1, 1, +1500.0, "Salary", datetime(2025, 11, 1), "Monthly salary"),
    Transaction(2, 1, -45.5, "Groceries", datetime(2025, 11, 2), "Spar Einkauf"),
    Transaction(3, 1, -20.0, "Transport", datetime(2025, 11, 3), "Wiener Linien Monatskarte"),
    Transaction(4, 2, +2000.0, "Salary", datetime(2025, 11, 1), "Full-time job"),
    Transaction(5, 2, -150.0, "Electronics", datetime(2025, 11, 2), "New keyboard"),
    Transaction(6, 3, +300.0, "Gift", datetime(2025, 11, 1), "Birthday money"),
    Transaction(7, 3, -50.0, "Food", datetime(2025, 11, 3), "McDonalds"),
]
# → Diese Daten werden beim Start automatisch in den Speicher geladen.
# → Es gibt keinen persistenten Speicher (alles verschwindet beim Beenden).

# ===================================================================
# STUB-FUNKTIONEN (Platzhalter für zukünftige Datenbankabfragen)
# ===================================================================


def get_all_users() -> list[User]:
    """
    Gibt alle Benutzer aus der Dummy-Datenbank zurück.

    Returns:
        list[User]: Liste aller Benutzerobjekte.
    """
    # Es wird einfach die gesamte USERS-Liste zurückgegeben.
    return USERS


def get_wallets_by_user(user_id: int) -> list[Wallet]:
    """
    Gibt alle Wallets eines bestimmten Benutzers zurück.

    Args:
        user_id (int): Die ID des gewünschten Benutzers.

    Returns:
        list[Wallet]: Eine Liste aller Wallets, die zu diesem Benutzer gehören.
    """
    # Durchläuft alle Wallets und prüft, ob die user_id übereinstimmt.
    # List Comprehension = kompakte Schreibweise für Filterung.
    return [w for w in WALLETS if w.user_id == user_id]


def get_transactions_by_wallet(wallet_id: int) -> list[Transaction]:
    """
    Gibt alle Transaktionen eines bestimmten Wallets zurück.

    Args:
        wallet_id (int): ID des Wallets, für das Transaktionen gesucht werden.

    Returns:
        list[Transaction]: Alle Transaktionen dieses Wallets.
    """
    # Hier wird jedes Transaction-Objekt geprüft,
    # ob seine wallet_id der gesuchten entspricht.
    return [t for t in TRANSACTIONS if t.wallet_id == wallet_id]


def add_transaction(wallet_id: int, amount: float, category: str, description: str = "") -> Transaction:
    """
    Fügt eine neue Dummy-Transaktion hinzu.

    Diese Funktion simuliert eine INSERT-Operation in einer echten Datenbank.
    Es wird kein Rückgabewert aus der DB erzeugt – stattdessen generiert
    die Funktion selbst eine ID auf Basis der Listenlänge.

    Args:
        wallet_id (int): ID des Wallets, dem die Transaktion zugeordnet wird.
        amount (float): Betrag der Transaktion (positiv = Einnahme, negativ = Ausgabe).
        category (str): Kategoriebezeichnung, z. B. "Salary" oder "Food".
        description (str, optional): Freitextbeschreibung. Standardwert = leerer String.

    Returns:
        Transaction: Das neu erstellte Transaktionsobjekt.
    """
    # ID = aktuelle Länge der Liste + 1 → einfache AutoIncrement-Simulation
    new_id = len(TRANSACTIONS) + 1

    # Neues Transaktionsobjekt wird erstellt
    transaction = Transaction(
        new_id,               # fortlaufende ID
        wallet_id,            # Wallet-Zuordnung
        amount,               # Betrag (positiv/negativ)
        category,             # Kategorie (z. B. "Groceries")
        datetime.now(),       # aktuelles Datum/Zeit (Zeitstempel)
        description            # Beschreibung (z. B. "Tankstelle")
    )

    # Die neue Transaktion wird der Dummy-Liste hinzugefügt
    TRANSACTIONS.append(transaction)

    # Rückgabe des neu erzeugten Objekts
    return transaction


def calculate_wallet_balance(wallet_id: int) -> float:
    """
    Berechnet den aktuellen Kontostand auf Basis aller Transaktionen.

    Diese Funktion summiert alle zugehörigen Transaktionen (Einnahmen & Ausgaben)
    für ein bestimmtes Wallet und gibt den Gesamtbetrag zurück.

    Args:
        wallet_id (int): ID des Wallets, dessen Kontostand berechnet werden soll.

    Returns:
        float: Der aktuelle Saldo (Summe der Beträge).
    """
    # 1. Alle Transaktionen dieses Wallets abrufen
    transactions = get_transactions_by_wallet(wallet_id)

    # 2. Betragssummen berechnen (Summe aller .amount-Werte)
    total_balance = sum(t.amount for t in transactions)

    # 3. Rückgabe als float
    return total_balance


# ===================================================================
# HAUPTTEST (nur für lokale Ausführung)
# ===================================================================
if __name__ == "__main__":
    # Dieser Block wird nur ausgeführt, wenn das Skript direkt gestartet wird
    # (nicht beim Import in anderen Modulen).

    print("\n--- TEST DATABASE MODULE ---\n")

    # Alle Benutzer anzeigen
    print("Alle Benutzer:", get_all_users())

    # Wallets von Benutzer 1 (Ivan)
    print("\nIvan Wallets:", get_wallets_by_user(1))

    # Transaktionen des Wallets 1 (Ivan Main)
    print("\nTransaktionen Ivan Wallet 1:", get_transactions_by_wallet(1))

    # Neue Transaktion hinzufügen (Test)
    print("\nNeuer Eintrag:", add_transaction(1, -12.5, "Coffee", "Test Transaction"))

    # Kontostand berechnen (nach neuer Transaktion)
    print("\nKontostand Ivan:", calculate_wallet_balance(1))