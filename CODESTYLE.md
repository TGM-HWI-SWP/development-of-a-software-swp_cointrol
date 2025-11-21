Styleguide

1. Allgemeine Richtlinien
•	Einheitliche Sprache: Englisch für Code
•	Kommentare dürfen auf Deutsch sein
•	Dateinamen verwenden snake_case (z. B. database.py, ui_dashboard.py)
•	4 Leerzeichen für Einrückung
•	Maximale Zeilenlänge: 100 Zeichen
•	Keine Hardcodierung von Pfaden oder URLs
•	Jeder Code enthält Typannotationen und Docstrings

2. Namenskonventionen
Element	Regel	Beispiel
Klassen	PascalCase	class User:
Funktionen / Methoden	snake_case	def get_wallets_by_user():
Konstanten	UPPER_CASE	DEFAULT_BALANCE = 0.0
Variablen	lowercase	user_id = 1
Dateien	snake_case	ui_login.py
Module	Singular	model (nicht models)

3. Kommentare & Docstrings
Docstring-Format: Google Style
Kommentare: beginnen mit # (Leerzeichen nach #)
Kurze Kommentare inline, längere oberhalb der Codezeile

Datei-Header (am Anfang jeder Datei):
"""
database.py
-----------
Data handling and interfaces for the CoinTrol model
"""
Funktions-Docstring (Beispiel):
def calculate_wallet_balance(wallet_id: int) -> float:
    """
    Calculates the total balance for a given wallet.

    Args:
        wallet_id (int): The wallet identifier.

    Returns:
        float: Total balance of all transactions.
    """

4. Typing
•	Jeder Parameter und jede Rückgabe hat Typannotationen
•	def add_transaction(wallet_id: int, amount: float, category: str, description: str) -> None:
•	Listen oder Dictionaries immer typisieren (list[User], dict[str, float])

5. Code-Style-Regeln
•	Immer if __name__ == "__main__": für Startpunkte.
•	Keine Magic Numbers → Konstanten verwenden.
•	Einheitliche Leerzeilen:
    o	2 Leerzeilen zwischen Klassen.
    o	1 Leerzeile zwischen Funktionen.
•	Imports sortieren:
    1.	Standardbibliotheken
    2.	Drittanbieter
    3.	interne Module

Beispiel:
import json
from datetime import datetime
from model.database import get_wallets_by_user

6. Git & Branches
Rolle	Branch	Beschreibung
Ivan	model	Datenbank- & Datenlogik
Aleksej	controller	Logik & Kommunikation
Gabriel	view	Benutzeroberfläche
Regeln:
•	Niemals direkt auf main pushen.
•	Jeder arbeitet im eigenen Branch
•	Merge nur über Pull Requests
•	Commit Messages: Englisch, kurz und klar
Beispiel: week3: added typing and docstrings to model

7. Tests
•	Alle Tests liegen in src/coin_trol/tests/
•	Testfunktionen beginnen mit test_
•	Dummy-Daten oder Mocks sind erlaubt
•	Tests werden mit pytest gestartet:
•	pytest src/coin_trol/tests

8. Beispiel-Codevorlage (Snippet)
def example_function(param1: int, param2: str) -> bool:
    """
    Short description
    Args:
        param1 (int): Example numeric input
        param2 (str): Example text input

    Returns:
        bool: True if successful
    """
    # TODO: Replace with real logic
    return True

9. Erweiterte Hinweise
•	f-Strings für Stringformatierungen verwenden
•	Exceptions gezielt abfangen (keine blanken except:-Blöcke)
•	Konstanten / Konfigurationen in config.py
•	GUI-Dateien enthalten keine Logik
•	Logik-Dateien enthalten keine print()s – bei Bedarf Logging verwenden
