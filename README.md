
# Notizen-Verwaltungssystem (API & UI)

Ein kompaktes Python-Projekt, das eine REST-Schnittstelle (FastAPI) zur strukturierten Ablage von Notizen mit einer übersichtlichen Weboberfläche (Streamlit) verbindet. Die Anwendung erlaubt das Katalogisieren über Kategorien und Schlagwörter.

## Komponenten des Repositories

Die Codebasis gliedert sich in folgende Dateien und Ordner:

- `main.py` — Das Anwendungs-Backend: Steuert die FastAPI-Routen, das Datenbank-Setup via SQLModel sowie die SQLite-Integration.
- `frontend.py` — Das Anwendungs-Frontend: Eine interaktive Streamlit-Oberfläche, um Datensätze im Browser einzusehen und neue Einträge zu erfassen.
- `notes.db` — Der lokale Datenspeicher: Eine SQLite-Datenbankdatei, die sich beim Erststart selbstständig generiert.
- `test_notes.py` — Älteres, manuelles Skriptsystem für punktuelle Abfragen während der Entwicklungsphase.
- `explorationen/` — Archivordner mit früheren Entwürfen und Testdateien aus der Entstehung des Projekts.
- `bus/` — Lokale Sicherheitskopien und persönliche Backups von Zwischenständen der Arbeit.
- `presentationen/` — Begleitendes Präsentations- und Anschauungsmaterial zu den einzelnen Kurstagen.
- `work-log.md` — Persönliches Arbeitsprotokoll zur Dokumentation des Lernfortschritts.

## Systemanforderungen

- Python in Version 3.12 oder aktueller
- Der Paketmanager `uv` zur effizienten Ausführung und Verwaltung der Umgebung

## Vorbereitung & Installation

Um das Projekt mitsamt allen benötigten Bibliotheken aufzusetzen, genügt dieser Befehl:

```bash
uv sync

```

## Starten des Backends

Das API-Backend wird über die Konsole mit folgendem Aufruf gestartet:

```bash
uv run fastapi dev main.py

```

Nach dem Start läuft der Server lokal unter der Adresse `http://127.0.0.1:8000`.

### Automatische Dokumentation

Die API stellt eigenständig zwei visuelle Dokumentationsseiten bereit:

* Swagger-Testumgebung: `http://127.0.0.1:8000/docs`
* ReDoc-Übersicht: `http://127.0.0.1:8000/redoc`

## Starten des Frontends

Öffne ein **weiteres, separates Terminalfenster** und führe die grafische Oberfläche wie folgt aus:

```bash
uv run streamlit run frontend.py

```

Die Benutzeroberfläche startet daraufhin automatisch im Browser unter `http://localhost:8501`.

## Bereitgestellte API-Schnittstellen

### Notiz-Operationen

* `POST /notes` — Legt einen neuen Eintrag an (Rückgabewert: Statuscode 201)
* `GET /notes` — Ruft die Liste aller Notizen ab (unterstützt verschiedene Suchfilter)
* `GET /notes/{note_id}` — Lädt ein spezifisches Dokument anhand der ID aus der Datenbank
* `PUT /notes/{note_id}` — Ersetzt eine vorhandene Notiz vollständig mit neuen Werten
* `PATCH /notes/{note_id}` — Erlaubt die gezielte Modifikation einzelner Datenfelder
* `DELETE /notes/{note_id}` — Entfernt einen Eintrag permanent (Rückgabewert: Statuscode 204)
* `GET /notes/stats` — Liefert Metriken (Gesamtzahl, Verteilung auf Kategorien, meistgenutzte Tags)

### Filteroptionen und Zusatzrouten

Beim Abruf über `GET /notes` können folgende Parameter zur Eingrenzung übergeben werden:

* `category` (Filterung nach einem Themenbereich)
* `search` (Stichwortsuche innerhalb von Titel und Textinhalt)
* `tag` (Filterung nach einem bestimmten Schlagwort)
* `created_after` (Zeigt Einträge ab einem bestimmten Erstellungsdatum)
* `created_before` (Zeigt Einträge bis zu einem bestimmten Erstellungsdatum)

Ergänzende Auswertungs-Routen:

* `GET /categories` — Gibt alle verwendeten Kategorien sortiert aus
* `GET /categories/{category_name}/notes` — Filtert alle Einträge einer gewünschten Kategorie
* `GET /tags` — Listet sämtliche vergebene Schlagwörter auf
* `GET /tags/{tag_name}/notes` — Sucht gezielt nach Notizen mit dem angegebenen Tag

