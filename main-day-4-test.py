from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime, timezone
from typing import Annotated, Optional
from sqlmodel import SQLModel, Field, Session, create_engine, Relationship, select, or_, col
from collections import Counter

# Server starten mit:
# uv run fastapi dev

app = FastAPI(
    title="Angewandte Programmierung Kurs",
    description="Einfache Notiz-Verwaltung API",
    version="1.0",
)

#################################
#### Datenbank Setup
#################################

class NoteTagLink(SQLModel, table=True):
    __tablename__ = 'notelink'
    note_id: Optional[int] = Field(default=None, foreign_key="notes.id", primary_key=True)
    tag_id: Optional[int] = Field(default=None, foreign_key="tags.id", primary_key=True)

class Note(SQLModel, table=True):
    __tablename__ = 'notes'
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    category: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    tags: list["Tag"] = Relationship(back_populates="notes", link_model=NoteTagLink)

class Tag(SQLModel, table=True):
    __tablename__ = 'tags'
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    notes: list[Note] = Relationship(back_populates="tags", link_model=NoteTagLink)

engine = create_engine("sqlite:///notes.db")
SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

#################################
#### Daten-Modelle
#################################

class NoteCreate(BaseModel): 
    title: str
    content: str
    category: str 
    tags: list[str] = []

class NoteResponse(BaseModel): 
    id: int
    title: str
    content: str
    category: str 
    tags: list[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

#################################
#### Endpunkte
#################################

@app.post("/notes", status_code=201, response_model=NoteResponse)
def create_note(note: NoteCreate, session: SessionDep):
    """Erstellt eine neue Notiz"""
    db_note = Note(
        title=note.title,
        content=note.content,
        category=note.category
    )
    
    tag_objects = []
    for tag_name in note.tags:
        tag_name_lower = tag_name.lower().strip()
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
    return db_note

@app.get("/notes", response_model=list[NoteResponse])
def list_notes(session: SessionDep):
    """Zeigt alle Notizen"""
    return session.exec(select(Note)).all()

@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int, session: SessionDep):
    """Löscht eine Notiz über die ID"""
    db_note = session.get(Note, note_id)
    if not db_note:
        raise HTTPException(status_code=404, detail="Notiz nicht gefunden")
    session.delete(db_note)
    session.commit()
    return