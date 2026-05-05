import pytest
from fastapi.testclient import TestClient
from main import app # Hier 'main' durch den Namen deiner Datei ersetzen

client = TestClient(app)

def test_status_404():
    """1. Test: Nicht existierende Seite aufrufen"""
    response = client.get("/nicht-da")
    assert response.status_code == 404

def test_get_all_notes():
    """2. Test: Liste aller Notizen abrufen"""
    response = client.get("/notes")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_simple_note():
    """3. Test: Eine einfache Notiz anlegen"""
    payload = {"title": "Test", "content": "Text", "category": "Test", "tags": []}
    response = client.post("/notes", json=payload)
    assert response.status_code == 201

def test_create_note_with_tags():
    """4. Test: Notiz mit Tags anlegen"""
    payload = {"title": "Tag-Test", "content": "Inhalt", "category": "Arbeit", "tags": ["wichtig"]}
    response = client.post("/notes", json=payload)
    assert response.status_code == 201
    assert "wichtig" in response.json()["tags"]

def test_check_notes_list():
    """5. Test: Abrufen der Notizen-Liste nach Erstellung"""
    response = client.get("/notes")
    assert response.status_code == 200

def test_delete_wrong_id():
    """6. Test: Löschen einer ID, die nicht existiert"""
    response = client.delete("/notes/9999")
    assert response.status_code == 404

def test_create_and_delete_specific():
    """
    7. Test: Notiz ANLEGEN
    8. Test: Genau diese Notiz LÖSCHEN
    """
    # Schritt 7: Anlegen
    payload = {"title": "Lösch-Test", "content": "Weg damit", "category": "Temp", "tags": []}
    create_res = client.post("/notes", json=payload)
    note_id = create_res.json()["id"]
    assert create_res.status_code == 201

    # Schritt 8: Genau dieses Objekt wieder löschen
    del_res = client.delete(f"/notes/{note_id}")
    assert del_res.status_code == 204

    # Prüfen, ob ID weg ist
    check = client.get("/notes")
    ids = [n["id"] for n in check.json()]
    assert note_id not in ids