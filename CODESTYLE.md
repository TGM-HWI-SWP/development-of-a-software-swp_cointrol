CoinTrol – Code Style Guide (SWP Projekt 2025)
1. Allgemeine Richtlinien

Sprache:

Code wird in Englisch geschrieben.

Kommentare und Docstrings dürfen auf Deutsch sein.

Namenskonvention:
Verwende snake_case für Dateien und Funktionen (z. B. database.py, get_wallets_by_user()).

Einrückung: 4 Leerzeichen pro Ebene.

Maximale Zeilenlänge: 100 Zeichen.

Keine Hardcodierung: Keine festen Pfade oder Zugangsdaten im Code.

Typisierung & Dokumentation: Jeder Codeblock hat Typannotationen und Docstrings.

2. Namenskonventionen
Element	Regel	Beispiel
Klassen	PascalCase	class User:
Funktionen / Methoden	snake_case	def get_wallets_by_user():
Konstanten	UPPER_CASE	DEFAULT_BALANCE = 0.0
Variablen	lower_case	user_id = 1
Dateien	snake_case	ui_login.py
Module	Singular	model, nicht models
3. Kommentare & Docstrings

Docstring-Format: Google Style
Kommentare: beginnen mit # + Leerzeichen.
Kurze Kommentare inline, längere Erklärungen oberhalb des Codeblocks.

Beispiel – Datei-Header:
"""
database.py
-----------
Data handling and interfaces for the CoinTrol model.
"""

Beispiel – Funktions-Docstring:
def calculate_wallet_balance(wallet_id: int) -> float:
    """
    Calculates and updates the total balance for a given wallet.

    Args:
        wallet_id (int): The wallet identifier.

    Returns:
        float: Total balance of all transactions.
    """

4. Typisierung

Alle Funktionen und Methoden enthalten Typannotationen.

Rückgabewerte sind ebenfalls typisiert.

Beispiel:

def add_transaction(wallet_id: int, amount: float, category: str, description: str) -> None:
    ...


Komplexe Datentypen:

list[User], dict[str, float], tuple[str, int] usw.

Typfehler werden mit mypy geprüft.

5. Code-Style-Regeln

Immer if __name__ == "__main__": am Programmstart.

Keine „Magic Numbers“ – stattdessen Konstanten definieren.

Einheitliche Leerzeilen:

2 Leerzeilen zwischen Klassen.

1 Leerzeile zwischen Funktionen.

Import-Reihenfolge:

Standardbibliotheken

Drittanbieter-Bibliotheken (PyQt6, pymongo, dotenv …)

Interne Module (from coin_trol.model import db_interface)

Beispiel:

import json
from datetime import datetime
from coin_trol.model.db_interface import get_wallets_by_user

6. Git & Branch-Regeln
Rolle	Branch	Beschreibung
Ivan	model	Datenbank, Struktur, MongoDB, CRUD
Aleksej	controller	Businesslogik & Kommunikation zwischen View & Model
Gabriel	view	Benutzeroberfläche, Design & GUI-Funktionalität

Regeln:

Niemals direkt auf main pushen.

Jeder arbeitet in einem eigenen Feature-Branch.

Merge nur über Pull Requests.

Commit Messages kurz, englisch und präzise.

Beispiel: week3: added typing and docstrings to model

7. Tests

Alle Tests liegen in src/coin_trol/tests/

Testfunktionen beginnen mit test_

Dummy-Daten oder Mocks sind erlaubt.

Tests werden mit pytest ausgeführt:

pytest src/coin_trol/tests


Unit-Tests prüfen:

Model-Funktionen (CRUD)

Controller-Logik

GUI-Antworten (Integrationstest)

8. Beispiel-Codevorlage
def example_function(param1: int, param2: str) -> bool:
    """
    Example of a documented function.

    Args:
        param1 (int): Example numeric input.
        param2 (str): Example text input.

    Returns:
        bool: True if successful.
    """
    # TODO: Replace with real logic
    return True

9. Erweiterte Hinweise

f-Strings immer statt + oder % für Formatierungen.
→ Beispiel: f"{user.name} hat {balance:.2f} € Guthaben."

Ausnahmen gezielt abfangen:
Kein except: ohne spezifischen Fehler.

Konfigurationen (z. B. Pfade, URIs) immer in config.py oder .env.

GUI-Dateien enthalten nur Darstellung, keine Logik.

Controller-Dateien enthalten keine print()-Ausgaben – stattdessen Logging oder Statusleiste.

Alle Dateien beginnen mit Header-Docstring (Titel, Beschreibung, Zweck).

Kommentare nie veraltet lassen – Code und Kommentar müssen übereinstimmen.

10. Tools & Qualitätsrichtlinien

Formatierung: black

Linting: ruff

Typprüfung: mypy

Build / Packaging: build & pyinstaller

Testen: pytest

PEP8-konform: alle Tools in pyproject.toml integriert.

11. Git Commit Guidelines (Quick Reference)
Typ	Zweck	Beispiel
feat:	Neues Feature	feat(view): added login statusbar
fix:	Bugfix	fix(model): corrected balance calculation
style:	Formatierung / Kommentare	style(controller): added docstrings
refactor:	Codeüberarbeitung	refactor(view): simplified dashboard layout
test:	Tests hinzugefügt	test(model): added db_interface unit test
docs:	Dokumentation	docs: updated README and codestyle