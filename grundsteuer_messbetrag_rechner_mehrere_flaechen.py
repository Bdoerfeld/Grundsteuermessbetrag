import streamlit as st

# FDP-Logo einbinden
logo_url = "https://www.fdp-mv.de/sites/default/files/2020-10/MV-Logo.png"
st.markdown(
    f"""
    <div style="display: flex; justify-content: flex-end; align-items: center;">
        <img src="{logo_url}" width="120" style="margin-top: 10px; margin-right: 10px;">
    </div>
    """,
    unsafe_allow_html=True
)

# Titel und Einleitung
st.title("Grundsteuermessbetragsrechner - Grundsteuerreform ab 2025")
st.write("""
Ab 2025 wird die Grundsteuer in Deutschland nach neuen Berechnungsregeln erhoben. 
Mit diesem Rechner können Sie den neuen Grundsteuermessbetrag für verschiedene Flächenarten auf Ihrem Grundstück berechnen.
Bitte beachten Sie, dass diese Berechnung nur für die Ermittlung des Grundsteuermessbetrags für Grundstücke in Mecklenburg-Vorpommern geeignet ist.

Sie benötigen die Fläche und den Bodenrichtwert für jede Art von Fläche:

- **Wohngrundstücke**: 0,31 Promille Steuermesszahl
- **Unbebaute Grundstücke**: 0,34 Promille Steuermesszahl

Bitte wenden Sie sich bei Fragen an [kontakt@fdp-wismar.de](mailto:kontakt@fdp-wismar.de).
""")

# Initialisierung der Variablen für den gesamten Grundsteuerwert und Grundsteuermessbetrag
gesamt_grundsteuerwert = 0
gesamt_grundsteuermessbetrag = 0

# Anzahl der Flächenarten, die hinzugefügt werden sollen
st.subheader("Flächen auf dem Grundstück hinzufügen")
anzahl_flaechen = st.number_input("Anzahl der verschiedenen Flächenarten auf dem Grundstück", min_value=1, step=1)

# Schleife zur Eingabe der Daten für jede Flächenart
for i in range(int(anzahl_flaechen)):
    st.markdown(f"#### Fläche {i + 1}")
    flaechenart = st.selectbox(f"Art der Fläche {i + 1}", ["Wohngrundstück", "Unbebautes Grundstück"], key=f"flaechenart_{i}")
    flaeche = st.number_input(f"Fläche {i + 1} (m²)", min_value=0.0, step=1.0, key=f"flaeche_{i}")
    bodenrichtwert = st.number_input(f"Bodenrichtwert {i + 1} (Euro/m²)", min_value=0.0, step=1.0, key=f"bodenrichtwert_{i}")

    # Steuermesszahl je nach Flächenart festlegen
    if flaechenart == "Wohngrundstück":
        steuermesszahl = 0.31 / 1000  # 0,31 Promille für Wohngrundstücke
    else:
        steuermesszahl = 0.34 / 1000  # 0,34 Promille für unbebaute Grundstücke

    # Berechnung des Grundsteuerwerts und des Grundsteuermessbetrags für die aktuelle Fläche
    grundsteuerwert = flaeche * bodenrichtwert
    grundsteuermessbetrag = grundsteuerwert * steuermesszahl

    # Hinzufügen zum Gesamtwert
    gesamt_grundsteuerwert += grundsteuerwert
    gesamt_grundsteuermessbetrag += grundsteuermessbetrag

    # Anzeige der Ergebnisse für die aktuelle Fläche
    st.write(f"Grundsteuerwert für Fläche {i + 1}: {grundsteuerwert:.2f} Euro")
    st.write(f"Grundsteuermessbetrag für Fläche {i + 1}: {grundsteuermessbetrag:.2f} Euro")

# Gesamtergebnisse anzeigen
st.subheader("Gesamtergebnisse")
st.write(f"Gesamter Grundsteuerwert für das Grundstück: {gesamt_grundsteuerwert:.2f} Euro")
st.write(f"Neuer Grundsteuermessbetrag für das gesamte Grundstück: {gesamt_grundsteuermessbetrag:.2f} Euro")

# Erklärung der Berechnungsschritte
st.subheader("Erklärung der Berechnungsschritte")
st.write("""
1. **Grundsteuerwert je Fläche berechnen**: Die Fläche wird mit dem Bodenrichtwert multipliziert, um den Grundsteuerwert für jede Flächenart zu erhalten.
2. **Grundsteuermessbetrag je Fläche berechnen**: Der Grundsteuerwert wird mit der jeweiligen Steuermesszahl multipliziert, die je nach Flächenart unterschiedlich ist.
3. **Gesamtergebnis**: Die Grundsteuerwerte und Grundsteuermessbeträge aller Flächenarten werden addiert, um den Gesamtbetrag zu erhalten.
""")
