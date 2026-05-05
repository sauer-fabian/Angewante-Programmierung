from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timezone
import json
from pathlib import Path

# run server
# uv run fastapi dev


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
    title="Angewandte Programmierung Kurs",
    description="Simple note management API",
    version="1.0",
)

#################################
#### Note API Endpoints (Day 2)
#################################

class NoteCreate(BaseModel): # was wir von der API erwarten, erbt von BaseModel
    title: str
    content: str
    category: str 
    tags: list[str] = [] # Tags hinzugefügt, Standardwert ist eine leere Liste

class Note(NoteCreate): # was wir zurückgeben wollen, erbt von NoteCreate
    id: int
    title: str
    content: str
    category: str 
    tags: list[str] = [] # Tags hinzugefügt, Standardwert ist eine leere Liste
    created_at: str

NOTES_FILE = Path("data/notes.json") # Storage
notes_db = []
note_id_counter = 1

def load_notes(): # file funktion
    """Load notes from JSON file"""
    global notes_db, note_id_counter

    if NOTES_FILE.exists():
        with open(NOTES_FILE, 'r') as f:
            data = json.load(f)
            # FIX: Falls alte Notizen keine Kategorie haben, wird hier "default" gesetzt (wie bei deiner Freundin)
            notes_db = [
                Note(**{**note, "category": note.get("category", "default")}) 
                for note in data
            ]

            # Set counter to max ID + 1
            if notes_db:
                note_id_counter = max(note.id for note in notes_db) + 1

def save_notes(notes_db=None): # schreibt die daten raus (Parameter optional gemacht für Kompatibilität mit delete_note)
    """Save notes to JSON file after each change"""
    global notes_db # Nutze die globale Variable, falls nichts übergeben wird
    # Ensure data directory exists
    NOTES_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(NOTES_FILE, 'w') as f:
        # Convert Note objects to dicts
        notes_data = [note.dict() for note in notes_db]
        json.dump(notes_data, f, indent=2)

load_notes()



### Create post

@app.post("/notes", status_code=201) # wenn jemand eine POST Anfrage an /notes sendet, wird die Funktion create_note aufgerufen
def create_note(note: NoteCreate) -> Note:
    """Create a new note"""
    global note_id_counter

    new_note = Note( # Note Objekt erstellen
        id=note_id_counter,
        title=note.title,
        content=note.content,
        category=note.category, # ← Task 1: Kategorie wird jetzt mitgespeichert
        created_at=datetime.now(timezone.utc).isoformat() # aktuelle Zeit in UTC formatieren
    )

    notes_db.append(new_note) # neue Notiz zur Liste hinzufügen
    note_id_counter += 1

    save_notes() # Notizen in JSON Datei speichern

    return new_note # neue Notiz an Client zurückgeben

##############################################################################
#### Get Notes  (Day 2) Endpunkt ersetzen (Day 3) + GET/PUT/DELETET/ hinzufügen
#############################################################################

# @app.get("/notes") # wenn jemand eine GET Anfrage an /notes sendet, wird die Funktion get_notes aufgerufen
# def get_notes() -> list[Note]:
    """Get all notes"""
    # FIX: load_notes() gibt nichts mehr zurück! Wir greifen einfach auf die globale Variable zu.
    return notes_db # Notizen an Client zurückgeben

@app.get("/notes")
def list_notes(
    category: str = None,
    search: str = None,
    tag: str = None
) -> list[Note]:
    
    filtered = []
    for note in notes_db:
        if category and note.category != category:
            continue
        
        if search:
            search_lower = search.lower()
            title_match = search_lower in note.title.lower()
            content_match = search_lower in note.content.lower()
            if not (title_match or content_match):
                continue
        
        if tag and tag not in note.tags:
            continue
        
        filtered.append(note)
    
    return filtered

@app.put("/notes/{note_id}")
def update_note(note_id: int, note_update: NoteCreate) -> Note:
    
    for i, note in enumerate(notes_db):
        if note.id == note_id:
            updated_note = Note(
                id=note.id,
                title=note_update.title,
                content=note_update.content,
                category=note_update.category,
                tags=note_update.tags,
                created_at=note.created_at
            )
            
            notes_db[i] = updated_note
            save_notes()
            return updated_note
    
    raise HTTPException(
        status_code=404,
        detail=f"Note with ID {note_id} not found"
    )

@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int):
    
    for i, note in enumerate(notes_db):
        if note.id == note_id:
            notes_db.pop(i)
            save_notes()
            return  
    
    raise HTTPException(
        status_code=404,
        detail=f"Note with ID {note_id} not found"
    )

##################################################################
#### Tags hinzufügen (Day 3)
##################################################################
@app.get("/tags")
def list_tags() -> list[str]:
    
    all_tags = set()
    for note in notes_db:
        for tag in note.tags:
            all_tags.add(tag)
    
    return sorted(list(all_tags))

@app.get("/tags/{tag_name}/notes")
def get_notes_by_tag(tag_name: str) -> list[Note]:
    
    filtered = []
    for note in notes_db:
        if tag_name in note.tags:
            filtered.append(note)
    
    return filtered

##################################################################
#### AUFGABEN (Homework & Bonus) (Day 2)
##################################################################

# GET specific note by ID 
@app.get("/notes/{note_id}")
def get_note(note_id: int):
    """Get a specific note by ID"""
    
    for note in notes_db:
        if note.id == note_id:
            return note
    
    # Not found - raise 404 error
    raise HTTPException(
        status_code=404,
        detail=f"Note with ID {note_id} not found"
    )

# Filter Notes by Category 
@app.get("/notes/category/{category}")
def get_notes_by_category(category: str):
    """Get all notes in a specific category"""
    filtered_notes = []
    
    for note in notes_db:
        if note.category == category:
            filtered_notes.append(note)
    
    return filtered_notes

# Add Statistics Endpoint 
@app.get("/notes/stats")
def get_notes_stats():
    """Get statistics about notes"""
    
    # Count by category
    categories = {}
    for note in notes_db:
        if note.category in categories:
            categories[note.category] += 1
        else:
            categories[note.category] = 1
    
    return {
        "total_notes": len(notes_db),
        "by_category": categories
    }

# Bonus Add DELETE endpoint 
@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    """Delete a note by ID"""
    
    for i, note in enumerate(notes_db):
        if note.id == note_id:
            notes_db.pop(i)  # Notiz aus der Liste entfernen
            save_notes()  # Geänderte Liste speichern
            return {"message": "Note deleted"}
    
    raise HTTPException(status_code=404, detail="Note not found")
