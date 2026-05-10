from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator, ConfigDict, model_validator, EmailStr
from datetime import datetime
import json
from pathlib import Path
from typing import Optional
from typing_extensions import Self

app = FastAPI(title="Notiz API - Bulletproof Version", version="1.0.0")

# --- MODELLE ---

class NoteCreate(BaseModel):
    # Schritt D: Konfiguration (Strippen & Extra-Felder verbieten)
    model_config = ConfigDict(
        str_strip_whitespace=True, 
        extra="forbid"
    )

    # Schritt A: Felder mit harten Regeln
    title: str = Field(min_length=3, max_length=100)
    content: str = Field(min_length=1, max_length=10000)
    category: str = Field(min_length=2, max_length=30)
    tags: list[str] = Field(default_factory=list, max_length=10)
    # Dein E-Mail Feld
    author_email: EmailStr = Field(description="E-Mail des Erstellers")

    # Schritt B: Kategorie & Tags säubern
    @field_validator("category")
    @classmethod
    def category_lowercase(cls, v: str) -> str:
        return v.lower()

    @field_validator("tags")
    @classmethod
    def clean_tags(cls, raw_tags: list[str]) -> list[str]:
        saubere_tags = []
        gesehene = set()
        for tag in raw_tags:
            t = tag.strip().lower()
            if not t:
                raise ValueError("Ein Tag darf nicht leer sein.")
            if t not in gesehene:
                saubere_tags.append(t)
                gesehene.add(t)
        return saubere_tags

    # Schritt C: Cross-Field Logik (Kategorie 'work' braucht Tag 'work')
    @model_validator(mode="after")
    def check_work_tag(self) -> Self:
        if self.category == "work" and "work" not in self.tags:
            raise ValueError("Arbeits-Notizen brauchen zwingend den Tag 'work'.")
        return self

class Note(NoteCreate):
    id: int
    created_at: str

# --- SPEICHER-LOGIK ---
NOTES_FILE = Path("notes.json")

def load_notes():
    if not NOTES_FILE.exists():
        return [], 1
    with open(NOTES_FILE, "r") as f:
        data = json.load(f)
        notes = [Note(**n) for n in data]
        counter = max([n.id for n in notes], default=0) + 1
        return notes, counter

def save_notes(notes):
    with open(NOTES_FILE, "w") as f:
        json.dump([n.model_dump() for n in notes], f, indent=2)

# --- ENDPUNKTE ---

@app.post("/notes", status_code=201)
def create_note(note_in: NoteCreate):
    notes, counter = load_notes()
    new_note = Note(
        id=counter,
        created_at=datetime.now().isoformat(),
        **note_in.model_dump()
    )
    notes.append(new_note)
    save_notes(notes)
    return new_note

@app.get("/notes")
def list_notes():
    notes, _ = load_notes()
    return notes