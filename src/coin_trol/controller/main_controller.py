from model.database import (
    get_wallets_by_user,
    get_transactions_by_wallet,
    calculate_wallet_balance,
)

def start_app():
    print("Starte CoinTrol...\n")
    user_id = 1
    display_user_dashboard(user_id)

def display_user_dashboard(user_id):
    wallets = get_wallets_by_user(user_id)
    for w in wallets:
        print(f"\n=== {w.name} ===")
        for t in get_transactions_by_wallet(w.wallet_id):
            print("  ", t)
        balance = calculate_wallet_balance(w.wallet_id)
        print(f"--> Aktueller Kontostand: {balance:.2f}€")
