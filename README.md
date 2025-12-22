[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/cqMTK5D_)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=21267486&assignment_repo_type=AssignmentRepo)

---

#  CoinTrol – SWP Projekt 2025  
**Team:** Ivan Strainovic, Aleksej Pancika, Gabriel  
**Klasse:** 4BHWII – HTL Wien XX

---

##  Week 1 – Projektstart

**Ziele:**
- Projektmanagement aufsetzen (PSP, Zeitplanung, Rollen)
- Rollen definieren:  
  - Ivan → Model/DB  
  - Aleksej → Controller/Businesslogik  
  - Gabriel → View/UI
- Ordnerstruktur, Git-Repository, `.gitignore` und README anlegen

**Ergebnis:**
- Repository erstellt und mit GitHub Classroom verbunden  
- Virtuelle Umgebung (`.venv`) aktiviert  
- Projektstruktur aufgebaut:
src/
└─ coin_trol/
├─ model/
├─ controller/
├─ view/
├─ utils/
└─ tests/

markdown
Code kopieren
- Rollen- und Zeitplanung abgeschlossen  

---

##  Week 2 – Model Layer (Ivan)

**Verantwortlich:** Ivan  
**Ziel:** Aufbau der Datenstruktur und Definition der Schnittstellen zwischen Model, Controller und View.

###  Struktur
- `src/coin_trol/model/entities.py` → Enthält die Klassen:
- **User** – repräsentiert einen Benutzer  
- **Wallet** – repräsentiert ein Konto / eine Geldbörse  
- **Transaction** – repräsentiert einzelne Transaktionen (Einnahmen/Ausgaben)
- `src/coin_trol/model/database.py` → Enthält Dummy-Daten und Schnittstellenfunktionen

###  Wichtige Funktionen
| Funktion | Parameter | Rückgabe | Beschreibung |
|-----------|------------|-----------|---------------|
| `get_all_users()` | – | `list[User]` | Gibt alle Benutzer zurück |
| `get_wallets_by_user(user_id)` | `int` | `list[Wallet]` | Holt alle Wallets eines Benutzers |
| `get_transactions_by_wallet(wallet_id)` | `int` | `list[Transaction]` | Holt alle Transaktionen eines Wallets |
| `add_transaction(wallet_id, amount, category, description)` | `int, float, str, str` | `Transaction` | Fügt eine neue Transaktion hinzu |
| `calculate_wallet_balance(wallet_id)` | `int` | `float` | Berechnet aktuellen Kontostand eines Wallets |

###  Testen
```bash
python src/coin_trol/main.py
Schnittstellenanalyse
Ivan: Model & Schnittstellen

Aleksej: Steuerlogik (Controller)

Gabriel: Darstellung (View)

Ergebnis:
Grundlegende MVC-Struktur und Schnittstellen stehen.

Week 3 – Coding Guidelines & Integration
Ziele:

Styleguide (PEP8 + Docstrings) erstellt

Einheitliche Namenskonventionen und Typannotationen

helpers.py erweitert

Controller-Anbindung vorbereitet

Erste MVP-Komponenten getestet

Styleguide
Einheitliche Sprache: Englisch im Code, Kommentare Deutsch

Klassen in PascalCase, Funktionen in snake_case, Konstanten in ALL_CAPS

Docstring-Format: Google-Style

4 Leerzeichen Einrückung, max. 100 Zeichen pro Zeile

Ergebnis
Model vollständig mit Controller verbunden, liefert Daten an View.
Styleguide.md angelegt.
pytest-Tests erfolgreich.

Week 4 – MVP-Komponenten entwickeln
Verantwortlich:

Ivan → Model / JSON-Datenhaltung / CRUD

Aleksej → Controller / Use-Cases / Logik

Gabriel → View / GUI-Formulare / Interaktion

Ziele
Model-CRUD-Funktionen (Create, Read, Update, Delete) implementieren

Controller-Use-Cases zur Datenweitergabe zwischen Model ↔ View entwickeln

View (UI) mit einfachen Formularen (Login, Dashboard) aufbauen

Erste Integrationstests mit Dummy-Daten durchführen

Ivan (Model)
Dummy-Daten erweitert in database.py

db_interface.py für JSON-Persistenz implementiert

Neue Funktionen:

persist_data()

create_wallet()

update_wallet_balance()

delete_transaction()

Erweiterte Tests (test_model.py)

helpers.py für Lookup-Funktionen ergänzt

Aleksej (Controller)
Verbindung zwischen View und Model hergestellt

Implementierung zentraler Use-Cases (add_transaction, get_balance, login_user)

Logikprüfung und Fehlerbehandlung integriert

Gabriel (View)
Aufbau der Dummy-GUI (Login und Dashboard)

Anpassung an Controller-Schnittstellen

Erste GUI-Tests mit Dummy-Daten

main.py – MVP-Durchstich
Enthält den Testablauf von Login → Controller → Model → View

Simuliert Benutzer-Login, Wallet-Auswahl, Transaktionsverarbeitung und Balance-Berechnung

Dient als Integrationstest für alle Schichten

🧪 Testen
bash
Code kopieren
pytest src/coin_trol/tests/
python src/coin_trol/main.py
✅ Ergebnis
Funktionaler Durchstich: Eingabe → Controller → Model → Anzeige

CRUD-Operationen laufen fehlerfrei

JSON-Datei wird nach Änderungen aktualisiert

Alle Schichten arbeiten zusammen

