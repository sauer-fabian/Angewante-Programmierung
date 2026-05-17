# Work Log

**Student Name:** 

Instructions: Fill out one log for each course day. Content to consider: Course Sessions + Assignment

## Template:

---

## 1. ✅ What did I accomplish?

_Reflect on the activities, exercises, and work you completed today._

**Guiding questions:**
- What topics or concepts did you work with?
- What exercises or projects did you complete?
- What tools or technologies did you use?
- What did you learn or practice?

---

## 2. 🚧 What challenges did I face?

_Describe any difficulties, obstacles, or confusing moments you encountered._

**Guiding questions:**
- What was difficult to understand?
- Where did you get stuck?
- What errors or problems did you face?
- What felt frustrating or confusing?


---

## 3. 💡 How did I overcome them?

_Explain how you overcame the challenges or what help you needed._

**Guiding questions:**
- What strategies did you try?
- Who or what helped you (instructor, classmates, documentation)?
- What did you learn from solving the problem?
- What questions do you still have?


---

## Eigene Framework-Erkärung 
Aufbau des Work Logs: Unter „1. ✅ What did I accomplish?“ erfolgt eine einfache stichpunktartige Aufzählung der Ergebnisse. Die Abschnitte „2. 🚧 What challenges did I face?“ und „3. 💡 How did I overcome them?“ sind durchnummeriert und inhaltlich exakt aufeinander abgestimmt (Problem 1 wird durch Lösung 1 behoben).

## Einsatz von KI
Zur Lösung von Problemstellungen, zum Verständnis von Fehlermeldungen und zur Code-Anpassung wurden verschiedene KI-Tools (GitHub Copilot, ChatGPT, Google Gemini) genutzt. Im Vergleich hat mich Google Gemini bei meinen Problemen am besten geholfen und wurde daher am häufigsten verwendet.


## Week 1

### Day 1

#### 1. ✅ What did I accomplish?

- Entwicklungsumgebung mit VS Code, Git und dem Package Manager uv vollständig eingerichtet.

- Unterschied zwischen Git (lokal) und GitHub (Cloud) gelernt und Git-Repository initialisiert.

- Erstes FastAPI-Projekt erstellt und eine „Hello World“-API programmiert.

- Die API über den Browser und die interaktive Dokumentation (/docs) erfolgreich getestet.

- Mehrere einfache Endpunkte erstellt.

- Hausaufgabe: Endpoint erstellt, der eine Zahl (Dein Alter) empfängt und um +1 erhöht zurückgibt. (... So alt bist du nächstes Jahr )

---

#### 2. 🚧 What challenges did I face?

1. Die Installation von Git über das Terminal war unübersichtlich. 

2. Der Paketmanager Homebrew war in diesem Kontext neu für mich (ich kannte ihn bisher nur für Konsolen-Modifikationen für Romhacks).

3. Das Zusammenspiel zwischen dem lokalen Server, dem Browser und der API-Logik war am Anfang schwer zu verstehen.

4. Die Testergebnisse im Terminal wurden mir zunächst nicht angezeigt.
---

#### 3. 💡 How did I overcome them?

1. Hilfe bei der Installation und Einrichtung von Kommilitonen erhalten.

2. Befehle gegoogelt, die Dokumentation gelesen und gelernt, wie Homebrew als Paketverwalter für Software arbeitet.

3. Durch das Starten des Servers mit uv run fastapi dev und direktes Testen im Browser die Funktionsweise der API nachvollzogen. Zudem Befehle gegoogelt und die Dokumentation gelesen.

4. Den Befehl uv run pytest test_main.py -v im Terminal verwendet, um die detaillierten Ergebnisse anzuzeigen.

---

### Day 2

#### 1. ✅ What did I accomplish?
- Grundlagen zu APIs, HTTP und JSON gelernt.

- Die .gitignore Datei kennengelernt, um unnötige Dateien vom Upload auszuschließen. (sehr wichtig wenn man was nicht funktioniert könnte es daran liegen) 

