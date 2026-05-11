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

## Week 1

### Day 1

#### 1. ✅ What did I accomplish?

setup von Git 

Code mit Server und eingabe 

uv implementieren



---

#### 2. 🚧 What challenges did I face?

mit den neuen themen wie github und upload und phython connection klar kommen 

uv verstehen

sehe die testergnisse nicht 
---

#### 3. 💡 How did I overcome them?

nachfragen

googlen

uv run pytest test_main.py -v einfgefüt 

---

### Day 2

#### 1. ✅ What did I accomplish?

git ignore kennen gelernt 

HTtp 
kommunikationswege 

und Json
What we learned:

✅ HTTP = Communication protocol
✅ GET = retrieve, POST = create
✅ JSON = data format (like Python dict)
✅ Status codes communicate results
✅ FastAPI handles conversion automaticall




---

#### 2. 🚧 What challenges did I face?

nicht vergessen, das wenn ein fehler beim implemntieren kommt von Datei namen, dass dieser typ bei git ignore sein könnte.

Server error 

rest principe verstehen

SyntaxError: name 'notes_db' is parameter and global
---

#### 3. 💡 How did I overcome them?

git ignore augeschrieben das es passieren kann bei dateinamen

Gemini genutzt um fehlermeldungen zu verstehen und im code anzupassen
- server errror -> note hinzugefügt 
- bei data mal den notiz gelöscht dann hats funktioniert

gegooglet





---

### Day 3

#### 1. ✅ What did I accomplish?


tags hinzugefügt 

    Prüfungsleistung besser verstanden

Wie mach ich Testszenarien?
Also automatisieren, das bots dein quasi Formular bringen.

test basiert arbeiten, damit man alles noch mal durch laufen lassen kann um zu chekcen ob alles noch funktioniert

fast gui anschauen
damit ki geben und test schreiben lasen
pyt test, 
    damit teste ergnisse kathegorien festlegen können 



Delet doppelt drin gehabt durch bosuns aufgabe von tag 2



---

#### 2. 🚧 What challenges did I face?

prüfungsleistung verstehen

Verstehen des codes

Quellcode deer ki übergeben -> testsschreiben lassen schreien kreire test for the following openapi specification store the test in reference impllementation folder use pytest and requests libery 
(code)


getting shit done (Frame Work), um sehr konkret ein projekt beschreiben um projket zu machen

save notes doppelt drin gehabt (Python erlaubt das nicht. Ein Name darf in einer Funktion nicht gleichzeitig ein übergebener Parameter und eine globale Variable sein.)

code dopplungen bonus aufgabe

---

1. Der bestehende Endpunkt /notes/stats muss angepasst werden. Er soll zusätzlich die 5 häufigsten Tags und die Gesamtzahl aller verschiedenen Tags ausgeben.

2. neue Endpunkte bauen:  
- Einen für eine Liste aller existierenden Kategorien.  
- Einen für alle Notizen aus einer bestimmten Kategorie.

3. Endpunkt, der nur einzelne Felder einer Notiz ändert. PUT überschreibt die ganze Notiz, PATCH ändert nur die Daten, die du mitgibst.

4. Du musst zwei neue Filter für GET /notes einbauen: created_after und created_before.

5. Die JSON-Datei wird durch eine SQLite-Datenbank ersetzt. Das ist die größte Aufgabe und erfordert viele Änderungen im Code.

notes gruppen entfernen 
- path
- load notes
- def save notes
- load notes

allte entpunkte zeigen fehler an 

die notes.db datei hat weird aussehen 

server error aber nicht rausgefunden warum
---

#### 3. 💡 How did I overcome them?

Es soll ein sinnvolles system entstehen

überlegen ob ich ein eigens projekt mache 

Ki Fragen -> Lösche den Parameter notes_db=None aus der Klammer. Da du im restlichen Code immer nur save_notes() ohne Werte aufrufst, wird dieser Parameter nicht gebraucht.

uv add sqlmodel instaliert

delet bonusaufgabe raus gmeacht 
---
1. #@app.get("/notes/stats") verwerfen und code aktualisieren

2. - Code für liste aller  existierenden Kathegrie erstellen 
-Code für alle Notizen die ganu zu eingegebenen Kategroie erstellt 

@app.get("/notes") erneut anpassen. Du fügst zwei neue Filter für das Datum ein: created_after und created_before. Man kann das ISO-Datum direkt als Text vergleichen.


neue endpunkte für datenbank verwenden

hab SQLite Viewer instaliert


## Week 2

### Day 4

#### 1. ✅ What did I accomplish?

niemmals namen wie paket nennen sonst überschreiben des packets

fake macht random namen mit versciednen nationlaitäten (schriften)

### prompt gestaltung 
erklärung was wir haben 
bevor du anfängst stell mir fragen zur klärung

einzeltest starten
uv run pytest test-day. py :: test_is_adult_boundery_18 # 

kleinen test anfangen, 

workflow;
erst einen externe file aufbauen, um zu testen, ob es funktioniert 

wie man die tests startet 
 uv run pytest test_main.py  
 wie man sie sieht 
  uv run pytest test_main.py -v

Die Klassen NoteCreate und Note prüfen, ob die Daten, die reinkommen, korrekt sind (z. B. ob der Titel ein Text ist).

