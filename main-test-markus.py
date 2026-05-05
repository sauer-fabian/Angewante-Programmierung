import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool

# Importiere deine App und die DB-Session-Funktion aus main.py
from main import app, get_session

# Erstelle eine temporäre Datenbank nur für die Tests im Arbeitsspeicher
sqlite_url = "sqlite://"
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False}, poolclass=StaticPool)

def get_test_session():
    with Session(engine) as session:
        yield session

# Überschreibe die normale Datenbank-Verbindung mit der Test-Datenbank
app.dependency_overrides[get_session] = get_test_session
client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    """Erstellt vor jedem Test frische Tabellen und löscht sie danach."""
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)


#################################
#### Deine 8 Extrem-Tests
#################################

# 1. Test: Chinesische Zeichen (Unicode Support)
def test_create_note_chinese_characters():
    payload = {
        "title": "你好", 
        "content": "这是一个测试 (Das ist ein Test)", 
        "category": "測試", 
        "tags": ["中文", "测试"]
    }
    response = client.post("/notes", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "你好"
    assert "中文" in [tag["name"] if isinstance(tag, dict) else tag for tag in data["tags"]]


# 2. Test: Emojis (Erweiterter Unicode Support)
def test_create_note_with_emojis():
    payload = {
        "title": "Raketenstart 🚀",
        "content": "Ganz viel Feuer 🔥🔥🔥",
        "category": "Weltraum 🌌",
        "tags": ["👽", "✨"]
    }
    response = client.post("/notes", json=payload)
    assert response.status_code == 201
    assert "🚀" in response.json()["title"]


# 3. Test: Ultra-langer Text (Lasttest für Content)
def test_create_note_ultra_long_content():
    # Erstellt einen String mit 100.000 Zeichen
    huge_string = "A" * 100000 
    payload = {
        "title": "Langes Dokument",
        "content": huge_string,
        "category": "Test",
        "tags": []
    }
    response = client.post("/notes", json=payload)
    assert response.status_code == 201
    assert len(response.json()["content"]) == 100000


# 4. Test: Ultra-hohe ID (Sollte 404 Not Found werfen, keinen Crash)
def test_delete_ultra_high_id():
    # Eine ID, die garantiert nicht existiert
    response = client.delete("/notes/999999999999999")
    # Deine App wirft laut Code manuell einen 404 Fehler, wenn die ID fehlt
    assert response.status_code == 404
    assert response.json()["detail"] == "Notiz nicht gefunden"


# 5. Test: Negative ID
def test_delete_negative_id():
    response = client.delete("/notes/-5")
    assert response.status_code == 404


# 6. Test: Massenhaft Tags auf einmal
def test_create_note_massive_tags():
    # Erstellt eine Liste mit 500 verschiedenen Tags ["tag0", "tag1", ...]
    massive_tags = [f"tag{i}" for i in range(500)]
    payload = {
        "title": "Tag Monster",
        "content": "Ich habe zu viele Tags",
        "category": "Test",
        "tags": massive_tags
    }
    response = client.post("/notes", json=payload)
    assert response.status_code == 201
    assert len(response.json()["tags"]) == 500


# 7. Test: SQL-Injection-Versuch
def test_sql_injection_strings():
    # Versucht, böswilligen SQL-Code einzuschleusen
    malicious_string = "Robert'); DROP TABLE notes;--"
    payload = {
        "title": malicious_string,
        "content": malicious_string,
        "category": malicious_string,
        "tags": [malicious_string]
    }
    response = client.post("/notes", json=payload)
    assert response.status_code == 201
    # SQLModel sichert das ab, der Text sollte einfach als normaler String gespeichert werden
    assert response.json()["title"] == malicious_string


# 8. Test: Whitespace und leere Strings in Tags
def test_empty_strings_and_whitespaces():
    payload = {
        "title": "   ", 
        "content": "", 
        "category": "\n", 
        "tags": ["   ", "", "  Hallo  "]
    }
    response = client.post("/notes", json=payload)
    assert response.status_code == 201
    data = response.json()
    
    # Da du in deinem Code tag_name.lower().strip() verwendest, 
    # sollten aus den Leerzeichen-Tags leere Strings werden und "  Hallo  " zu "hallo"
    assert "hallo" in data["tags"]
    assert "" in data["tags"]