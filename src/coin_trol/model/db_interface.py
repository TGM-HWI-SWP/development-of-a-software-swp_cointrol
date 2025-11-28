"""
db_interface.py
---------------
Verbindung zu MongoDB Atlas + CRUD-Funktionen für CoinTrol.
"""

from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
import os
from bson import ObjectId

# .env laden
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

users_col = db["users"]
wallets_col = db["wallets"]
transactions_col = db["transactions"]

# ------------------- CREATE -------------------

def create_user(name: str, email: str) -> str:
    user = {"name": name, "email": email, "created_at": datetime.now()}
    result = users_col.insert_one(user)
    return str(result.inserted_id)

def create_wallet(user_id: str, name: str, balance: float = 0.0) -> str:
    wallet = {"user_id": user_id, "name": name, "balance": balance, "currency": "EUR"}
    result = wallets_col.insert_one(wallet)
    return str(result.inserted_id)

def add_transaction(wallet_id: str, amount: float, category: str, description: str = "") -> str:
    trans = {
        "wallet_id": wallet_id,
        "amount": amount,
        "category": category,
        "description": description,
        "date": datetime.now(),
    }
    result = transactions_col.insert_one(trans)
    return str(result.inserted_id)

# ------------------- READ -------------------

def calculate_wallet_balance(wallet_id: str) -> float:
    transactions = transactions_col.find({"wallet_id": wallet_id})
    total = sum(t["amount"] for t in transactions)
    wallets_col.update_one({"_id": ObjectId(wallet_id)}, {"$set": {"balance": total}})
    return total

# ------------------- UPDATE -------------------

def update_wallet_balance(wallet_id: str, new_balance: float) -> bool:
    result = wallets_col.update_one(
        {"_id": ObjectId(wallet_id)},
        {"$set": {"balance": new_balance}}
    )
    return result.modified_count > 0

# ------------------- DELETE -------------------

def delete_transaction(transaction_id: str) -> bool:
    result = transactions_col.delete_one({"_id": ObjectId(transaction_id)})
    return result.deleted_count > 0