Mit load_notes() und save_notes() schreibst du alles in die notes.json. So sind deine Notizen nicht weg, wenn du den Server ausschaltest.

POST /notes: Erstellt eine Notiz, gibt ihr eine ID und speichert sie.  
GET /notes: Listet alle gespeicherten Notizen auf.  
GET /notes/{id}: Sucht eine ganz bestimmte Notiz raus.  



---

#### 2. 🚧 What challenges did I face?

rausgefunden das create_engine ausgegraut ist 

den code zum laufen lassen



---

#### 3. 💡 How did I overcome them?

ki gefrag wie fixen 

ki gefragt wie man test und 



---

### Day 5

#### 1. ✅ What did I accomplish?

grundlagen von programierung
- arten von daten (float,integer...)
- was ist github (gibt auch varianten)
- was sidn standartberiffe (Def, print..)

wie validiere ich richtig:

art und weiße wie man ein datum  eingibt, wird geläst in bag end. Geb: "YYYY-MM-DD" so passt 

front end macht es wie es passiert 


- ✅ Use `Field(...)` constraints fluently
- ✅ Write `field_validator` and `model_validator` functions
- ✅ Choose between Optional, default, and required
- ✅ Read and explain Pydantic 422 error responses
- ✅ Tighten loose models so bad data is rejected at the door

---

#### 2. 🚧 What challenges did I face?

unstrukturierter daten aufbau

edge tests 

hausaufgabe
modelle spezifisieren 
titellänge begränzen 
titel inhalt spezifisieren (teilenumbrüche verhindern)
eigene test erweitern, -> grenzfälle testen 
    reject short title 
    unnohen categrien...


lange nicht gemerkt, das ich uv add email-validator installieren muss


internatal serverer errer, probleme mit derr ntoes.json datei
---

#### 3. 💡 How did I overcome them?
uv add email-validator installiert im terminal
neues main.py aus unterricht und selbstarbeit übernommen 


notes.json gelöscht, wurde neu erstellt hat geklappt


---

### Day 6

#### 1. ✅ What did I accomplish?

gelernt das mein code noch nicht gut genung ist





---

#### 2. 🚧 What challenges did I face?

1. 20 faild 11 passed 97 errors

2. Fehlermeldung:
"msg":"Field required","loc":["body","author_email"]
(API erwartet im "Body" (also in den Daten, die geschickt werden) ein Feld namens author_email. Die Test-Suite schickt dieses Feld aber nicht mit.)

3. "msg":"Value error, Arbeits-Notizen brauchen zwingend den Tag 'work'."
Die Test-Suite erstellt aber Notizen mit der Kategorie "work", nutzt aber andere Tags (z. B. "sample", "test" oder "spaced"). Dein Code blockt das mit einem Fehler 422 ab, aber die Test-Suite erwartet Erfolg (201).

4.  Fehler  404 

5. Fehler durch reihnfolge 

6. 405 fehler, fastAPI findet den pfad /notes/{note_id} aber gibt dort keine funkton mit der methode put 

7. findet top tags nciht gut 

8. zu kurze tags werden angenommen 

9. created_after und created_before lehnt keine ungültigen daten bisher ab

10. list_notes datum führt zum absturz

11. Die Tests finden die Endpunkte /categories/... und /tags/... nicht.

12. API anwortet mit 201 (Erfolg), aber der Test erwartet 422, weil 11 Tags zu viele sind.

13. alle 70 tests wurden gescipped

14. Status 200 filtert noch nnicht richtig

15. Test schickt ein absichtlich falsches Datum (wie 2026-13-01 oder den Text not-a-date) und erwartet, dass deine API das mit einem Fehler 422 ablehnt.
---

#### 3. 💡 How did I overcome them?

1. erst mal author email optional gemacht

2. @model_validator raus hauen

3. Root-Endpunkt hinzufügen 
(keinen Endpunkt für @app.get("/") hast. Die Test-Suite erwartet dort eine Antwort.)

4. bei get notes filter logig hinzufüge nmit if 

5. endpunkte aus tag 3 wieder hinzufuügen 

6. 405 fehelr: endpunkt mit put hinzufügen für /notes/{note_id}

7. nutzen collections.Counter, um die Top-Tags leicht zu finden:

8. tag feld aktuallisieren

9. Typ in der Funktion von str auf date ändern. FastAPI validiert das Datum dann automatisch nach ISO-Standard.

10. nehme str um sie als text zu vergleichen, damit iso strings sortierbar sind.

11. Endpunkte in main.py kopieren

12. max_length Beschränkung

13. Server war nicht erreichbar


14. alle Filter (Kategorie, Suche, Tags und Datum) korrekt kombiniert:

15. Änderung  vom Anfang der list_notes Funktion in der main.py

---

## Week 3

### Day 7

#### 1. ✅ What did I accomplish?






---

#### 2. 🚧 What challenges did I face?






---

#### 3. 💡 How did I overcome them?






---

### Day 8

#### 1. ✅ What did I accomplish?






---

#### 2. 🚧 What challenges did I face?






---

#### 3. 💡 How did I overcome them?






---

### Day 9

#### 1. ✅ What did I accomplish?






---

#### 2. 🚧 What challenges did I face?






---

#### 3. 💡 How did I overcome them?






---


# 🎉 Congratulations! You did it! 🎓✨













