[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/cqMTK5D_)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=21267486&assignment_repo_type=AssignmentRepo)
<<<<<<< HEAD
---

## 🧱 Week 2 – Model Layer (Ivan)

**Verantwortlich:** Ivan  
**Ziel:** Aufbau der Datenstruktur und Definition der Schnittstellen zwischen Model, Controller und View.

### 📂 Struktur
- `src/coin_trol/model/entities.py` → Enthält die Klassen:
  - **User** – repräsentiert einen Benutzer
  - **Wallet** – repräsentiert ein Konto / eine Geldbörse
  - **Transaction** – repräsentiert einzelne Transaktionen (Einnahmen/Ausgaben)
- `src/coin_trol/model/database.py` → Enthält Dummy-Daten und die Schnittstellenfunktionen für den Controller

### ⚙️ Wichtige Funktionen
| Funktion | Parameter | Rückgabe | Beschreibung |
|-----------|------------|-----------|---------------|
| `get_all_users()` | – | `list[User]` | Gibt alle Benutzer zurück |
| `get_wallets_by_user(user_id)` | `int` | `list[Wallet]` | Holt alle Wallets eines Benutzers |
| `get_transactions_by_wallet(wallet_id)` | `int` | `list[Transaction]` | Holt alle Transaktionen eines Wallets |
| `add_transaction(wallet_id, amount, category, description)` | `int, float, str, str` | `Transaction` | Fügt eine neue Transaktion hinzu |
| `calculate_wallet_balance(wallet_id)` | `int` | `float` | Berechnet aktuellen Kontostand eines Wallets |

### 🧪 Testen
Zum Testen des Models:
```bash
python src/coin_trol/main.py

## Schnittstellenanalyse (Week 2)
Die Verbindung zwischen Model, Controller und View wurde dokumentiert.
Ivan: Datenmodell & Schnittstellenfunktionen
Aleksej: Steuerlogik zwischen Schichten
Gabriel: Darstellung (UI, Dummy-Screens)
=======

Woche 3 – Stichpunkte (meine Arbeit)

View-Dateien überarbeitet und an Styleguide angepasst
Typannotationen ergänzt
Datei-Header + Docstrings sauber geschrieben
Konstanten eingeführt, Magic Numbers entfernt
Dummy-Login und Dummy-Dashboard implementiert
Grundgerüst (Login → Dashboard) erstellt
MVC-Struktur vorbereitet
Erste MVP-Bausteine lauffähig gemacht
>>>>>>> origin/view
