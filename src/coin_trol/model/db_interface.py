"""
db_interface.py
---------------
Verbindung zu MongoDB Atlas + CRUD-Funktionen für CoinTrol.
"""

from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
from pathlib import Path
from bson import ObjectId
import os

# ============================================================
# KONFIGURATION
# ============================================================

# .env aus dem Projekt-Hauptverzeichnis laden
env_path = Path(__file__).resolve().parents[3] / ".env"
load_dotenv(dotenv_path=env_path)

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

db = None
client = None

# Verbindung zu MongoDB herstellen
try:
    if not MONGO_URI or not DB_NAME:
        raise ValueError("MONGO_URI oder DB_NAME fehlt in der .env-Datei.")

    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]

    if db is not None:
        print(f"[DB] Verbunden mit MongoDB-Datenbank: {DB_NAME}")
    else:
        print("[DB-Fehler] Keine Datenbank gefunden.")

except Exception as e:
    print(f"[DB-Fehler] Verbindung fehlgeschlagen: {e}")
    db = None

# Collections definieren
if db is not None:
    users_col = db["users"]
    wallets_col = db["wallets"]
    transactions_col = db["transactions"]
else:
    users_col = wallets_col = transactions_col = None


# ============================================================
# CREATE
# ============================================================

def create_user(name: str, email: str, password: str = "1234") -> str:
    """Erstellt einen neuen Benutzer + Standard-Wallet."""
    if users_col is None:
        raise ConnectionError("Keine Datenbankverbindung verfügbar.")

    # Benutzer einfügen
    user = {
        "name": name,
        "email": email,
        "password": password,
        "created_at": datetime.now()
    }
    result = users_col.insert_one(user)
    user_id = str(result.inserted_id)

    # Standard-Wallet automatisch anlegen
    try:
        create_wallet(user_id, "Main Wallet", 0.0)
        print(f"[DB] Benutzer '{name}' + Main Wallet erstellt.")
    except Exception as e:
        print(f"[DB-Warnung] Wallet konnte nicht erstellt werden: {e}")

    return user_id


def create_wallet(user_id: str, name: str, balance: float = 0.0) -> str:
    """Erstellt ein neues Wallet für einen Benutzer."""
    if wallets_col is None:
        raise ConnectionError("Keine Datenbankverbindung verfügbar.")

    wallet = {
        "user_id": user_id,
        "name": name,
        "balance": balance,
        "currency": "EUR",
        "created_at": datetime.now()
    }
    result = wallets_col.insert_one(wallet)
    return str(result.inserted_id)


def add_transaction(wallet_id: str, amount: float, category: str, description: str = "", currency: str = "EUR") -> str:
    """Fügt eine Transaktion hinzu und aktualisiert das Wallet-Guthaben."""
    if transactions_col is None:
        raise ConnectionError("Keine Datenbankverbindung verfügbar.")

    trans = {
        "wallet_id": wallet_id,
        "amount": amount,
        "category": category,
        "description": description,
        "currency": currency,
        "date": datetime.now(),
    }
    result = transactions_col.insert_one(trans)

    # Wallet aktualisieren
    update_wallet_balance(wallet_id)

    return str(result.inserted_id)


# ============================================================
# READ
# ============================================================

def calculate_wallet_balance(wallet_id: str) -> float:
    """Berechnet und aktualisiert den Kontostand eines Wallets."""
    if transactions_col is None or wallets_col is None:
        raise ConnectionError("Keine Datenbankverbindung verfügbar.")

    transactions = transactions_col.find({"wallet_id": wallet_id})
    total = sum(t.get("amount", 0.0) for t in transactions)
    wallets_col.update_one({"_id": ObjectId(wallet_id)}, {"$set": {"balance": round(total, 2)}})
    return round(total, 2)


def get_user_by_login(username: str, password: str):
    """Prüft Benutzer-Login und gibt User-ID zurück."""
    if users_col is None:
        raise ConnectionError("Keine Datenbankverbindung verfügbar.")

    user = users_col.find_one({"name": username, "password": password})
    return str(user["_id"]) if user else None


def get_wallets_by_user(user_id: str):
    """Gibt alle Wallets eines Benutzers zurück."""
    if wallets_col is None:
        raise ConnectionError("Keine Datenbankverbindung verfügbar.")
    return list(wallets_col.find({"user_id": user_id}))


def get_transactions_by_wallet(wallet_id: str):
    """Gibt alle Transaktionen eines bestimmten Wallets zurück."""
    if transactions_col is None:
        raise ConnectionError("Keine Datenbankverbindung verfügbar.")
    return list(transactions_col.find({"wallet_id": wallet_id}))


# ============================================================
# UPDATE
# ============================================================

def update_wallet_balance(wallet_id: str) -> float:
    """
    Aktualisiert den Kontostand eines Wallets basierend auf allen Transaktionen.
    Gibt den neuen Kontostand zurück.
    """
    try:
        if not wallet_id:
            print("[DB] Keine Wallet-ID angegeben.")
            return 0.0

        transactions = list(transactions_col.find({"wallet_id": wallet_id}))
        total = sum(t.get("amount", 0.0) for t in transactions)

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
# DELETE
# ============================================================

def delete_transaction(transaction_id: str) -> bool:
    """Löscht eine Transaktion und aktualisiert danach den Wallet-Stand."""
    if transactions_col is None:
        raise ConnectionError("Keine Datenbankverbindung verfügbar.")

    # Wallet-ID zuerst finden
    trans = transactions_col.find_one({"_id": ObjectId(transaction_id)})
    wallet_id = trans["wallet_id"] if trans else None

    result = transactions_col.delete_one({"_id": ObjectId(transaction_id)})

    if wallet_id:
        update_wallet_balance(wallet_id)

    return result.deleted_count > 0
