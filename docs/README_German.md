
# Reparaturverwaltungssystem

## Projektbeschreibung
Dieses Projekt dient zur Verwaltung und Bearbeitung von Reparaturanfragen (RMA) für Kunden und Mitarbeiter. Es bietet eine Benutzeroberfläche zur Eingabe, Bearbeitung und Verfolgung von Reparaturdaten sowie eine Datenbank zur Speicherung und Organisation der Informationen.

---

## Projektstruktur

### Hauptverzeichnis
- **app.py**: Hauptdatei zum Starten der Flask-Anwendung.
- **init_db.py**: Skript zur Initialisierung und Erstellung der Datenbank.
- **inspector.py**: Werkzeug zum Debuggen und Analysieren von Datenbanken oder Excel-Dateien.

### Verzeichnisse

#### **admin_module**
- **models.py**: Datenbankinteraktionen und Modelle.
- **routes.py**: Definition der Anwendungsrouten.
- **mock_data.py**: Enthält Beispiel- und Testdaten.

#### **static**
- **styles.css**: Stile für das Frontend.
- **scripts.js**: JavaScript-Funktionen zur Interaktivität.
- **table_controls.js**: Spezifische Tabellensteuerungsfunktionen.

#### **templates**
- HTML-Vorlagen für verschiedene Seiten, z. B.:
  - **index.html**: Startseite.
  - **employee_dashboard.html**: Mitarbeiter-Dashboard.
  - **new_repair.html**: Formular zur Registrierung neuer Reparaturen.

---

## Installation

1. Python 3.13 oder höher installieren.
2. Abhängigkeiten installieren:
   ```bash
   pip install -r requirements.txt
   ```
3. Datenbank initialisieren:
   ```bash
   python init_db.py
   ```
4. Server starten:
   ```bash
   python app.py
   ```

---

## Features

- **Kundenportal**: Ermöglicht Kunden die Einreichung und Nachverfolgung von Reparaturanfragen.
- **Mitarbeiterportal**: Bietet Mitarbeitern Tools zur Verwaltung von Reparaturprozessen.
- **Berichtserstellung**: Generiert Berichte basierend auf dem Status der Reparaturanfragen.

---

## Datenbank

Die Datenbank ist so konzipiert, dass alle relevanten Felder für Kunden- und Mitarbeiterformulare enthalten sind. Alle Abfragen und Interaktionen erfolgen über definierte Modelle und Funktionen.

---

## Entwicklernotizen

Für zukünftige Implementierungen:
- Optimierung der SQL-Abfragen für große Datenmengen.
- Integration von API-Schnittstellen für externe Systeme (z. B. SAP).
- Verbesserung der Benutzeroberfläche für eine bessere UX.

