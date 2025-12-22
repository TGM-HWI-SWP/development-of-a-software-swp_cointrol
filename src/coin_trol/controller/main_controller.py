# main_controller.py

# Diese Datei verbindet die VIEW-Schicht (z. B. ui_login, ui_dashboard)
# mit der MODEL-Schicht (db_interface.py).
# 
# Der Controller ist das "Gehirn" zwischen Benutzeroberfläche und Datenbank.
# Er empfängt Befehle von der UI, ruft passende Datenbankfunktionen auf
# und gibt Ergebnisse zurück.


# IMPORTS aus der Datenbank-Schicht

# Jede dieser Funktionen stammt aus db_interface.py und kommuniziert mit MongoDB.
from coin_trol.model.db_interface import (
    get_user_by_login,        # Prüft Login-Daten in der DB
    create_user,              # Erstellt neuen Benutzer
    create_wallet,            # Erstellt neues Wallet
    add_transaction,          # Fügt Transaktion hinzu
    get_wallets_by_user,      # Holt alle Wallets eines Users
    get_transactions_by_wallet,  # Holt Transaktionen eines Wallets
    calculate_wallet_balance, # Berechnet den Kontostand eines Wallets
    update_wallet_balance,    # Aktualisiert Balance in der DB
    delete_transaction,       # Löscht Transaktion
)



# LOGIN-FUNKTION

def login(username: str, password: str) -> str | None:
    """
    Führt den Login-Prozess durch.
    Prüft Benutzername und Passwort gegen MongoDB.
    Gibt die Benutzer-ID zurück, falls erfolgreich.
    """

    # Anfrage an die Datenbank – überprüft, ob Benutzer existiert
    user_id = get_user_by_login(username, password)

    # Wenn Benutzer gefunden → Erfolg
    if user_id:
        print(f"[Controller] Login erfolgreich – User-ID: {user_id}")
        return user_id
    else:
        # Wenn kein Eintrag mit diesen Daten → Fehlermeldung
        print("[Controller] Login fehlgeschlagen!")
        return None



# DASHBOARD- UND WALLET-FUNKTIONEN
def get_user_balance(user_id: str) -> float:
    """
    Berechnet die gesamte Summe aller Wallets eines Benutzers.
    """

    # Holt alle Wallets aus der Datenbank, die zu dieser User-ID gehören
    wallets = get_wallets_by_user(user_id)
    total = 0.0  # Variable zur Summierung des Gesamtguthabens

    # Schleife über alle Wallets → Summiere alle Balances
    for w in wallets:
        # Jede Balance wird aktuell aus Transaktionen berechnet
        total += calculate_wallet_balance(str(w["_id"]))

    # Ausgabe in der Konsole zur Kontrolle
    print(f"[Controller] Gesamtbalance: {total} €")

    # Rückgabe des Gesamtbetrags an die View (z. B. Dashboard)
    return total


def get_wallet_details(user_id: str):
    """
    Gibt alle Wallets + zugehörige Transaktionen des Benutzers zurück.
    """

    # Holt alle Wallets des Benutzers
    wallets = get_wallets_by_user(user_id)
    data = []  # Hier werden die Ergebnisse gesammelt

    # Für jedes Wallet alle Transaktionen und Balances laden
    for w in wallets:
        wallet_id = str(w["_id"])  # ObjectId in String konvertieren
        transactions = get_transactions_by_wallet(wallet_id)  # Liste aller Transaktionen abrufen

        # Dictionary mit vollständigen Wallet-Infos anlegen
        wallet_info = {
            "wallet": w,                                    # Wallet-Daten (Name, Balance etc.)
            "transactions": transactions,                   # Liste der Transaktionen
            "balance": calculate_wallet_balance(wallet_id)  # Aktueller Kontostand
        }

        # Zum Ergebnis hinzufügen
        data.append(wallet_info)

    # Log-Ausgabe zur Kontrolle (z. B. "3 Wallets geladen.")
    print(f"[Controller] {len(data)} Wallets geladen.")
    return data



# CRUD-FUNKTIONEN – Create / Read / Update / Delete

def add_new_transaction(wallet_id: str, amount: float, category: str, description: str = ""):
    """
    Fügt eine neue Transaktion hinzu und aktualisiert danach automatisch den Kontostand.
    """

    # Neue Transaktion in der Datenbank anlegen
    trans_id = add_transaction(wallet_id, amount, category, description)

    # Nach dem Hinzufügen sofort neuen Kontostand berechnen
    new_balance = calculate_wallet_balance(wallet_id)

    # Konsolenausgabe zur Bestätigung
    print(f"[Controller] Neue Transaktion {trans_id} hinzugefügt. Neuer Kontostand: {new_balance} €")

    # Rückgabe der Transaktions-ID (z. B. zur Anzeige oder Aktualisierung in der UI)
    return trans_id


def remove_transaction(transaction_id: str):
    """
    Löscht eine Transaktion aus der Datenbank.
    """

    # Aufruf der Delete-Funktion aus db_interface.py
    success = delete_transaction(transaction_id)

    # Überprüfung und Logmeldung
    if success:
        print(f"[Controller] Transaktion {transaction_id} erfolgreich gelöscht.")
    else:
        print(f"[Controller] Fehler beim Löschen von Transaktion {transaction_id}.")

    # Gibt True oder False zurück (z. B. für Anzeige in UI)
    return success