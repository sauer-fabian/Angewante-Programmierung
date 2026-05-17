import requests
import pytest
from faker import Faker

# --- EINSTELLUNGEN ---

# Basis-URL für die lokalen Tests
BASE_URL = "http://127.0.0.1:8000"


# --- TESTS: ERSTELLEN (POST) ---

# Normale Notiz erfolgreich erstellen
def test_create_note():
    note_data = {
        "title": "Test Note",
        "content": "Das ist ein Test",
        "category": "Testing",
        "tags": ["test", "pytest"]
    }

    response = requests.post(f"{BASE_URL}/notes", json=note_data)

    assert response.status_code == 201

    data = response.json()
    assert data["title"] == "Test Note"
    assert data["content"] == "Das ist ein Test"
    assert data["category"] == "Testing"
    assert "id" in data
    assert "created_at" in data

# Fehler provozieren durch fehlende Pflichtfelder
def test_create_note_missing_fields():
    invalid_notes = [
        {
            "content": "Kein Titel",
            "category": "Test",
            "tags": []
        },
        {
            "title": "Kein Content",
            "category": "Test",
            "tags": []
        },
        {
            "title": "Kein Category",
            "content": "Content",
            "tags": []
        }
    ]

    for note_data in invalid_notes:
        response = requests.post(f"{BASE_URL}/notes", json=note_data)
        assert response.status_code == 422


# --- TESTS: ABRUFEN (GET) ---

# Ganze Liste aller Notizen abrufen
def test_list_notes():
    response = requests.get(f"{BASE_URL}/notes")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)

# Eine ganz bestimmte Notiz über die ID laden
def test_get_note_by_id():
    note_data = {
        "title": "Note für ID Test",
        "content": "Diese Note wird danach per ID gesucht",
        "category": "Testing",
        "tags": ["id-test"]
    }

    create_response = requests.post(f"{BASE_URL}/notes", json=note_data)
    assert create_response.status_code == 201

    created_note = create_response.json()
    note_id = created_note["id"]

    response = requests.get(f"{BASE_URL}/notes/{note_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == note_id
    assert data["title"] == "Note für ID Test"
    assert data["content"] == "Diese Note wird danach per ID gesucht"
    assert data["category"] == "Testing"

# Fehler bei der Suche nach nicht existierenden IDs prüfen
def test_get_nonexistent_note():
    for note_id in range(-10, 0):
        response = requests.get(f"{BASE_URL}/notes/{note_id}")

        assert note_id < 0
        assert response.status_code == 404

    for note_id in range(100000, 100010):
        response = requests.get(f"{BASE_URL}/notes/{note_id}")

        assert note_id >= 100000
        assert response.status_code == 404


# --- TESTS: ÜBERSCHREIBEN & ÄNDERN (PUT & PATCH) ---

# Komplette Notiz mit PUT ersetzen
def test_update_note():
    note_data = {
        "title": "Original",
        "content": "Original Content",
        "category": "Test",
        "tags": ["old"]
    }

    create_response = requests.post(f"{BASE_URL}/notes", json=note_data)
    note_id = create_response.json()["id"]

    updated_data = {
        "title": "Updated Title",
        "content": "Updated Content",
        "category": "Updated",
        "tags": ["new"]
    }

    response = requests.put(f"{BASE_URL}/notes/{note_id}", json=updated_data)
    assert response.status_code == 200

    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["content"] == "Updated Content"
    assert data["category"] == "Updated"
    assert data["tags"] == ["new"]

# PUT bei einer nicht existierenden ID
def test_update_nonexistent_note():
    updated_data = {
        "title": "Updated",
        "content": "Updated",
        "category": "Test",
        "tags": []
    }

    for note_id in range(-10, 0):
        response = requests.put(f"{BASE_URL}/notes/{note_id}", json=updated_data)

        assert note_id < 0
        assert response.status_code == 404

    for note_id in range(100000, 100010):
        response = requests.put(f"{BASE_URL}/notes/{note_id}", json=updated_data)

        assert note_id