- Note Taking API mit Daten-Speicherung in einer notes.json gebaut (Persistenz).

- Verwendung der HTTP-Methoden GET (Daten holen) und POST (Daten senden).

- Nutzung von Pydantic-Modellen für die Struktur der Notizen.

- Daten werden dauerhaft in einer notes.json gespeichert (Daten-Persistenz).

- Bonusaufgabe gelöst: Einen DELETE-Endpunkt zum Löschen von Notizen eingebaut.
---

#### 2. 🚧 What challenges did I face?

1. „Internal Server Error“ (Fehler 500) beim Versuch, neue Daten in die JSON-Datei zu schreiben. Generelle Unsicherheit, wo genau Code im Skript ergänzt werden muss.

2. Syntax-Fehler: Die Variable notes_db wurde fehlerhaft gleichzeitig als Parameter und als globale Variable verwendet.

3. Das REST-Prinzip war schwer verständlich
---

#### 3. 💡 How did I overcome them?

1. Die fehlende Funktion save_notes() im POST-Endpunkt ergänzt, damit die Daten auf der Festplatte gespeichert werden. Die Code-Struktur mit den Vorlesungsbeispielen verglichen und Einrückungsfehler korrigiert.

2. KI genutzt, um die Fehlermeldungen zu analysieren. Eine alte Testnotiz aus der Datei gelöscht, danach funktionierte der Code wieder.

3. Informationen zum REST-Prinzip im Internet nachgelesen und die HTTP-Methoden entsprechend zugeordnet.

---

### Day 3

#### 1. ✅ What did I accomplish?

#### 1. ✅ What did I accomplish?

* HTTP-Fehlercodes (wie 404 und 500) kennengelernt.

* Unterschied zwischen Path-Parametern (für eine konkrete Ressource) und Query-Parametern (als Filterfunktion) gelernt.

* Tags zu den Notizen hinzugefügt.

* Das Konzept des testbasierten Arbeitens angewendet, um Funktionen automatisiert zu überprüfen.

* Die FastAPI-GUI genutzt, um der KI Spezifikationen zu geben und Tests schreiben zu lassen.

* Die Datenspeicherung von JSON auf eine SQLite-Datenbank umgestellt und eine Many-to-Many-Beziehung über eine Link-Tabelle hergestellt.

* Die Anforderungen der Prüfungsleistung besser verstanden.

* Das Framework "Getting Shit Done" kennengelernt, um ein Projekt sehr konkret zu beschreiben und umzusetzen.

* Gelernt, wie man die KI Tests schreiben lässt, mit dem genauen Prompt: *"Create tests for the following OpenAPI specification. Store the test in the reference implementation folder. Use pytest and requests library."*

* Das "Resource-Oriented Design" bei REST-APIs verstanden: URLs sollten immer Nomen und keine Verben sein (z. B. `/notes` statt `/getNotes`).

* Mehrere Query-Parameter im Code kombiniert, um komplexe Filterungen (z. B. Suche + Kategorie + Tag gleichzeitig) zu ermöglichen.
---

#### 2. 🚧 What challenges did I face?

1. Fehler durch Code-Dopplungen (z. B. war der Delete-Endpunkt von Tag 2 doppelt im Code) und störende alte Funktionen, die noch auf das alte Dateisystem ausgelegt waren. Es gab auch Parameter-Reste, die Verwirrung stifteten.

2. Alte und neue Endpunkte zeigten Fehler an. Pfade wie `/test/123` wurden aufgrund einer falschen Reihenfolge im Code falsch interpretiert.

3. Die Umsetzung der vielen neuen Aufgaben war aufwendig: Den Statistik-Endpunkt anpassen (soll zusätzlich die 5 häufigsten Tags und die Gesamtzahl ausgeben), neue Endpunkte für Kategorien bauen, den Unterschied zwischen PUT (ganze Notiz überschreiben) und PATCH (einzelne Daten ändern) abbilden und Datumsfilter (`created_after`, `created_before`) einbauen.

