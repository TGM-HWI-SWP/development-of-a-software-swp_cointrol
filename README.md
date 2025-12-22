[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/cqMTK5D_)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=21267486&assignment_repo_type=AssignmentRepo)
CoinTrol – Intelligenter Finanz- und Ausgabenmanager

Projektzeitraum: Oktober – Dezember 2025
Schule: HTL TGM Wien – Abteilung Informatik
Fach: SWP (Softwareentwicklung & Projektmanagement)
Klasse: 4BHWII
Team:

Ivan Strainovic – Model / Datenbank / MongoDB

Aleksej pancika – Controller / Businesslogik

Gabriel Rajkovic – View / GUI / Integration & Design

1. Projektbeschreibung

CoinTrol ist ein Python-basiertes Softwareprojekt zur Verwaltung persönlicher Finanzen.
Ziel ist die Entwicklung einer modernen, datenbankgestützten Desktop-Anwendung im MVC-Architekturmodell (Model-View-Controller).
Die App erlaubt Benutzern, Einnahmen und Ausgaben zu erfassen, mehrere Wallets zu verwalten und den Gesamtstatus ihrer Finanzen zu überwachen.

Die Anwendung nutzt eine MongoDB-Datenbank (Atlas/Compass) zur persistenten Speicherung von Benutzern, Wallets und Transaktionen,
eine grafische Benutzeroberfläche (GUI) in PyQt6, und eine saubere Controller-Schicht,
die Datenvalidierung und Geschäftslogik kapselt.

2. Projektziele

Aufbau eines vollständigen MVC-Systems mit klarer Trennung der Schichten

Professionelle PyQt6-GUI mit responsivem Dark-Mode

MongoDB-Anbindung über ein modulares Interface

CRUD-Funktionalitäten (Create, Read, Update, Delete) für Wallets & Transaktionen

Automatische Saldenberechnung je Wallet und Gesamtbalance

Dokumentierte Codebasis mit Type-Hints, Docstrings, Inline-Kommentaren

GitHub-Versionierung mit Branch-Strategie und klarer Aufgabenaufteilung

PEP8-Styleguide-konformer Code mit mypy & ruff überprüft

Abgabe eines stabilen MVPs (Minimum Viable Product) inkl. README & Installationsanleitung

3. Architekturüberblick (MVC-Pattern)
Model        ->  Datenbank (MongoDB), Entities, DB-Interface
Controller   ->  Logik, Schnittstelle zwischen View und Model
View         ->  GUI in PyQt6 (Login, Dashboard, Wallets, Transaktionen)

Model (Ivan Strainovic)

Verwaltung der Datenstrukturen (entities.py)

Dummy-Datenbank & MongoDB-Interface (database.py, db_interface.py)

CRUD-Funktionen (create, read, update, delete)

Verbindung zu MongoDB über .env Datei

Implementierung von Fehlerbehandlung und Datenvalidierung

Controller (Aleksej pancika)

Verbindung zwischen Model und View

Überprüfung von Eingaben, Steuerung der Logik

Übergabe von Daten an die GUI

Methoden zur Login-Prüfung, Transaktionssteuerung, Wallet-Update

View (Gabriel Rajkovic)

Gestaltung der grafischen Benutzeroberfläche mit PyQt6

Aufbau der Fenster: Login, Dashboard, Wallet-Übersicht, Transaktionen

