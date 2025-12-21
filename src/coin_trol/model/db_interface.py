"""
db_interface.py
---------------
Dieses Modul stellt die Schnittstelle zwischen der CoinTrol-App und einer MongoDB-Datenbank her.

Es enthält:
 - Verbindung zu MongoDB Atlas über die MONGO_URI (aus .env)
 - Zugriff auf Collections (users, wallets, transactions)
 - CRUD-Funktionen (Create, Read, Update, Delete)
 - Automatische Berechnung von Wallet-Balances

Alle Funktionen arbeiten mit PyMongo und ObjectId-Strukturen.
"""

# ============================================================
# BENÖTIGTE IMPORTS
# ============================================================
from pymongo import MongoClient           # Hauptklasse für MongoDB-Verbindung
from dotenv import load_dotenv            # Zum Laden von Umgebungsvariablen (.env)
from datetime import datetime             # Für Zeitstempel
from pathlib import Path                  # Zum sicheren Pfadhandling (.env-Suche)
from bson import ObjectId                 # Zum Umgang mit MongoDB-Objekt-IDs
import os                                # Zugriff auf Umgebungsvariablen (os.getenv)

# ============================================================
# KONFIGURATION & VERBINDUNG
# ============================================================

# Pfad zur .env-Datei bestimmen (3 Ordner über diesem Modul)
env_path = Path(__file__).resolve().parents[3] / ".env"

# .env-Datei laden → enthält MONGO_URI und DB_NAME
load_dotenv(dotenv_path=env_path)

# Verbindungseinstellungen aus Umgebungsvariablen holen
MONGO_URI = os.getenv("MONGO_URI")  # Verbindung zur MongoDB-Instanz
DB_NAME = os.getenv("DB_NAME")      # Name der zu verwendenden Datenbank

# Platzhalter für Client und Datenbank
db = None
client = None

# ------------------------------------------------------------
# Verbindung zur MongoDB-Datenbank herstellen
# ------------------------------------------------------------
try:
    # Prüfen, ob Variablen korrekt geladen wurden
    if not MONGO_URI or not DB_NAME:
        raise ValueError("MONGO_URI oder DB_NAME fehlt in der .env-Datei.")

    # Verbindung mit MongoDB-Cluster herstellen
    client = MongoClient(MONGO_URI)

    # Datenbank auswählen
    db = client[DB_NAME]

    # Rückmeldung im Terminal
    if db is not None:
        print(f"[DB] Verbunden mit MongoDB-Datenbank: {DB_NAME}")
    else:
        print("[DB-Fehler] Keine Datenbank gefunden.")

except Exception as e:
    # Fehlermeldung bei Verbindungsfehler
    print(f"[DB-Fehler] Verbindung fehlgeschlagen: {e}")
    db = None  # Verhindert Folgefehler, falls db nicht erreichbar ist

# ------------------------------------------------------------
# Collections definieren (wie Tabellen in relationalen DBs)
# ------------------------------------------------------------
if db is not None:
    users_col = db["users"]              # Benutzer
    wallets_col = db["wallets"]          # Wallets
    transactions_col = db["transactions"]# Transaktionen
else:
    # Fallback, falls DB nicht verfügbar ist
    users_col = wallets_col = transactions_col = None


# ============================================================
# CREATE – Datensätze anlegen
# ============================================================

def create_user(name: str, email: str, password: str = "1234") -> str:
    """
    Erstellt einen neuen Benutzer in der Datenbank und legt automatisch ein Standard-Wallet an.

    Args:
        name (str): Benutzername.
        email (str): E-Mail-Adresse.
        password (str, optional): Passwort (Standardwert: "1234").

    Returns:
        str: Die erzeugte Benutzer-ID als String.
    """
    if users_col is None:
        raise ConnectionError("Keine Datenbankverbindung verfügbar.")

    # Benutzer-Dokument vorbereiten
    user = {
        "name": name,
        "email": email,
        "password": password,
        "created_at": datetime.now()  # aktueller Zeitstempel
    }

    # Dokument einfügen → insert_one() gibt InsertResult zurück
    result = users_col.insert_one(user)

    # ID extrahieren (ObjectId in String umwandeln)
    user_id = str(result.inserted_id)

    # Standard-Wallet für neuen Benutzer anlegen
    try:
        create_wallet(user_id, "Main Wallet", 0.0)
        print(f"[DB] Benutzer '{name}' + Main Wallet erstellt.")
    except Exception as e:
        print(f"[DB-Warnung] Wallet konnte nicht erstellt werden: {e}")

    return user_id


def create_wallet(user_id: str, name: str, balance: float = 0.0) -> str:
    """
    Erstellt ein neues Wallet für einen Benutzer.

    Args:
        user_id (str): ID des Benutzers, dem das Wallet gehört.
        name (str): Walletname.
        balance (float): Anfangsbetrag (Standard: 0.0).

    Returns:
        str: Die ID des neu erstellten Wallets.
    """
    if wallets_col is None:
        raise ConnectionError("Keine Datenbankverbindung verfügbar.")

    # Wallet-Dokument vorbereiten
    wallet = {
        "user_id": user_id,
        "name": name,
        "balance": balance,
        "currency": "EUR",
        "created_at": datetime.now()
    }

    # Wallet speichern
    result = wallets_col.insert_one(wallet)
    return str(result.inserted_id)