4. Die Umstellung von der JSON-Datei auf die SQLite-Datenbank war die größte Aufgabe und erforderte viele Änderungen. Sie verursachte unerklärliche Server-Fehler. Zudem sah die neue Datenbankdatei (`notes.db`) im normalen Code-Editor komplett unleserlich (weird) aus.

5. JSON-Payload-Formatierung in der API (Swagger UI): Ein Versuch, Tags ohne Anführungszeichen (z. B. [rot]) zu übergeben, schlug fehl und wurde vom System nicht akzeptiert.

6. NameError Abstürze im Code: Nach dem Löschen der JSON-Logik stürzte das Programm ab, weil alte Endpunkte noch Variablen wie den note_id_counter suchten. Später trat ein ähnlicher Fehler auf, weil engine nicht definiert war.

7. Unerklärliche "Internal Server Error" (500) Meldungen beim Erstellen einer Notiz mit Tags in der neuen Datenbank. Die Fehlerursache war im Browser nicht sichtbar, da die Datenbank die Many-to-Many-Beziehung (NoForeignKeysError) ohne ausdrückliche Erklärung im Code nicht verstand.

---

#### 3. 💡 How did I overcome them?

1. Die doppelten Code-Teile gelöscht und veraltete JSON-Funktionen (wie `load_notes`, `save_notes` und Pfad-Angaben) komplett entfernt. Auf Anraten der KI habe ich zudem den Parameter `notes_db=None` aus den Klammern gelöscht, da die Funktion im restlichen Code immer ohne Werte aufgerufen wurde.

2. Die Reihenfolge der Endpunkte im Code korrigiert (spezifische Pfade weiter nach oben gesetzt), damit FastAPI die Pfade wieder richtig zuordnet und interpretiert.

3. Die Aufgaben Schritt für Schritt abgearbeitet: Den alten Statistik-Endpunkt `#@app.get("/notes/stats")` verworfen und den Code aktualisiert. Neue Endpunkte für die Liste aller Kategorien und für Notizen einer bestimmten Kategorie erstellt. Den Endpunkt `@app.get("/notes")` angepasst, um die Datumsfilter einzubauen (dabei gelernt, dass man das ISO-Datum direkt als Text vergleichen kann).

4. Den SQLite Viewer in VS Code installiert, wodurch die Datenbank leserlich wurde. Die Fehler nach der Datenbank-Migration gesucht und die nötigen neuen Endpunkte für die Datenbank Stück für Stück umgesetzt.

5. Das richtige JSON-Format angewendet: Gelernt, dass Strings innerhalb von Listen in JSON zwingend in doppelte Anführungszeichen gesetzt werden müssen (also ["rot"] statt [rot]).

6. Den alten Code komplett durch die neue SQLModel-Logik ersetzt (wodurch IDs von der Datenbank automatisch vergeben werden und der Counter obsolet wurde). Fehlende Werkzeuge wie create_engine am Anfang der Datei in den Import-Bereich hinzugefügt.

7. Gelernt, wie man den Stacktrace (Fehlertext) in der Server-Konsole liest, um die Ursache für einen 500er-Fehler zu finden. Das Problem gelöst, indem ich eine explizite Verbindungstabelle (NoteTagLink) als Code definiert und per link_model verknüpft habe. Wichtigstes Learning: Die durch vorherige Fehler korrumpierte notes.db-Datei musste vor dem Server-Neustart komplett gelöscht werden, damit sie sauber neu aufgebaut werden konnte.

## Week 2

### Day 4

#### 1. ✅ What did I accomplish?


- Simple Tests für Beispiel-Endpunkte geschrieben und die vom Gruppenpartner ausgeführt

- Alle Endpunkte und Grenzfälle getestet

