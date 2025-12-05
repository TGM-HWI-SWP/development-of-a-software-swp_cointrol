"""
db_interface.py
---------------
Verbindung zu MongoDB Atlas + CRUD-Funktionen für CoinTrol.
Dient als zentrale Schnittstelle zwischen Controller und Datenbank.
"""

from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
from bson import ObjectId
import os
import sys

# ------------------------------------------------------------
# Initialisierung
# ------------------------------------------------------------
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "CoinTrol")

try:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    users_col = db["users"]
    wallets_col = db["wallets"]
    transactions_col = db["transactions"]
except Exception as e:
    print(f"[DB-ERROR] Verbindung zu MongoDB fehlgeschlagen: {e}")
    sys.exit(1)


# ------------------------------------------------------------
# CREATE
# ------------------------------------------------------------

def create_user(name: str, email: str) -> str:
    """Erstellt einen neuen Benutzer."""
    user = {"name": name, "email": email, "created_at": datetime.now()}
    result = users_col.insert_one(user)
    print(f"[DB] User angelegt: {name}")
    return str(result.inserted_id)


def create_wallet(user_id: str, name: str, balance: float = 0.0) -> str:
    """Erstellt ein Wallet für einen Benutzer."""
    wallet = {"user_id": user_id, "name": name, "balance": balance, "currency": "EUR"}
    result = wallets_col.insert_one(wallet)
    print(f"[DB] Wallet erstellt: {name}")
    return str(result.inserted_id)


def add_transaction(wallet_id: str, amount: float, category: str, description: str = "") -> str:
    """Fügt eine neue Transaktion hinzu."""
    trans = {
        "wallet_id": wallet_id,
        "amount": amount,
        "category": category,
        "description": description,
        "date": datetime.now(),
    }
    result = transactions_col.insert_one(trans)
    print(f"[DB] Neue Transaktion: {category} ({amount}€)")
    return str(result.inserted_id)


# ------------------------------------------------------------
# READ
# ------------------------------------------------------------

def calculate_wallet_balance(wallet_id: str) -> float:
    """Berechnet und aktualisiert den Kontostand eines Wallets."""
    transactions = transactions_col.find({"wallet_id": wallet_id})
    total = sum(t["amount"] for t in transactions)
    wallets_col.update_one({"_id": ObjectId(wallet_id)}, {"$set": {"balance": total}})
    print(f"[DB] Balance aktualisiert: {total:.2f}€")
    return total


# ------------------------------------------------------------
# UPDATE
# ------------------------------------------------------------

def update_wallet_balance(wallet_id: str, new_balance: float) -> bool:
    """Setzt einen neuen Kontostand für ein Wallet."""
    result = wallets_col.update_one(
        {"_id": ObjectId(wallet_id)},
        {"$set": {"balance": new_balance}},
    )
    if result.modified_count:
        print(f"[DB] Balance geändert → {new_balance:.2f}€")
    return result.modified_count > 0


# ------------------------------------------------------------
# DELETE
# ------------------------------------------------------------

def delete_transaction(transaction_id: str) -> bool:
    """Löscht eine Transaktion."""
    result = transactions_col.delete_one({"_id": ObjectId(transaction_id)})
    if result.deleted_count:
        print(f"[DB] Transaktion gelöscht: {transaction_id}")
    return result.deleted_count > 0


# ------------------------------------------------------------
# TEST (nur lokal ausführen)
# ------------------------------------------------------------

if __name__ == "__main__":
    print("=== MongoDB CRUD Test ===")

    # 1. Benutzer erstellen
    user_id = create_user("Ivan Test", "ivan@cointrol.at")

    # 2. Wallet anlegen
    wallet_id = create_wallet(user_id, "Test Wallet")

    # 3. Transaktionen hinzufügen
    add_transaction(wallet_id, +500.0, "Salary", "Test income")
    add_transaction(wallet_id, -50.0, "Food", "Pizza & Drinks")

    # 4. Balance berechnen
    balance = calculate_wallet_balance(wallet_id)
    print(f"Balance: {balance}€")

    # 5. Transaktion löschen (falls du manuell testen willst)
    # delete_transaction("<trans_id>")