def add_transaction(wallet_id: str, amount: float, category: str, description: str = "", currency: str = "EUR") -> str:
    """
    Fügt eine neue Transaktion hinzu und aktualisiert anschließend automatisch den Wallet-Stand.

    Args:
        wallet_id (str): ID des Wallets.
        amount (float): Betrag (positiv = Einnahme, negativ = Ausgabe).
        category (str): Kategorie der Transaktion.
        description (str, optional): Beschreibung (z. B. 'Einkauf').
        currency (str, optional): Währung (Standard: EUR).

    Returns:
        str: ID der neu hinzugefügten Transaktion.
    """
    if transactions_col is None:
        raise ConnectionError("Keine Datenbankverbindung verfügbar.")

    # Transaktions-Dokument
    trans = {
        "wallet_id": wallet_id,
        "amount": amount,
        "category": category,
        "description": description,
        "currency": currency,
        "date": datetime.now()
    }

    # In MongoDB einfügen
    result = transactions_col.insert_one(trans)

    # Nach Einfügen sofort Kontostand neu berechnen
    update_wallet_balance(wallet_id)

    return str(result.inserted_id)


# ============================================================
# READ – Daten lesen
# ============================================================

def calculate_wallet_balance(wallet_id: str) -> float:
    """
    Berechnet den aktuellen Kontostand eines Wallets und aktualisiert diesen in der Datenbank.

    Args:
        wallet_id (str): Wallet-ID.

    Returns:
        float: Neuer Kontostand (gerundet auf 2 Nachkommastellen).
    """
    if transactions_col is None or wallets_col is None:
        raise ConnectionError("Keine Datenbankverbindung verfügbar.")

    # Alle Transaktionen für das Wallet abrufen
    transactions = transactions_col.find({"wallet_id": wallet_id})

    # Summe aller Beträge berechnen
    total = sum(t.get("amount", 0.0) for t in transactions)

    # Wallet-Dokument in der DB mit neuem Kontostand updaten
    wallets_col.update_one(
        {"_id": ObjectId(wallet_id)},
        {"$set": {"balance": round(total, 2)}}
    )

    return round(total, 2)


def get_user_by_login(username: str, password: str):
    """
    Prüft, ob ein Benutzer mit angegebenem Namen und Passwort existiert.

    Args:
        username (str): Benutzername.
        password (str): Passwort.

    Returns:
        str | None: Benutzer-ID, falls Login korrekt, sonst None.
    """
    if users_col is None:
        raise ConnectionError("Keine Datenbankverbindung verfügbar.")

    # Abfrage mit Filter für Name und Passwort
    user = users_col.find_one({"name": username, "password": password})

    # Wenn Benutzer gefunden → ID zurückgeben
    return str(user["_id"]) if user else None


def get_wallets_by_user(user_id: str):
    """
    Gibt alle Wallets eines bestimmten Benutzers zurück.

    Args:
        user_id (str): Benutzer-ID.

    Returns:
        list[dict]: Liste der Wallet-Dokumente.
    """
    if wallets_col is None:
        raise ConnectionError("Keine Datenbankverbindung verfügbar.")

    return list(wallets_col.find({"user_id": user_id}))


def get_transactions_by_wallet(wallet_id: str):
    """
    Gibt alle Transaktionen eines bestimmten Wallets zurück.

    Args:
        wallet_id (str): Wallet-ID.

    Returns:
        list[dict]: Liste der Transaktionen.
    """
    if transactions_col is None:
        raise ConnectionError("Keine Datenbankverbindung verfügbar.")

    return list(transactions_col.find({"wallet_id": wallet_id}))


# ============================================================
# UPDATE – bestehende Datensätze anpassen
# ============================================================

def update_wallet_balance(wallet_id: str) -> float:
    """
    Aktualisiert den Kontostand eines Wallets basierend auf allen Transaktionen.

    Wird z. B. nach dem Hinzufügen oder Löschen von Transaktionen aufgerufen.

    Args:
        wallet_id (str): ID des Wallets.

    Returns:
        float: Neuer Kontostand (rund).
    """
    try:
        # Kein Wallet angegeben → Abbruch
        if not wallet_id:
            print("[DB] Keine Wallet-ID angegeben.")
            return 0.0

        # Alle Transaktionen des Wallets abrufen
        transactions = list(transactions_col.find({"wallet_id": wallet_id}))

        # Gesamtsumme berechnen
        total = sum(t.get("amount", 0.0) for t in transactions)

        # In DB aktualisieren
        wallets_col.update_one(
            {"_id": ObjectId(wallet_id)},
            {"$set": {"balance": round(total, 2)}}
        )

        print(f"[DB] Wallet {wallet_id} aktualisiert. Neuer Kontostand: {total:.2f} €")
        return round(total, 2)

    except Exception as e:
        print(f"[DB-Fehler] update_wallet_balance fehlgeschlagen: {e}")
        return 0.0


# ============================================================
# DELETE – Datensätze löschen
# ============================================================

def delete_transaction(transaction_id: str) -> bool:
    """
    Löscht eine Transaktion aus der Datenbank und aktualisiert danach den Wallet-Kontostand.

    Args:
        transaction_id (str): ID der zu löschenden Transaktion.

    Returns:
        bool: True, wenn gelöscht, sonst False.
    """
    if transactions_col is None:
        raise ConnectionError("Keine Datenbankverbindung verfügbar.")

    # Zuerst die zugehörige Wallet-ID ermitteln, damit wir danach das Wallet updaten können
    trans = transactions_col.find_one({"_id": ObjectId(transaction_id)})
    wallet_id = trans["wallet_id"] if trans else None

    # Transaktion löschen
    result = transactions_col.delete_one({"_id": ObjectId(transaction_id)})

    # Wenn Wallet existierte → Kontostand aktualisieren
    if wallet_id:
        update_wallet_balance(wallet_id)

    # True, wenn tatsächlich 1 Datensatz gelöscht wurde
    return result.deleted_count > 0