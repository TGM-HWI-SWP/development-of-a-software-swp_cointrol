import json
import os

DB_PATH = os.path.join("data", "database.json")


class UserStorage:

    @staticmethod
    def load_db():
        if not os.path.exists(DB_PATH):
            return {"users": {}}

        with open(DB_PATH, "r") as f:
            try:
                return json.load(f)
            except:
                return {"users": {}}

    @staticmethod
    def save_db(db):
        with open(DB_PATH, "w") as f:
            json.dump(db, f, indent=4)

    @staticmethod
    def register_user(username: str, password: str) -> bool:
        db = UserStorage.load_db()

        # User existiert bereits
        if username in db["users"]:
            return False

        db["users"][username] = {
            "password": password,
            "transactions": []
        }

        UserStorage.save_db(db)
        return True

    @staticmethod
    def validate_login(username: str, password: str) -> bool:
        db = UserStorage.load_db()
        if username not in db["users"]:
            return False
        return db["users"][username]["password"] == password

    @staticmethod
    def add_transaction(username: str, amount: float, category: str, desc: str):
        db = UserStorage.load_db()

        if username not in db["users"]:
            return

        db["users"][username]["transactions"].append({
            "amount": amount,
            "category": category,
            "description": desc
        })

        UserStorage.save_db(db)

    @staticmethod
    def get_transactions(username: str):
        db = UserStorage.load_db()
        if username not in db["users"]:
            return []
        return db["users"][username]["transactions"]
