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
st.title("Berechnung Grundsteuermessbetrag - ab 2025")
st.write("""
Dieser Rechner unterstützt die Berechnung des neuen Grundsteuermessbetrags. 
**Hinweis**: Diese Berechnung ist nur für Grundstücke in Mecklenburg-Vorpommern geeignet.

Benötigte Informationen:
- **Wohnfläche, Garagenfläche und andere Flächenarten**: Geben Sie die Flächen für jede Art von Fläche an.
- **Bodenrichtwert**: Sie können den Bodenrichtwert für Ihr Grundstück ermitteln, indem Sie auf den Button unten klicken.
- **Steuermesszahlen**:
  - Wohngrundstücke: 0,31 Promille
  - Unbebaute Grundstücke: 0,34 Promille
  - Garagen können in einigen Fällen eigene Werte haben.

Falls Fragen bestehen, wenden Sie sich an [kontakt@fdp-wismar.de](mailto:kontakt@fdp-wismar.de).
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
    flaechenart = st.selectbox(f"Art der Fläche {i + 1}", ["Wohnfläche", "Garagenfläche", "Unbebaute Fläche", "Sonstige Fläche"], key=f"flaechenart_{i}")
    flaeche = st.number_input(f"Fläche {i + 1} (m²)", min_value=0.0, step=1.0, key=f"flaeche_{i}")
    
    # Link zur Bodenrichtwertseite
    st.markdown(
        f"""
        <a href="https://www.geoport-nwm.de/de/bodenrichtwertkarte-bauland-nwm.html" target="_blank">
        <button style="background-color: #4CAF50; color: white; padding: 10px; border: none; border-radius: 5px; cursor: pointer;">
        Hier können Sie den Bodenrichtwert für Ihr Grundstück ermitteln - nur NWM
        </button></a>
        """,
        unsafe_allow_html=True
    )

    bodenrichtwert = st.number_input(f"Bodenrichtwert {i + 1} (Euro/m²) nach Ermittlung auf der verlinkten Seite", min_value=0.0, step=1.0, key=f"bodenrichtwert_{i}")

    # Auswahl des Baujahrs/Renovierungsjahrs
    if flaechenart == "Wohnfläche":
        baujahr = st.selectbox(f"Baujahr oder letzte Renovierung für Fläche {i + 1}", ["Vor 1948", "1948 - 1978", "1979 oder später"], key=f"baujahr_{i}")
        if baujahr == "Vor 1948":
            zuschlag = 1.1  # Beispielsweise ein Zuschlag für ältere Gebäude
        elif baujahr == "1948 - 1978":
            zuschlag = 1.05
        else:
            zuschlag = 1.0  # Kein Zuschlag für neuere Gebäude
    else:
        zuschlag = 1.0

    # Steuermesszahl je nach Flächenart festlegen
    if flaechenart == "Wohnfläche":
        steuermesszahl = 0.31 / 1000 * zuschlag
    elif flaechenart == "Garagenfläche":
        steuermesszahl = 0.32 / 1000  # Beispiel für Garagenflächen
    else:
        steuermesszahl = 0.34 / 1000

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
2. **Grundsteuermessbetrag je Fläche berechnen**: Der Grundsteuerwert wird mit der jeweiligen Steuermesszahl multipliziert, die je nach Flächenart unterschiedlich ist. Zuschläge können für bestimmte Gebäudejahre oder Renovierungen gelten.
3. **Gesamtergebnis**: Die Grundsteuerwerte und Grundsteuermessbeträge aller Flächenarten werden addiert, um den Gesamtbetrag zu erhalten.
""")
