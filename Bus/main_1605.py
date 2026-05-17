from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator, ConfigDict, model_validator, EmailStr
from datetime import datetime
import json
from pathlib import Path
from typing import Optional
from typing_extensions import Self
from datetime import date
from pydantic import BaseModel, Field, field_validator
from typing import List, Dict
from collections import Counter
from sqlmodel import SQLModel, Field, Session, create_engine, select
from typing import List, Dict

# FastAPI Instanz erstellen - Der Einstiegspunkt unserer API
app = FastAPI(title="Notiz API - Bulletproof Version", version="1.0.0")

# --- MODELLE ---

class Note(SQLModel, table=True):
    __tablename__ = "notes"

    id: Optional[int] = Field(default=None, primary_key=True) # Die ID wird automatisch hochgezählt
    title: str = Field(min_length=3, max_length=100)
    content: str = Field(min_length=1)
    category: str
    tags_raw: str = Field(default="[]") # Wir speichern die Liste als Text
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())

# Für den PATCH Endpunkt (alle Felder sind optional)
class NoteUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    content: Optional[str] = Field(None, min_length=1)
    category: Optional[str] = None
    tags: Optional[List[str]] = None

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

class NoteCreate(BaseModel):
    # Schritt D: Konfiguration (Strippen & Extra-Felder verbieten)
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    title: str = Field(min_length=3, max_length=100)
    content: str = Field(min_length=1)
    category: str
    # Hier max_length=10 hinzufügen:
    tags: list[str] = Field(default_factory=list, max_length=10) 
    author_email: str | None = None

    # Schritt B: Kategorie & Tags säubern
    @field_validator("category")
    @classmethod
    def category_lowercase(cls, v: str) -> str:
        return v.lower() # Macht Eingaben einheitlich klein

    @field_validator("tags")
    @classmethod
    def clean_tags(cls, raw_tags: list[str]) -> list[str]:
        # Logik um Duplikate zu entfernen und Leer-Tags zu verhindern
        saubere_tags = []
        gesehene = set()
        for tag in raw_tags:
            t = tag.strip().lower()
            if len(t) < 2: # Regel: Mindestens 2 Zeichen
                raise ValueError("Tag zu kurz (min 2 Zeichen)")
            if t not in gesehene:
                saubere_tags.append(t)
                gesehene.add(t)
        return saubere_tags

    # Schritt C: Cross-Field Logik (Abhängigkeit zwischen zwei Feldern prüfen)
    #@model_validator(mode="after")
    #def check_work_tag(self) -> Self:
        # Prüft Kombination: Wenn Kategorie X, dann muss Tag Y da sein
       # if self.category == "work" and "work" not in self.tags:
       #     raise ValueError("Arbeits-Notizen brauchen zwingend den Tag 'work'.")
       # return self

# Vererbung: Note hat alles von NoteCreate + ID und Zeitstempel
class Note(NoteCreate):
    id: int
    created_at: str


# --- SPEICHER-LOGIK ---
NOTES_FILE = Path("notes.json")

def load_notes():
    # Lädt Daten aus JSON und wandelt sie in Pydantic-Objekte um
    if not NOTES_FILE.exists():
        return [], 1
    with open(NOTES_FILE, "r") as f:
        data = json.load(f)
        notes = [Note(**n) for n in data] # Entpacken der Dicts in das Modell
        counter = max([n.id for n in notes], default=0) + 1
        return notes, counter

def save_notes(notes):
    # Speichert Objekte als sauberes JSON-Format ab
    with open(NOTES_FILE, "w") as f:
        json.dump([n.model_dump() for n in notes], f, indent=2)

# --- ENDPUNKTE ---
@app.get("/notes/stats")
def get_stats():
    notes, _ = load_notes()
    if not notes:
        return {"total_notes": 0, "by_category": {}, "unique_tags_count": 0, "top_tags": []}
    
    cats = [n.category for n in notes]
    all_tags = []
    for n in notes:
        all_tags.extend(n.tags)
    
    # Zähle die Häufigkeit der Tags
    tag_counts = Counter(all_tags)
    # Erstelle Liste der Top 5 Tags im Format {"tag": "name", "count": X}
    top_tags = [{"tag": tag, "count": count} for tag, count in tag_counts.most_common(5)]
        
    return {
        "total_notes": len(notes),
        "by_category": dict(Counter(cats)),
        "unique_tags_count": len(set(all_tags)),
        "top_tags": top_tags
    }