Einheitliches Farbdesign (Dark Mode mit Akzentfarbe #5B5CF0)

Umsetzung von Statusleisten statt Pop-up-Meldungen

Scrollbare Layouts, moderne Typografie, intuitive Navigation

4. Projektstruktur

CoinTrol/
│
├── coin_trol/
│   ├── model/
│   │   ├── entities.py
│   │   ├── database.py
│   │   └── db_interface.py
│   ├── controller/
│   │   └── main_controller.py
│   └── view/
│       ├── ui_login.py
│       ├── ui_dashboard.py
│       ├── Wallets.py
│       └── Transaktion.py
│
├── tests/
│   ├── test_model.py
│   ├── test_controller.py
│   └── test_view.py
│
├── .env.example
├── requirements.txt
├── pyproject.toml
├── README.md
└── main.py

5. Funktionen
Bereich	Funktion	Beschreibung
Login / Registrierung	Benutzeranmeldung & Erstellung neuer Konten	Passwortvalidierung & DB-Speicherung
Dashboard	Übersicht aller Finanzen	Gesamtbalance, Monatsausgaben, Einnahmen
Wallets	Mehrere Konten pro Benutzer	Automatische Saldenberechnung
Transaktionen	Einnahmen/Ausgaben verwalten	CRUD-Funktionen + Kategorisierung
Statusleiste	Rückmeldungen ohne Pop-ups	Benutzerfreundliche Fehleranzeige
Dark-Mode Design	Einheitliche Farbpalette	#1E1F26 Hintergrund, #5B5CF0 Akzent
Scrollbare Layouts	Bessere Übersicht bei vielen Elementen	ScrollArea in Dashboard & Transaktionen

6. Installation & Ausführung
Voraussetzungen

Python 3.11 oder höher

MongoDB Compass oder MongoDB Atlas-Konto

Virtuelle Umgebung (.venv) aktiv

Setup-Schritte
# 1. Repository klonen
git clone https://github.com/<team>/CoinTrol.git
cd CoinTrol

# 2. Virtuelle Umgebung erstellen
python -m venv .venv
# Aktivieren
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# 3. Abhängigkeiten installieren
pip install -r requirements.txt

# 4. .env-Datei erstellen (Beispiel)
MONGO_URI=mongodb+srv://istrainovic:Cointrol1@cointrol.fcises4.mongodb.net/?appName=CoinTrol
DB_NAME=CoinTrol

# 5. Starten
python main.py

7. Verbindung zu MongoDB

Die Verbindung erfolgt über die Datei .env (nicht im Repo enthalten).

Beispiel:

MONGO_URI=mongodb+srv://istrainovic:Cointrol1@cointrol.fcises4.mongodb.net/?appName=CoinTrol


Die Collections:

users → Benutzerkonten

wallets → Einzelne Geldbörsen

transactions → Transaktionen (Einnahmen/Ausgaben)

8. Qualitätssicherung

Code Style: PEP8, geprüft mit ruff

Typing: vollständige Typannotationen, geprüft mit mypy

Tests: pytest für Controller- & Model-Tests

Dokumentation: Docstrings nach Google-Style

Versionierung: Branch-basiertes Git-Workflow (keine Direktcommits auf main)

Commit-Politik: viele kleine, sinnvolle Commits (pro Feature oder Datei)

Merge Reviews: durch Teammitglied, um Fehler zu vermeiden

9. Git-Workflow

Jeder arbeitet auf eigenem Branch (feature/gui, feature/db, controller_logic, etc.)

Änderungen werden lokal getestet

Commits enthalten klare Messages (z. B. “Added MongoDB CRUD base”)

Merge in integration/mvp_final

Nach erfolgreichem Test → Merge in main

Nur getestete, lauffähige Versionen auf main

10. Nutzung von KI & Tools

Zur Unterstützung während der Entwicklung wurden folgende Tools eingesetzt:

Tool	Zweck
ChatGPT (GPT-5)	Codeoptimierung, Refactoring, Kommentierung, Doku
GitHub Copilot	Vorschläge bei GUI-Layouts
MongoDB Compass	Testen von Queries
VS Code	Hauptentwicklungsumgebung
mypy / pytest / ruff	Typprüfung, Tests, Codequalität

11. Erweiterungsideen (Future Work)

Export als PDF / CSV

Filter & Suchfunktionen

Mehrsprachige UI

Diagramme (Matplotlib)

Passwort-Hashing (bcrypt)

Benutzer-Avatar & Themes

12. Lizenz & Urheberrecht

© 2025 HTL TGM Wien – Abteilung Wirtschaftsingineurwesen
Verwendung ausschließlich für Bildungszwecke.
Lizenz: MIT License