- Einführung in das automatisierte Testen von APIs mit `pytest` und der Bibliothek `requests`.

- Die grundlegende Teststruktur nach dem Prinzip „Arrange – Act – Assert“ (Vorbereiten – Ausführen – Prüfen) gelernt und angewendet.

- Die `Faker`-Library erfolgreich eingebunden, um automatisch zufällige Testdaten (wie Namen in verschiedenen Schriften) zu generieren.

- Gelernt, dass man eigene Dateien niemals exakt wie installierte Bibliotheken benennen darf, da Python diese sonst überschreibt und blockiert.

- Gelernt, wie man über das Terminal gezielt Einzeltests ansteuert, Tests komplett durchlaufen lässt und sich mit dem Parameter `-v` die ausführlichen Ergebnisse anzeigen lässt.

- Den Workflow für die API-Entwicklung optimiert: Zuerst eine separate Test-Datei aufbauen, um den Code isoliert und sicher zu prüfen.

- Eine eigene `test_notes.py` erstellt, die alle wichtigen Endpunkte (POST zum Erstellen, GET zum Auflisten, GET mit ID zum Suchen) automatisch validiert.

- Verstanden, wie Pydantic-Klassen (NoteCreate und Note) eingehende Daten am API-Eingang absichern (z. B. Typenprüfung, ob der Titel ein Text ist).

---

#### 2. 🚧 What challenges did I face?

1. Pytest hat am Anfang überhaupt keine Tests erkannt („0 tests found“), weil die Benennung der Testdateien und Testfunktionen nicht den strengen Namenskonventionen entsprach.

2. Der Befehl `create_engine` wurde im Code-Editor plötzlich ausgegraut dargestellt, was zu Verwirrung führte und auf einen fehlerhaften Import hindeutete.

3. Beim Ausführen der Tests mit der `requests`-Bibliothek gab es Verbindungsfehler, weil das Zusammenspiel zwischen den Test-Skripten und der API nicht funktionierte.

4. Nach dem erfolgreichen Durchlauf der Tests zeigte pytest in der Zusammenfassung nur "7 passed" statt der erwarteten 8 Tests an.

5. Große Verwirrung darüber, wo genau im Code-Editor die Test-Struktur abgelegt werden muss und in welchem spezifischen Terminal-Fenster die Test-Befehle gestartet werden müssen. 



---

#### 3. 💡 How did I overcome them?

1. Die Dateinamen konsequent in `test_main.py` bzw. `test_day4.py` umbenannt und alle Testfunktionen mit dem Präfix `test_` versehen, damit pytest sie automatisch findet und ausführt.

2. KI gefragt, wie der Import-Fehler bei `create_engine` zu beheben ist, ungenutzte Import-Leichen bereinigt und den Code-Aufbau für die Dateipersistenz sauber getrennt.

3. Den Workflow korrigiert: Verstanden, dass für `requests`-basierte Tests immer zwei Terminals parallel laufen müssen – im ersten Terminal muss die FastAPI mit `uv run fastapi dev` aktiv laufen, bevor im zweiten Terminal die Test-Suite mit `uv run pytest -v` gestartet wird.

4. Verstanden, dass pytest jede Python-Funktion als genau einen Test zählt. Ich hatte das "Anlegen" und "Löschen" in einer Funktion kombiniert. Durch das Aufteilen in zwei separate Funktionen (test_create_to_delete und test_delete_specific) wurden die vollen 8 Tests sauber durchgezählt.

5. Eine dedizierte Datei test_main.py im exakt selben Root-Verzeichnis angelegt und das integrierte Terminal von VS Code (Strg + ö) genutzt, um sicherzustellen, dass die Befehle im richtigen Projektpfad ausgeführt werden.  

---

### Day 5

#### 1. ✅ What did I accomplish?

- Grundlagen der Programmierung wiederholt (Datentypen wie Float und Integer, Standardbegriffe wie Def, print).

