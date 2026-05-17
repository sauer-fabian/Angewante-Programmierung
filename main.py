#-------- Importe ------------

from fastapi import FastAPI, HTTPException, Depends # Werkzeuge für die Web-Schnittstelle
from pydantic import BaseModel, Field, field_validator, ConfigDict # Prüfwerkzeug für Daten (z.B. Textlänge)
from datetime import datetime # Werkzeuge für aktuelle Datum
from typing import Optional, List #  legt Art von Import-Daten fest (darf auch leer stehen)
from collections import Counter # zählen von Elementen
import json # Textumwandlung
from sqlmodel import SQLModel, Field as TypeField, Session, create_engine, select # Für Datenbank 

# API starten
app = FastAPI(title="Notiz API", version="1.0.0") 

# --- DATENBANK EINRICHTEN ---

# Verbindung zur Datei notes.db herstellen
engine = create_engine("sqlite:///notes.db")

# Tabelle für die Datenbank definieren
class NoteTable(SQLModel, table=True):
    __tablename__ = "notes"

    id: Optional[int] = TypeField(default=None, primary_key=True) # ID wird automatisch vergeben
    title: str
    content: str
    category: str
    tags_json: str = "[]" # Listen werden als Text gespeichert
    created_at: str

# Datenbankdatei und Tabellen erzeugen
SQLModel.metadata.create_all(engine)

# Verbindung zur Datenbank öffnen und schließen
def get_db():
    with Session(engine) as session:
        yield session

# --- DATEN MODELLE ---

# Modell für PATCH 
class NoteUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    content: Optional[str] = Field(None, min_length=1)
    category: Optional[str] = None
    tags: Optional[List[str]] = None

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

# Modell für POST und PUT (Erstellen und Ersetzen)
class NoteCreate(BaseModel):

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    title: str = Field(min_length=3, max_length=100)
    content: str = Field(min_length=1)
    category: str

    tags: list[str] = Field(default_factory=list, max_length=10) 
    author_email: str | None = None

# Automatisches Aufräumen
    @field_validator("category")
    
    # alles in Kleinbuchstaben
    @classmethod
    def category_lowercase(cls, v: str) -> str:
        return v.lower()

    # Tags müssten min. aus 2 Zeichen bestehen und Dopplungen werden gelöscht 
    @field_validator("tags")
    @classmethod
    def clean_tags(cls, raw_tags: list[str]) -> list[str]:
        saubere_tags = []
        gesehene = set()
        for tag in raw_tags:
            t = tag.strip().lower()
            if len(t) < 2:
                raise ValueError("Tag zu kurz (min 2 Zeichen)")
            if t not in gesehene:
                saubere_tags.append(t)
                gesehene.add(t)
        return saubere_tags

# Datenbank-Text zurück in Liste umwandeln
def format_note(db_note: NoteTable) -> dict:
    return {
        "id": db_note.id,
        "title": db_note.title,
        "content": db_note.content,
        "category": db_note.category,
        "tags": json.loads(db_note.tags_json),
        "created_at": db_note.created_at
    }

# --- ENDPUNKTE ---

# Statistik ausgeben
@app.get("/notes/stats")
def get_stats(db: Session = Depends(get_db)):
    db_notes = db.exec(select(NoteTable)).all()
    notes = [format_note(n) for n in db_notes]
    
    if not notes:
        return {"total_notes": 0, "by_category": {}, "unique_tags_count": 0, "top_tags": []}
    
    cats = [n["category"] for n in notes]
    all_tags = []
    for n in notes:
        all_tags.extend(n["tags"])
    
    # Tags werden gezählt
    tags_count = Counter(all_tags)
    
    # 5 häufigsten Tags werden ermittelt
    top_tags = [{"tag": tag, "count": count} for tag, count in tags_count.most_common(5)]
        
    return {
        "total_notes": len(notes),
        "by_category": dict(Counter(cats)),
        "unique_tags_count": len(set(all_tags)),
        "top_tags": top_tags
    }

# Alle Kategorien auflisten
@app.get("/categories")
def list_categories(db: Session = Depends(get_db)):
    db_notes = db.exec(select(NoteTable)).all()
    cats = sorted(list(set(n.category for n in db_notes)))
    return cats

# Notizen einer bestimmten Kategorie anzeigen
@app.get("/categories/{category_name}/notes")
def get_notes_by_category(category_name: str, db: Session = Depends(get_db)):
    db_notes = db.exec(select(NoteTable).where(NoteTable.category == category_name.lower())).all()
    return [format_note(n) for n in db_notes]

