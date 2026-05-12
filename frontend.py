import streamlit as st
import requests

# Die Adresse deiner API
API_URL = "http://127.0.0.1:8000"

st.title("Notiz-Verwaltung")

# 1. Bereich: Notizen anzeigen
st.header("Vorhandene Notizen")

# Daten von der eigenen API abrufen
antwort_laden = requests.get(f"{API_URL}/notes")

if antwort_laden.status_code == 200:
    notizen = antwort_laden.json()
    if notizen:
        # Eine Liste nur mit den Titeln erstellen
        titel_liste = [n["title"] for n in notizen]
        auswahl = st.selectbox("Wähle eine Notiz aus:", titel_liste)

        # Details der gewählten Notiz suchen und anzeigen
        for n in notizen:
            if n["title"] == auswahl:
                st.write(f"**Inhalt:** {n['content']}")
                st.write(f"**Kategorie:** {n['category']}")
                st.write(f"**Tags:** {', '.join(n['tags'])}")
    else:
        st.info("Keine Notizen gefunden.")
else:
    st.error("Konnte Notizen nicht laden.")

# 2. Bereich: Neue Notiz erstellen
st.header("Neue Notiz schreiben")

with st.form("erstellen"):
    titel_neu = st.text_input("Titel")
    inhalt_neu = st.text_area("Inhalt")
    kategorie_neu = st.text_input("Kategorie")
    tags_neu = st.text_input("Tags (mit Komma trennen)")
    
    knopf = st.form_submit_button("Speichern")

if knopf:
    if titel_neu and inhalt_neu:
        # Den Text bei Kommas trennen und in eine Liste umwandeln
        tag_liste = [t.strip() for t in tags_neu.split(",") if t.strip()]
        
        daten = {
            "title": titel_neu,
            "content": inhalt_neu,
            "category": kategorie_neu,
            "tags": tag_liste
        }
        
        # Daten an die API senden
        ergebnis = requests.post(f"{API_URL}/notes", json=daten)
        
        if ergebnis.status_code == 201:
            st.success("Notiz wurde gespeichert!")
            st.rerun() # Seite neu laden, um die Liste zu aktualisieren
        else:
            st.error(f"Fehler: {ergebnis.text}")

            # Überschrift für das Formular
st.header("Neue Notiz schreiben")

# Das Formular startet hier
with st.form("notiz_erstellen"):
    # Eingabefeld für den Namen der Notiz
    titel_neu = st.text_input("Titel der Notiz")
    
    # Großes Feld für den Text der Notiz
    inhalt_neu = st.text_area("Inhalt")
    
    # Feld für die Gruppe oder Art der Notiz
    kategorie_neu = st.text_input("Kategorie")
    
    # Feld für Suchwörter, getrennt durch Komma
    tags_neu = st.text_input("Tags (Beispiel: wichtig, privat)")
    
    # Der Knopf zum Absenden der Daten
    knopf = st.form_submit_button("Notiz speichern")

# Was passiert, wenn man auf den Knopf drückt:
if knopf:
    if titel_neu and inhalt_neu:
        # Den Text bei den Kommas trennen und Leerzeichen entfernen
        tag_liste = [t.strip() for t in tags_neu.split(",") if t.strip()]
        
        # Alle Daten in ein Paket packen
        daten = {
            "title": titel_neu,
            "content": inhalt_neu,
            "category": kategorie_neu,
            "tags": tag_liste
        }
        
        # Die Daten an deine API schicken
        ergebnis = requests.post(f"{API_URL}/notes", json=daten)
        
        # Prüfen, ob das Speichern geklappt hat (Code 201)
        if ergebnis.status_code == 201:
            st.success("Die Notiz wurde gespeichert.")
            st.rerun() # Die Seite neu laden, um die Liste zu aktualisieren
        else:
            st.error("Fehler: Die Daten konnten nicht gespeichert werden.")

            st.header("Vorhandene Notizen")

# Holt alle Notizen von deiner API
antwort = requests.get(f"{API_URL}/notes")

if antwort.status_code == 200:
    notizen = antwort.json()
    
    if notizen:
        # Erstellt eine Liste mit allen Titeln
        titel_liste = [n["title"] for n in notizen]
        
        # Zeigt ein Auswahlfeld mit den Titeln an
        auswahl = st.selectbox("Notiz zum Ansehen wählen:", titel_liste)

        # Sucht die gewählte Notiz und zeigt die Details
        for n in notizen:
            if n["title"] == auswahl:
                st.write(f"Inhalt: {n['content']}")
                st.write(f"Kategorie: {n['category']}")
                st.write(f"Tags: {', '.join(n['tags'])}")
    else:
        st.write("Es sind noch keine Notizen da.")
else:
    st.error("Daten konnten nicht geladen werden.")