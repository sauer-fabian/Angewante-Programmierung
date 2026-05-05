from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timezone
from pathlib import Path
from collections import Counter
from typing import Optional

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime
from typing import Annotated, Optional
from sqlmodel import SQLModel, Field, Session, create_engine, Relationship, select, or_, col

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
#### Note API Endpoints (Day 2) + Datenbank (Day 3)
#################################

# Was man beim Erstellen mitschickt
class NoteCreate(BaseModel):
    title: str
    content: str
    category: str
    tags: list[str] = []

# Was man beim Ändern mitschickt
class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[list[str]] = None

# Was das Programm zurückgibt
class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    category: str
    tags: list[str]
    created_at: str
    
    class Config:
        from_attributes = True

# Tabelle für Notizen in der Datenbank
class Note(SQLModel, table=True):
    __tablename__ = 'notes'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    category: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Verbindung zu Tags
    tags: list["Tag"] = Relationship(back_populates="notes")

# Tabelle für Tags in der Datenbank
class Tag(SQLModel, table=True):
    __tablename__ = 'tags'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    
    # Verbindung zu Notizen
    notes: list[Note] = Relationship(back_populates="tags")

# Datenbank erstellen
engine = create_engine("sqlite:///notes.db")
SQLModel.metadata.create_all(engine)

# Verbindung zur Datenbank herstellen
def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

### Create post
@app.post("/notes", status_code=201)
def create_note(note: NoteCreate, session: SessionDep) -> NoteResponse:
    
    # Notiz für Datenbank vorbereiten
    db_note = Note(
        title=note.title,
        content=note.content,
        category=note.category
    )
    
    # Tags prüfen und anlegen
    tag_objects = []
    seen_tags = set()
    
    for tag_name in note.tags:
        tag_name_lower = tag_name.lower().strip()
        if not tag_name_lower or tag_name_lower in seen_tags:
            continue
        
        seen_tags.add(tag_name_lower)
        
        # Prüfen, ob Tag schon in der Datenbank ist
        statement = select(Tag).where(Tag.name == tag_name_lower)
        existing_tag = session.exec(statement).first()
        
        if existing_tag:
            tag_objects.append(existing_tag)
        else:
            new_tag = Tag(name=tag_name_lower)
            session.add(new_tag)
            tag_objects.append(new_tag)
    
    db_note.tags = tag_objects
    
    # In Datenbank speichern
    session.add(db_note)
    session.commit()
    session.refresh(db_note)
    
    # Ausgabe zurückgeben
    return NoteResponse(
        id=db_note.id,
        title=db_note.title,
        content=db_note.content,
        category=db_note.category,
        tags=[tag.name for tag in db_note.tags],
        created_at=db_note.created_at.isoformat()
    )

##############################################################################
#### (Get Notes  (Day 2)) Endpunkte  (Day 3) + GET/PUT/DELETET/ hinzufügen
#############################################################################

#@app.get("/notes") # wenn jemand eine GET Anfrage an /notes sendet, wird die Funktion get_notes aufgerufen
#def get_notes() -> list[Note]:
    """Get all notes"""
    # FIX: load_notes() gibt nichts mehr zurück! Wir greifen einfach auf die globale Variable zu.
    return notes_db # Notizen an Client zurückgeben


@app.get("/notes")
def list_notes(
    category: str = None,
    search: str = None,
    tag: str = None,
    created_after: str = None,
    created_before: str = None
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
        
        # Neue Datums-Filter
        if created_after and note.created_at < created_after:
            continue
            
        if created_before and note.created_at > created_before:
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

@app.patch("/notes/{note_id}")
def partial_update_note(note_id: int, note_update: NoteUpdate) -> Note:
    
    for i, note in enumerate(notes_db):
        if note.id == note_id:
            
            if note_update.title is not None:
                note.title = note_update.title
            if note_update.content is not None:
                note.content = note_update.content
            if note_update.category is not None:
                note.category = note_update.category
            if note_update.tags is not None:
                note.tags = note_update.tags
            
            notes_db[i] = note
            save_notes()
            return note
    
    raise HTTPException(status_code=404, detail="Note not found")

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
#### Homework Bonus (Day 2)
##################################################################

# GET specific note by ID 
#@app.get("/notes/{note_id}")
#def get_note(note_id: int):
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
#@app.get("/notes/category/{category}")
#def get_notes_by_category(category: str):
    """Get all notes in a specific category"""
    filtered_notes = []
    
    for note in notes_db:
        if note.category == category:
            filtered_notes.append(note)
    
    return filtered_notes

# Add Statistics Endpoint 
#@app.get("/notes/stats")
#def get_notes_stats():
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
#@app.delete("/notes/{note_id}")
#def delete_note(note_id: int):
    """Delete a note by ID"""
    
    for i, note in enumerate(notes_db):
        if note.id == note_id:
            notes_db.pop(i)  # Notiz aus der Liste entfernen
            save_notes()  # Geänderte Liste speichern
            return {"message": "Note deleted"}
    
    raise HTTPException(status_code=404, detail="Note not found")

@app.get("/notes/stats")
def get_notes_stats():
    
    # Kategorien zählen
    categories = {}
    for note in notes_db:
        if note.category in categories:
            categories[note.category] += 1
        else:
            categories[note.category] = 1
    
    # Alle Tags in eine Liste packen
    all_tags = []
    for note in notes_db:
        for tag in note.tags:
            all_tags.append(tag)
    
    # Tags zählen
    tag_counts = Counter(all_tags)
    
    # Die 5 häufigsten Tags aussortieren
    top_5_tags = []
    for tag, count in tag_counts.most_common(5):
        top_5_tags.append({"tag": tag, "count": count})
        
    # Anzahl aller verschiedenen Tags ermitteln
    unique_tags = len(tag_counts)
    
    return {
        "total_notes": len(notes_db),
        "by_category": categories,
        "top_tags": top_5_tags,
        "unique_tags_count": unique_tags
    }


@app.get("/categories")
def list_categories() -> list[str]:
    
    all_categories = set()
    for note in notes_db:
        all_categories.add(note.category)
    
    return sorted(list(all_categories))

@app.get("/categories/{category_name}/notes")
def get_notes_by_category(category_name: str) -> list[Note]:
    
    filtered = []
    for note in notes_db:
        if note.category == category_name:
            filtered.append(note)
    
    return filtered