@app.get("/categories")
def list_categories():
    notes, _ = load_notes()
    # Erstellt eine sortierte Liste aller einzigartigen Kategorien
    cats = sorted(list(set(n.category for n in notes)))
    return cats

@app.get("/categories/{category_name}/notes")
def get_notes_by_category(category_name: str):
    notes, _ = load_notes()
    # Filtert Notizen nach der Kategorie im Pfad
    filtered = [n for n in notes if n.category == category_name.lower()]
    return filtered

@app.get("/tags")
def list_tags():
    notes, _ = load_notes()
    tags = set()
    for n in notes:
        tags.update(n.tags)
    return sorted(list(tags))

@app.get("/tags/{tag_name}/notes")
def get_notes_by_tag(tag_name: str):
    notes, _ = load_notes()
    # Filtert Notizen, die den Tag aus dem Pfad enthalten
    filtered = [n for n in notes if tag_name.lower() in n.tags]
    return filtered

@app.post("/notes", status_code=201) # 201 = Created
def create_note(note_in: NoteCreate):
    notes, counter = load_notes()
    # Neues Objekt erstellen und validierte Daten (note_in) reinmischen
    new_note = Note(
        id=counter,
        created_at=datetime.now().isoformat(),
        **note_in.model_dump() # Packt alle Felder aus NoteCreate hier rein
    )
    notes.append(new_note)
    save_notes(notes)
    return new_note

# WICHTIG: Stelle sicher, dass "datetime" oben importiert ist!
from datetime import datetime
@app.get("/notes")
def list_notes(
    category: Optional[str] = None,
    tag: Optional[str] = None,
    search: Optional[str] = None,
    created_after: Optional[datetime] = None,
    created_before: Optional[datetime] = None
):
    notes, _ = load_notes()
    filtered = notes

    # 1. Filter nach Kategorie
    if category:
        # Wir filtern die Liste und behalten nur Notizen mit dieser Kategorie
        filtered = [n for n in filtered if n.category.lower() == category.lower()]
    
    # 2. Filter nach Tag
    if tag:
        # Behalte nur Notizen, bei denen der gesuchte Tag in der Liste n.tags vorkommt
        filtered = [n for n in filtered if tag.lower() in [t.lower() for t in n.tags]]

    # 3. Suche in Titel ODER Inhalt
    if search:
        s = search.lower()
        filtered = [n for n in filtered if s in n.title.lower() or s in n.content.lower()]

    # 4. Datumsfilter
    if created_after:
        # Wir wandeln den Zeitstempel der Notiz in ein datetime Objekt um zum Vergleich
        filtered = [n for n in filtered if datetime.fromisoformat(n.created_at) >= created_after]
    
    if created_before:
        filtered = [n for n in filtered if datetime.fromisoformat(n.created_at) <= created_before]

    return filtered

@app.get("/")
def read_root():
    return {"message": "Note API is running"}

@app.get("/notes/{note_id}")
def get_note(note_id: int):
    notes, _ = load_notes()
    for n in notes:
        if n.id == note_id:
            return n
    raise HTTPException(status_code=404, detail="Note not found")

@app.patch("/notes/{note_id}")
def patch_note(note_id: int, update_data: NoteUpdate):
    notes, _ = load_notes()
    for i, n in enumerate(notes):
        if n.id == note_id:
            # Nur Felder aktualisieren, die geschickt wurden
            stored_data = n.model_dump()
            update_dict = update_data.model_dump(exclude_unset=True)
            stored_data.update(update_dict)
            
            updated_note = Note(**stored_data)
            notes[i] = updated_note
            save_notes(notes)
            return updated_note
            
    raise HTTPException(status_code=404, detail="Note not found")

@app.put("/notes/{note_id}")
def update_note(note_id: int, note_in: NoteCreate):
    notes, _ = load_notes()
    for i, n in enumerate(notes):
        if n.id == note_id:
            # PUT ersetzt alles (außer ID und Erstellungsdatum)
            updated_note = Note(
                id=n.id,
                created_at=n.created_at,
                **note_in.model_dump()
            )
            notes[i] = updated_note
            save_notes(notes)
            return updated_note
    raise HTTPException(status_code=404, detail="Note not found")

@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int):
    notes, _ = load_notes()
    for i, n in enumerate(notes):
        if n.id == note_id:
            notes.pop(i)
            save_notes(notes)
            return
    raise HTTPException(status_code=404, detail="Note not found")