- Verstanden, was GitHub ist und dass es verschiedene Varianten davon gibt.

- Datenvalidierung mit Pydantic tiefgehend behandelt.

- Gelernt, wie man richtig validiert: Die Art und Weise, wie ein Datum eingegeben wird, wird im Backend gelöst (Format: "YYYY-MM-DD").

- Field(...) Constraints für Pydantic-Modelle fließend genutzt.

- Eigene field_validator und model_validator Funktionen geschrieben.

- Gelernt, zwischen Optional, Default und Required Feldern zu wählen.

- Pydantic 422 Error Responses gelesen, verstanden und lose Modelle abgedichtet, damit schlechte Daten direkt abgewiesen werden.

---

#### 2. 🚧 What challenges did I face?

1. Probleme mit unstrukturiertem Datenaufbau und Schwierigkeiten bei den Edge Tests der Hausaufgabe (Modelle spezifizieren, Titellänge begrenzen, Zeilenumbrüche verhindern, unbekannte Kategorien abfangen).

2. Fehlermeldungen im Code, weil ich lange Zeit nicht gemerkt habe, dass man für die E-Mail-Validierung ein extra Paket installieren muss.

3. „Internal Server Error“ (Fehler 500) im Terminal aufgrund von Problemen mit der lokalen notes.json Datei.
---

#### 3. 💡 How did I overcome them?
1. Die Hausaufgabe Schritt für Schritt gelöst: Eigene Tests erweitert, um Grenzfälle wie reject short title oder unknown categories zu prüfen, und die Kategorien direkt im Validator mit .lower() normalisiert.

2. Das fehlende Paket mit dem Befehl uv add email-validator manuell im Terminal nachinstalliert.

3. Die fehlerhafte notes.json einfach komplett gelöscht. Sie wurde beim Serverstart sauber neu erstellt, wodurch der Fehler verschwand. Zudem das neue main.py aus dem Unterricht übernommen.


---

### Day 6

#### 1. ✅ What did I accomplish?

- Die eigene API gegen eine fremde externe Test-Suite geprüft.

- Eine eigene Datei class_based_decorator.py erstellt und Python-Decoratoren kennengelernt.

- Die Bibliothek icecream für übersichtlicheres und besseres Debugging installiert und genutzt.

- Die API-Logik überarbeitet, t, um die Anforderungen der Tests zu erfüllen (z.B. Root Endpoint hinzugefügt).


---

#### 2. 🚧 What challenges did I face?

1. Große Menge an Fehlermeldungen beim ersten Durchlauf der externen Test-Suite (20 failed, 11 passed, 97 errors).
2. Fehler 422, weil die API im Body das Feld `author_email` zwingend erwartete, die Test-Suite dieses Feld aber nicht mitsendete.
3. Fehler 422 bei Notizen der Kategorie "work", da eine Validierungsregel zwingend den Tag "work" verlangte, die Test-Suite aber andere Tags (wie "sample") schickte.
4. Fehler 404 beim Aufruf des Root-Pfads (`/`), da kein passender Endpunkt existierte.
5. Die Test-Suite verursachte Fehler 404, da sie die Endpunkte `/categories/...` und `/tags/...` nicht finden konnte.
6. Fehler 405 (Method Not Allowed) beim Pfad `/notes/{note_id}`, da die Test-Suite dort die HTTP-Methode PUT erwartete, diese im Code aber fehlte.
7. Die Statistik-Funktion hat die häufigsten Tags (Top Tags) nicht richtig ermittelt.
8. Zu kurze Tags wurden von der API fälschlicherweise angenommen, anstatt blockiert zu werden.
9. Absichtlich ungültige Datumsangaben im Test (wie "2026-13-01" oder reiner Text) führten zum kompletten Absturz der Anwendung, anstatt eine Fehlermeldung auszugeben.
10. Der Datumsvergleich innerhalb der Filterung funktionierte nicht zuverlässig und führte zu Abstürzen.
11. Die API antwortete bei einer Liste von 11 Tags mit Status 201, obwohl der Test aufgrund der Überschreitung der erlaubten Tag-Anzahl einen Fehler 422 erwartete.
12. Alle 70 Tests der Test-Suite wurden plötzlich übersprungen (skipped).
13. Der Endpunkt für die Filterung (Status 200) kombinierte die verschiedenen Suchkriterien (Kategorie, Suche, Tags, Datum) noch nicht korrekt.
14. Der Statistik-Endpunkt lieferte zu viele Ergebnisse bei den Top-Tags und schlug im Test fehl.

