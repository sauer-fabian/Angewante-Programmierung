# ============================================================================
# DAY 4: Advanced API Features
# ============================================================================
# Goal: Write and run tests for our APIs
#       - Use pytest to write unit tests for our API endpoints
#       - Use FastAPI's TestClient to simulate API requests
#       - Use Requests library to test API endpoints from outside the app
# Topics: Testing FastAPI applications, pytest, TestClient, Requests library
# ============================================================================
import pytest
import requests
from faker import Faker

fake = Faker()

BASE_URL = "http://localhost:8000"

def test_read_root():
    """Welcome endpoint - returns greeting message"""
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Hello World!"

def test_check_404_Error():
    """Test that requesting a non-existent endpoint returns a 404 error."""
    response = requests.get(f"{BASE_URL}/nonexistent")
    assert response.status_code == 404

def test_check_greetings():
    """Test the personalized greeting endpoint with a sample name."""
    for _ in range(10):
        # Korrigiert: Nutze 'fake', wie oben definiert
        name = fake.first_name()
        response = requests.get(f"{BASE_URL}/greetings/{name}")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == f"Hello {name}!"

def test_is_adult():
    """Test if Check Adult works"""
    # Beispiel für einen POST-Request oder Query-Parameter (je nachdem wie dein Endpoint aussieht)
    # Hier nehmen wir an, das Alter wird als Query-Parameter übergeben:
    test_age = 20
    response = requests.get(f"{BASE_URL}/is_adult?age={test_age}")
    
    assert response.status_code == 200
    # Hier kannst du weitere Asserts hinzufügen, z.B.:
    # assert response.json()["is_adult"] == True

def test_check_greetings():
    """Test the personalized greeting endpoint with a sample name."""
    for _ in range(10):
        # Nutze 'fake' (dein Faker-Objekt aus Zeile 12/13)
        name = fake.first_name()
        response = requests.get(f"{BASE_URL}/greetings/{name}")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == f"Hello {name}!"

def test_is_adult():
    """Test if Check Adult works"""
    age = 18
    # Wir senden die Anfrage an den Pfad /is-adult/{age}
    response = requests.get(f"{BASE_URL}/is-adult/{age}")
    
    assert response.status_code == 200
    data = response.json()
    
    # Überprüfung, ob das Ergebnis im JSON korrekt ist
    assert data["is_adult"] == True