---

## Tests

Das System bietet verschiedene Optionen, um die korrekte Funktionsweise der Schnittstellen und Datenverarbeitung zu überprüfen.

### 1. Automatisierte Test-Suite (Integrationstests)

Das Projekt enthält eine umfangreiche Testabdeckung in der Datei test_main.py. Insgesamt werden rund 70 automatisierte Testfälle ausgeführt, die alle Endpunkte, Filterkombinationen und Fehlerszenarien lückenlos überprüfen.

Um die Test-Suite zu starten, muss die FastAPI-Anwendung bereits im Hintergrund aktiv sein (http://127.0.0.1:8000). Führe dann im Projektordner folgenden Befehl aus:

```bash
uv run pytest test_main.py -v
```

### 2. Manueller Funktionstest via Swagger UI (Backend-Prüfung)

Um ohne den Start des Frontends zu kontrollieren, ob die API Einträge fehlerfrei verarbeitet und in der lokalen Datei `notes.db` hinterlegt, kann die interaktive Benutzeroberfläche unter `http://127.0.0.1:8000/docs` verwendet werden.

Navigiere dort zur Route `POST /notes`, aktiviere das Eingabefeld über den Button "Try it out" und nutze das folgende JSON-Strukturbeispiel für einen Schreibtest:

```json
{
  "title": "3D-Apfelschäler",
  "content": "Ein Gerät, welches Äpfel in beliebigen Formen schneidet",
  "category": "work",
  "tags": ["idea"]
}

```

### 3. Abrufen von Notizen über die Schnittstelle (GET-Abfrage)
Um zu kontrollieren, welche Einträge aktuell in der Datenbank hinterlegt sind, gibt es zwei unkomplizierte Wege, die direkt im Browser ohne das Streamlit-Frontend genutzt werden können:

* **Variante A (Direkt im Browser):** Da es sich um eine Standard-Abrufmethode (`GET`) handelt, kann die Adresse einfach in die Adresszeile des Webbrowsers eingegeben werden. Rufe dazu folgende URL auf, um alle Notizen als JSON-Text anzuzeigen:

```

[http://127.0.0.1:8000/notes](http://127.0.0.1:8000/notes)

```

* **Variante B (Über Swagger UI):**
Navigiere in der interaktiven Dokumentation (`http://127.0.0.1:8000/docs`) zum blauen Endpunkt `GET /notes` List Notes. Klicke auf **"Try it out"** und anschließend auf den blauen **"Execute"**-Button. Die API liefert daraufhin die Liste aller gespeicherten Notizen im Response-Body zurück.

```


---

## Datenhaltung und Validierungsmechanismen

Für die Persistenz wird `SQLModel` verwendet. Da relationale SQLite-Datenbanken keine Arrays oder Listen speichern können, werden die Tags als serialisierte Textzeile (`tags_json`) abgelegt und bei der API-Ausgabe im Hintergrund wieder in Python-Listen transformiert.

Beim Datenempfang erzwingt Pydantic die Einhaltung folgender Kriterien:

* **Titel:** Zwingend erforderlich; die Länge muss zwischen 3 und 100 Zeichen liegen.
* **Inhalt:** Zwingend erforderlich; muss mindestens 1 Zeichen enthalten.
* **Kategorien:** Werden vom System automatisch in einheitliche Kleinschreibung überführt.
* **Tags:** - Pro Notiz sind maximal 10 Schlagwörter erlaubt.
* Jedes einzelne Tag muss aus mindestens 2 Zeichen bestehen.
* Vorangestellte oder nachfolgende Leerzeichen werden entfernt, alle Buchstaben werden kleingeschrieben.
* Identische Stichwörter innerhalb einer Notiz werden automatisch aussortiert, um Duplikate zu vermeiden.


* **E-Mail:** Das Feld `author_email` ist im Schema hinterlegt, bleibt jedoch optional.
* **Sicherheits-Einschränkung:** Das mitsenden nicht definierter Zusatzfelder im JSON führt zu einer Abweisung des Requests (`extra="forbid"`).

Die Initialisierung der Tabellenstrukturen erfolgt vollautomatisch beim Starten der Anwendung.

## System zurücksetzen

Möchte man die Anwendung in den Auslieferungszustand versetzen und alle gespeicherten Notizen verwerfen, muss lediglich die Datei `notes.db` aus dem Projektordner gelöscht werden. Die Datenbankarchitektur baut sich beim nächsten Backend-Start komplett neu auf.

```

```