---

#### 3. 💡 How did I overcome them?

1. Die Fehlermeldungen im Terminal systematisch und Schritt für Schritt analysiert und abgearbeitet.
2. Das Feld `author_email` in der Modelldefinition von `NoteCreate` als optional definiert (`author_email: str | None = None`).
3. Den entsprechenden `@model_validator` für den "work"-Tag vorübergehend aus dem Code entfernt.
4. Einen Root-Endpunkt (`@app.get("/")`) hinzugefügt, um der Test-Suite eine Standardantwort zu liefern.
5. Die Endpunkte für Kategorien und Tags aus den Aufgaben von Tag 3 wieder vollständig in die `main.py` kopiert.
6. Einen Endpunkt mit der Methode PUT für `/notes/{note_id}` hinzugefügt, der die gesamte Notiz ersetzt.
7. `collections.Counter` eingebunden, um die Häufigkeit der Tags präzise auszugeben.
8. Die Validierung im Tag-Feld (`clean_tags`) aktualisiert, sodass Tags mindestens 2 Zeichen lang sein müssen.
9. Den Parametertyp in der Funktion von `str` auf `datetime` geändert, damit FastAPI ungültige ISO-Formate automatisch mit Fehler 422 abweist.
10. Die Datumsstrings als Text verglichen, um die ISO-Strings innerhalb der Funktion sortierbar und vergleichbar zu machen.
11. Eine Längenbeschränkung für die Tag-Liste im Pydantic-Modell hinterlegt, um zu viele Tags abzuweisen.
12. Die Verbindung geprüft und den lokalen API-Server im Terminal neu gestartet.
13. Alle Filterbedingungen am Anfang der `list_notes`-Funktion sauber mit `if`-Abfragen strukturiert und zusammengeführt.
14. Die Ausgabe der häufigsten Tags über `.most_common(5)` strikt auf die geforderten 5 Ergebnisse begrenzt.

---

## Week 3

### 1. ✅ What did I accomplish?

- Das Frontend-Framework Streamlit erfolgreich installiert.

- Gelernt, dass Streamlit UTF-8-Kodierung nutzt, wodurch sämtliche Sprachen und Sonderzeichen nativ unterstützt werden.

- Streamlit als schlanke und performante Möglichkeit kennengelernt, um ohne Java- oder tiefe HTML-Kenntnisse GUIs direkt in Python zu schreiben.

- Eine funktionierende Verbindung zwischen dem Frontend (Streamlit) und dem Backend (FastAPI) hergestellt.

- Die Funktion zum Anzeigen aller gespeicherten Notizen visuell eingebaut.

- Ein Eingabe-Formular erstellt, um neue Notizen an die API zu senden.

- Daten erfolgreich mit requests.get abgerufen und mit requests.post gespeichert.

---

#### 2. 🚧 What challenges did I face?

1. Streamlit-Import-Schwierigkeiten: Ein Versuch, die Bibliothek über pip install zu installieren, schlug fehl.

2. Allgemeine Fehler, das Skript und die Oberflächen-Anzeige fehlerfrei zum Laufen zu bringen.

3. Die API im Backend lehnte Daten ab, wenn erforderliche Pflichtfelder im Streamlit-Formular leer abgeschickt wurden.