# Alle Tags auflisten
@app.get("/tags")
def list_tags(db: Session = Depends(get_db)):
    db_notes = db.exec(select(NoteTable)).all()
    tags = set()
    for n in db_notes:
        tags.update(json.loads(n.tags_json))
    return sorted(list(tags))

# Notizen mit einem bestimmten Tag anzeigen
@app.get("/tags/{tag_name}/notes")
def get_notes_by_tag(tag_name: str, db: Session = Depends(get_db)):
    db_notes = db.exec(select(NoteTable)).all()
    notes = [format_note(n) for n in db_notes]
    filtered = [n for n in notes if tag_name.lower() in n["tags"]]
    return filtered

# Neue Notiz in Datenbank speichern
@app.post("/notes", status_code=201)
def create_note(note_in: NoteCreate, db: Session = Depends(get_db)):
    new_db_note = NoteTable(
        title=note_in.title,
        content=note_in.content,
        category=note_in.category,
        tags_json=json.dumps(note_in.tags),
        created_at=datetime.now().isoformat()
    )
    db.add(new_db_note)
    db.commit() # Speichern
    db.refresh(new_db_note) # Neue ID laden
    return format_note(new_db_note)

# Notizen suchen und filtern
@app.get("/notes")
def list_notes(
    category: Optional[str] = None,
    tag: Optional[str] = None,
    search: Optional[str] = None,
    created_after: Optional[datetime] = None,
    created_before: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    db_notes = db.exec(select(NoteTable)).all()
    notes = [format_note(n) for n in db_notes]
    filtered = notes

    #1. Filter nach Kategorie
    if category:
     # Filtert die Liste und behalten nur Notizen mit dieser Kategorie
        filtered = [n for n in filtered if n["category"].lower() == category.lower()]

    #2. Filter nach tag
    if tag:
     # Behalte nur Notizen, bei denen der gesuchte Tag in der Liste n.tags vorkommt
        filtered = [n for n in filtered if tag.lower() in [t.lower() for t in n["tags"]]]

    #  3. Suche in Titel oder Inhalt
    if search:
        s = search.lower()
        filtered = [n for n in filtered if s in n["title"].lower() or s in n["content"].lower()]

   # 4. Datumsfilter danach
    if created_after:
        filtered = [n for n in filtered if datetime.fromisoformat(n["created_at"]) >= created_after]
   # 5. Datumfiilter davor
    if created_before:
        filtered = [n for n in filtered if datetime.fromisoformat(n["created_at"]) <= created_before]

    return filtered

# Status prüfen (Server online?)
@app.get("/")
def read_root():
    return {"message": "Note API is running"}

# Einzelne Notiz über ID laden
@app.get("/notes/{note_id}")
def get_note(note_id: int, db: Session = Depends(get_db)):
    db_note = db.get(NoteTable, note_id)
    if db_note:
        return format_note(db_note)
    raise HTTPException(status_code=404, detail="Note not found") # Fehlermedldung, wenn es ID nicht gibt

# Einzelne Felder einer Notiz ändern
@app.patch("/notes/{note_id}")
def patch_note(note_id: int, update_data: NoteUpdate, db: Session = Depends(get_db)):
    db_note = db.get(NoteTable, note_id)
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
        
    stored_data = format_note(db_note)
    update_dict = update_data.model_dump(exclude_unset=True)
    stored_data.update(update_dict)
    
    db_note.title = stored_data["title"]
    db_note.content = stored_data["content"]
    db_note.category = stored_data["category"]
    db_note.tags_json = json.dumps(stored_data["tags"])
    
    db.add(db_note)
    db.commit() # Änderungen speichern
    db.refresh(db_note)
    return format_note(db_note)

# Komplette Notiz ersetzen/updaten
@app.put("/notes/{note_id}")
def update_note(note_id: int, note_in: NoteCreate, db: Session = Depends(get_db)):
    db_note = db.get(NoteTable, note_id)
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
        
    db_note.title = note_in.title
    db_note.content = note_in.content
    db_note.category = note_in.category
    db_note.tags_json = json.dumps(note_in.tags)
    
    db.add(db_note)
    db.commit() # Änderungen speichern
    db.refresh(db_note)
    return format_note(db_note)

# Notiz löschen
@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    db_note = db.get(NoteTable, note_id)
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
        
    db.delete(db_note)
    db.commit() # Eintrag löschen
    return