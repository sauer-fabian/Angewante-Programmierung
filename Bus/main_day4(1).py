from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime, timezone
from typing import Annotated, Optional
from sqlmodel import SQLModel, Field, Session, create_engine, Relationship, select, or_, col
from collections import Counter

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

class NoteCreate(BaseModel): # was wir von der API erwarten, erbt von BaseModel
    title: str
    content: str
    category: str # ← Task 1: Kategorie hinzugefügt
    tags: list[str] = []

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[list[str]] = None

class NoteResponse(BaseModel): # was wir zurückgeben wollen, erbt von NoteCreate
    id: int
    title: str
    content: str
    category: str # ← Task 1: Kategorie hinzugefügt
    tags: list[str]
    created_at: str
    
    class Config:
        from_attributes = True
# HIER: Die neue Verbindungstabelle (Schritt 1)
class NoteTagLink(SQLModel, table=True):
    __tablename__ = 'notelink'
    
    note_id: Optional[int] = Field(default=None, foreign_key="notes.id", primary_key=True)
    tag_id: Optional[int] = Field(default=None, foreign_key="tags.id", primary_key=True)

# Deine angepasste Notiz-Tabelle (Schritt 2)
class Note(SQLModel, table=True):
    __tablename__ = 'notes'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    category: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # HIER wurde link_model hinzugefügt
    tags: list["Tag"] = Relationship(back_populates="notes", link_model=NoteTagLink)

# Deine angepasste Tag-Tabelle (Schritt 3)
class Tag(SQLModel, table=True):
    __tablename__ = 'tags'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    
    # HIER wurde link_model hinzugefügt
    notes: list[Note] = Relationship(back_populates="tags", link_model=NoteTagLink)

# Hier wird die engine erstellt – danach sollte das Wort oben lila werden
engine = create_engine("sqlite:///notes.db")

# Damit werden die Tabellen in der Datei angelegt
SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

### Create post

@app.post("/notes", status_code=201) # wenn jemand eine POST Anfrage an /notes sendet, wird die Funktion create_note aufgerufen
def create_note(note: NoteCreate, session: SessionDep) -> NoteResponse:
    """Create a new note"""
    db_note = Note(
        title=note.title,
        content=note.content,
        category=note.category
    )
    
    tag_objects = []
    seen_tags = set()
    
    for tag_name in note.tags:
        tag_name_lower = tag_name.lower().strip()
        if not tag_name_lower or tag_name_lower in seen_tags:
            continue
        
        seen_tags.add(tag_name_lower)
        
        statement = select(Tag).where(Tag.name == tag_name_lower)
        existing_tag = session.exec(statement).first()
        
        if existing_tag:
            tag_objects.append(existing_tag)
        else:
            new_tag = Tag(name=tag_name_lower)
            session.add(new_tag)
            tag_objects.append(new_tag)
    
    db_note.tags = tag_objects
    
    session.add(db_note)
    session.commit()
    session.refresh(db_note)
    
    return NoteResponse(
        id=db_note.id,
        title=db_note.title,
        content=db_note.content,
        category=db_note.category,
        tags=[tag.name for tag in db_note.tags],
        created_at=db_note.created_at.isoformat()
    )

##############################################################################
#### Get Notes  (Day 2) Endpunkte  (Day 3) + GET/PUT/DELETET/ hinzufügen
#############################################################################

@app.get("/notes") # wenn jemand eine GET Anfrage an /notes sendet, wird die Funktion get_notes aufgerufen
def list_notes(
    session: SessionDep,
    category: str = None,
    search: str = None,
    tag: str = None,
    created_after: str = None,
    created_before: str = None
) -> list[NoteResponse]:
    """Get all notes"""
    statement = select(Note)
    
    if category:
        statement = statement.where(Note.category == category)
    
    if search:
        search_lower = search.lower()
        statement = statement.where(
            or_(
                col(Note.title).ilike(f"%{search_lower}%"),
                col(Note.content).ilike(f"%{search_lower}%")
            )
        )
    
    if tag:
        tag_lower = tag.lower()
        statement = statement.join(Note.tags).where(Tag.name == tag_lower)
        
    notes = session.exec(statement).all()
    
    filtered_notes = []
    for n in notes:
        if created_after and n.created_at.isoformat() < created_after:
            continue
        if created_before and n.created_at.isoformat() > created_before:
            continue
        filtered_notes.append(n)
    
    return [
        NoteResponse(
            id=n.id,
            title=n.title,
            content=n.content,
            category=n.category,
            tags=[t.name for t in n.tags],
            created_at=n.created_at.isoformat()
        )
        for n in filtered_notes
    ]