4. Editor zeigt Fehler: Trotz Installation zeigte der Code-Editor immer noch an, dass Streamlit nicht gefunden werden kann (`could not be resolved`).

5. Falsches Datenformat bei den Tags: Die API hat Fehlermeldungen ausgegeben, weil die Tags als einfacher Text statt als Liste an das Backend gesendet wurden.


---

#### 3. 💡 How did I overcome them?

1. Den korrekten Befehl `uv add streamlit` im Terminal verwendet.

2. Die Fehler im Code analysiert und in direkter Absprache mit Kommilitonen behoben.

3. Sicherheitsprüfungen direkt im Frontend eingebaut, damit nur vollständig ausgefüllte Formulare abgeschickt werden können.

4. Umgebung gewechselt: Das Skript wurde im Terminal mit dem Befehl `uv run` gestartet, damit Python die richtige Umgebung mit den installierten Paketen nutzt.

5. Text in Liste umgewandelt: Im Code wurde die Funktion `.split(",")` eingebaut, um den eingegebenen Text am Komma zu trennen und als korrekte Liste zu senden.


---

### Day 8

#### 1. ✅ What did I accomplish?

- Die saubere Datenstruktur und sinnvolle Ordnerstrukturen für das Projekt aufgebaut.

- Die .gitignore nochmals durchgesprochen: Gelernt, dass man vorgefertigte Standard-Versionen nutzt und diese manuell erweitert.

- Gelernt, dass pyproject.toml dazu dient, Projektabhängigkeiten, Metadaten und Build-Anforderungen zentral zu verwalten, um veraltete Formate zu ersetzen.

- Die Struktur einer professionellen README.md (Markdown) erarbeitet: Anleitung zum Starten des Servers, Code-Schnipsel zum Anlegen und Abholen von Notizen.

- Exkurs in Data Science durchgeführt: Daten bereinigt, sortiert und über die API direkt in den Browser geladen.

---
#### 2. 🚧 What challenges did I face?

1. Die Umstrukturierung des Codes und der Speicher-Logik verursachte anfangs viele Bugs.

2. Beim Wechsel von `notes.json` auf SQLite wurde zunächst eine fehlerhafte Datenbankdatei erzeugt, wodurch die 70 automatisierten Tests abstürzten.

3. Die Tests liefen im Hintergrund erfolgreich durch, aber über das Frontend ließen sich anscheinend keine neuen Notizen anlegen.

4. Der Backup-Ordner (`bus/`) wurde durch die vielen Zwischenstände extrem unübersichtlich.

5. Die exakte Syntax für Code-Highlighting in Markdown (z. B. für `bash` oder `json`) war mir neu, obwohl ich die Formatierungs-Basics aus Obsidian kannte.

6. Beim Testen anhand meiner eigenen README war anfangs unklar, ob die Daten wirklich korrekt in der Datenbank landen.

---

#### 3. 💡 How did I overcome them?

1. Den Code systematisch bereinigt, fehlerhafte Pfade aussortiert und auf die funktionierenden Kernteile reduziert.

2. `sqlmodel` sauber installiert, den Import hinzugefügt und die kaputte `notes.db` manuell gelöscht. Beim API-Neustart generierte sie sich fehlerfrei und alle Tests bestanden.

3. Es war lediglich ein kleines Timing-Problem: Nach etwa einer Minute war der Eintrag verarbeitet und in der Datenbank sichtbar.

4. Alte Dateien aufgeräumt und ein einheitliches Benennungssystem für die Backups eingeführt.

5. Mich kurz in die Markdown-Dokumentation eingelesen und das Highlighting gezielt für Terminal-Befehle und JSON formatiert.

6. Die Test-Schritte (z.B. via Swagger-UI) selbst durchgespielt und in der SQLite-Datenbank verifiziert, dass die Einträge dort fehlerfrei gespeichert werden.

# 🎉 Congratulations! You did it! 🎓✨













