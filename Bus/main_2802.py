from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timezone
import json
from pathlib import Path

## uv run fastapi dev

##2802

#################################
#### Defintion Endpoints (Day 1)
#################################

app = FastAPI()
@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/name/{name}") # wenn jemand ne anfrage stellt und die startet mit Name/{name}= frei definierbar (z.b Lisa) wählt funktion aus
def get_name(name: str):
    return {"message": f"Hello {name}"} # gibt zurück Hello Lisa

@app.get("/alter/{alter}") # wenn jemand ne anfrage stellt und die startet mit Name/{name}= frei definierbar (z.b Lisa) wählt funktion aus
def get_alter(alter: int):
    return {"message": f"in einen Jahr bist du {alter+1}"} # gibt zurück Hello Lisa

app = FastAPI(
    title="Angewante Programmierung Kurs",
    description="Simple note managment API",
    version="1.0",
)

#################################
#### Note API Endpoints (Day 2)
#################################

class NoteCreate(BaseModel): # was wir von der API erwarten, erbt von BaseModel
    title: str
    content: str

class Note(NoteCreate): # was wir zurückgeben wollen, erbt von NoteCreate
    id: int
    title: str
    content: str
    created_at: str

NOTES_FILE = Path("data/notes.json")

def load_notes():
    """Load notes from JSON file and return notes list and next ID counter"""
    notes_db = []
    note_id_counter = 1

    if NOTES_FILE.exists():
        with open(NOTES_FILE, 'r') as f:
            data = json.load(f)
            notes_db = [Note(**note) for note in data]

            # Set counter to max ID + 1
            if notes_db:
                note_id_counter = max(note.id for note in notes_db) + 1

    return notes_db, note_id_counter


def save_notes(notes_db): # schreibt die daten raus
    """Save notes to JSON file after each change"""
    # Ensure data directory exists
    NOTES_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(NOTES_FILE, 'w') as f:
        # Convert Note objects to dicts
        notes_data = [note.dict() for note in notes_db]
        json.dump(notes_data, f, indent=2)

@app.post("/notes", status_code=201) # wenn jemand eine POST Anfrage an /notes sendet, wird die Funktion create_note aufgerufen
def create_note(note: NoteCreate) -> Note:
    """Create a new note"""

    notes_db, note_id_counter = load_notes() # 2 Variablen: notes_db = liste mit allen Notizen, note_id_counter = nächster ID Counter

    new_note = Note( # Note Objekt erstellen
        id=note_id_counter,
        title=note.title,
        content=note.content,
        created_at=datetime.now(timezone.utc).isoformat() # aktuelle Zeit in UTC formatieren
    )

    notes_db.append(new_note) # neue Notiz zur Liste hinzufügen
    save_notes(notes_db) # Notizen in JSON Datei speichern

    return new_note # neue Notiz an Client zurückgeben

#################################
#### Get Notes  (Day 2)
#################################


@app.get("/notes") # wenn jemand eine GET Anfrage an /notes sendet, wird die Funktion get_notes aufgerufen
def get_notes() -> list[Note]:
    """Get all notes"""
    notes_db, _ = load_notes() # Notizen laden, wir brauchen nur die Notizen, nicht den ID Counter
    return notes_db # Notizen an Client zurückgeben

#################################
#### Homework  (Day 2)
#################################

