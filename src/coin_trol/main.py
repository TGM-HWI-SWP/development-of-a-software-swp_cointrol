"""
main.py
-------
Startpunkt des CoinTrol-Projekts (MVP-Durchstich).
Simuliert den Programmfluss von Login → Controller → Model → View.
"""

from view.ui_login import login_screen
from view.ui_dashboard import show_dashboard
from controller.main_controller import (
    get_wallets_by_user,
    get_transactions_by_wallet,
    add_transaction,
    calculate_wallet_balance,
)


def main() -> None:
    """
    Startet den MVP-Testablauf:
    - Dummy-Login
    - Abrufen von Wallets
    - Anzeigen der Transaktionen
    - Hinzufügen einer Beispiel-Transaktion
    - Berechnung des aktuellen Kontostands
    """
    print("\n===== COINTROL MVP START =====\n")

    # Dummy Login (Gabriels View)
    user_id = login_screen()

    # Controller ruft Wallets ab
    wallets = get_wallets_by_user(user_id)
    print(f"Wallets von Benutzer {user_id}: {wallets}")

    # Controller ruft Transaktionen ab
    if wallets:
        wallet_id = wallets[0].wallet_id
        txs = get_transactions_by_wallet(wallet_id)
        print(f"Transaktionen für Wallet {wallet_id}: {txs}")

        # Neue Dummy-Transaktion hinzufügen
        add_transaction(wallet_id, -12.50, "Coffee", "Morning Latte")
        print("Neue Transaktion hinzugefügt!")

        # Kontostand berechnen
        balance = calculate_wallet_balance(wallet_id)
        print(f"Aktueller Kontostand: {balance:.2f} €")

    # Dummy-Dashboard anzeigen (Gabriel)
    show_dashboard(user_id)

    print("\n===== MVP-DURCHSTICH BEENDET =====\n")


if __name__ == "__main__":
    main()