@app.put("/notes/{note_id}")
def update_note(note_id: int, note_update: NoteCreate, session: SessionDep) -> NoteResponse:
    db_note = session.get(Note, note_id)
    if not db_note:
        raise HTTPException(status_code=404, detail=f"Note with ID {note_id} not found")
        
    db_note.title = note_update.title
    db_note.content = note_update.content
    db_note.category = note_update.category
    
    tag_objects = []
    seen_tags = set()
    for tag_name in note_update.tags:
        tag_name_lower = tag_name.lower().strip()
        if not tag_name_lower or tag_name_lower in seen_tags:
            continue
        seen_tags.add(tag_name_lower)
        statement = select(Tag).where(Tag.name == tag_name_lower)
        existing_tag = session.exec(statement).first()
        if existing_tag:
            tag_objects.append(existing_tag)
        else:
            new_tag = Tag(name=tag_name_lower)
            session.add(new_tag)
            tag_objects.append(new_tag)
            
    db_note.tags = tag_objects
    
    session.add(db_note)
    session.commit()
    session.refresh(db_note)
    
    return NoteResponse(
        id=db_note.id,
        title=db_note.title,
        content=db_note.content,
        category=db_note.category,
        tags=[tag.name for tag in db_note.tags],
        created_at=db_note.created_at.isoformat()
    )

@app.patch("/notes/{note_id}")
def partial_update_note(note_id: int, note_update: NoteUpdate, session: SessionDep) -> NoteResponse:
    db_note = session.get(Note, note_id)
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
        
    if note_update.title is not None:
        db_note.title = note_update.title
    if note_update.content is not None:
        db_note.content = note_update.content
    if note_update.category is not None:
        db_note.category = note_update.category
        
    if note_update.tags is not None:
        tag_objects = []
        seen_tags = set()
        for tag_name in note_update.tags:
            tag_name_lower = tag_name.lower().strip()
            if not tag_name_lower or tag_name_lower in seen_tags:
                continue
            seen_tags.add(tag_name_lower)
            statement = select(Tag).where(Tag.name == tag_name_lower)
            existing_tag = session.exec(statement).first()
            if existing_tag:
                tag_objects.append(existing_tag)
            else:
                new_tag = Tag(name=tag_name_lower)
                session.add(new_tag)
                tag_objects.append(new_tag)
        db_note.tags = tag_objects
        
    session.add(db_note)
    session.commit()
    session.refresh(db_note)
    
    return NoteResponse(
        id=db_note.id,
        title=db_note.title,
        content=db_note.content,
        category=db_note.category,
        tags=[tag.name for tag in db_note.tags],
        created_at=db_note.created_at.isoformat()
    )


##################################################################
#### Tags hinzufügen (Day 3)
##################################################################

@app.get("/tags")
def list_tags(session: SessionDep) -> list[str]:
    statement = select(Tag)
    tags = session.exec(statement).all()
    return sorted([tag.name for tag in tags])

@app.get("/tags/{tag_name}/notes")
def get_notes_by_tag(tag_name: str, session: SessionDep) -> list[NoteResponse]:
    tag_lower = tag_name.lower()
    statement = select(Tag).where(Tag.name == tag_lower)
    tag = session.exec(statement).first()
    
    if not tag:
        return []
        
    return [
        NoteResponse(
            id=note.id,
            title=note.title,
            content=note.content,
            category=note.category,
            tags=[t.name for t in note.tags],
            created_at=note.created_at.isoformat()
        )
        for note in tag.notes
    ]


##################################################################
#### AUFGABEN (Homework & Bonus)
##################################################################

# GET specific note by ID 
@app.get("/notes/{note_id}")
def get_note(note_id: int, session: SessionDep) -> NoteResponse:
    """Get a specific note by ID"""
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail=f"Note with ID {note_id} not found")
    
    return NoteResponse(
        id=note.id,
        title=note.title,
        content=note.content,
        category=note.category,
        tags=[tag.name for tag in note.tags],
        created_at=note.created_at.isoformat()
    )

# Filter Notes by Category 
@app.get("/categories/{category_name}/notes")
def get_notes_by_category(category_name: str, session: SessionDep) -> list[NoteResponse]:
    """Get all notes in a specific category"""
    statement = select(Note).where(Note.category == category_name)
    notes = session.exec(statement).all()
    
    return [
        NoteResponse(
            id=n.id,
            title=n.title,
            content=n.content,
            category=n.category,
            tags=[t.name for t in n.tags],
            created_at=n.created_at.isoformat()
        )
        for n in notes
    ]

# Add Statistics Endpoint 
@app.get("/notes/stats")
def get_notes_stats(session: SessionDep):
    """Get statistics about notes"""
    notes = session.exec(select(Note)).all()
    
    # Count by category
    categories = {}
    for note in notes:
        if note.category in categories:
            categories[note.category] += 1
        else:
            categories[note.category] = 1
    
    all_tags = []
    for note in notes:
        for tag in note.tags:
            all_tags.append(tag.name)
            
    tag_counts = Counter(all_tags)
    
    top_5_tags = []
    for tag, count in tag_counts.most_common(5):
        top_5_tags.append({"tag": tag, "count": count})
        
    unique_tags = len(tag_counts)
    
    return {
        "total_notes": len(notes),
        "by_category": categories,
        "top_tags": top_5_tags,
        "unique_tags_count": unique_tags
    }

# Bonus Add DELETE endpoint 
@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int, session: SessionDep):
    """Delete a note by ID"""
    db_note = session.get(Note, note_id)
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
        
    session.delete(db_note)
    session.commit()
    return

@app.get("/categories")
def list_categories(session: SessionDep) -> list[str]:
    notes = session.exec(select(Note)).all()
    all_categories = set()
    for note in notes:
        all_categories.add(note.category)
    return sorted(list(all_categories))