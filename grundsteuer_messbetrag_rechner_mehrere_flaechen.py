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
st.title("Erweiterter Grundsteuermessbetragsrechner - Grundsteuerreform ab 2025")
st.write("""
Dieser Rechner unterstützt die Berechnung des neuen Grundsteuermessbetrags unter Berücksichtigung der fiktiven Nettokaltmiete, des Bodenrichtwerts und zusätzlicher Flächenarten.
Die Berechnung erfolgt nach dem Ertragswertverfahren für Ein- und Zweifamilienhäuser gemäß der Anlage 39 des Bewertungsgesetzes.
""")

# Infobox zu den verschiedenen Flächenarten und dem Bewertungsverfahren
st.subheader("Informationen zur Berechnung")
st.info("""
### Wohnflächenberechnung und Bewertungsverfahren
Für die Berechnung des Grundsteuerwerts wird eine fiktive Nettokaltmiete herangezogen, die nach Gebäudeart und Baujahr variiert. 
Die Werte sind gemäß der Anlage 39 des Bewertungsgesetzes festgelegt.

#### Definitionen:
- **Wohnfläche**: Beinhaltet alle Räume, die zu Wohnzwecken genutzt werden. Dazu gehören Wohnzimmer, Schlafzimmer, Küchen, Bäder und Flure.
- **Garagen und sonstige Flächen**: Weitere Flächenarten wie Garagen und unbebaute Flächen können separat hinzugefügt und bewertet werden.
""")

# Art des Gebäudes und Baujahr auswählen
haustyp = st.selectbox("Wählen Sie den Haustyp", ["Einfamilienhaus", "Zweifamilienhaus"])
baujahr = st.selectbox("Wählen Sie das Baujahr des Gebäudes", ["vor 1948", "1949–1978", "1979–1999", "2000 oder später"])

# Fiktive Nettokaltmiete basierend auf Haustyp und Baujahr
if haustyp == "Einfamilienhaus":
    if baujahr == "vor 1948":
        fiktive_miete = 5.5  # €/m² (Beispielwert)
    elif baujahr == "1949–1978":
        fiktive_miete = 7.2
    elif baujahr == "1979–1999":
        fiktive_miete = 9.0
    else:
        fiktive_miete = 11.96
else:  # Zweifamilienhaus
    if baujahr == "vor 1948":
        fiktive_miete = 4.5
    elif baujahr == "1949–1978":
        fiktive_miete = 6.0
    elif baujahr == "1979–1999":
        fiktive_miete = 8.0
    else:
        fiktive_miete = 10.5

st.write(f"Fiktive Nettokaltmiete für {haustyp} mit Baujahr {baujahr}: {fiktive_miete} €/m²")

# Eingabe der Wohnfläche zur Berechnung des Jahresrohertrags für die Wohnfläche
wohnflaeche = st.number_input("Wohnfläche (m²)", min_value=0.0, step=1.0)
jahresrohertrag_wohn = wohnflaeche * fiktive_miete * 12
st.write(f"Berechneter Jahresrohertrag der Wohnfläche: {jahresrohertrag_wohn:.2f} Euro")

# Zusätzliche Flächenarten hinzufügen
st.subheader("Zusätzliche Flächenarten hinzufügen")
anzahl_flaechen = st.number_input("Anzahl der verschiedenen zusätzlichen Flächenarten auf dem Grundstück", min_value=1, step=1)

# Gesamtertrag und -fläche initialisieren
gesamt_jahresrohertrag = jahresrohertrag_wohn
gesamt_grundflaeche = wohnflaeche

for i in range(int(anzahl_flaechen)):
    st.markdown(f"#### Fläche {i + 1}")
    flaechenart = st.selectbox(f"Art der Fläche {i + 1}", ["Garagenfläche", "Unbebaute Fläche", "Sonstige Fläche"], key=f"flaechenart_{i}")
    flaeche = st.number_input(f"Fläche {i + 1} (m²)", min_value=0.0, step=1.0, key=f"flaeche_{i}")
    if flaechenart == "Garagenfläche":
        ertragswert = 2.5  # Beispielwert €/m² für Garagenfläche
    elif flaechenart == "Unbebaute Fläche":
        ertragswert = 1.0  # Beispielwert €/m² für unbebaute Fläche
    else:
        ertragswert = 1.5  # Beispielwert €/m² für sonstige Flächen
    
    # Berechnung des Rohertrags für die aktuelle Fläche
    jahresrohertrag_flaeche = flaeche * ertragswert * 12
    gesamt_jahresrohertrag += jahresrohertrag_flaeche
    gesamt_grundflaeche += flaeche
    
    # Ausgabe des Rohertrags für die aktuelle Fläche
    st.write(f"Jahresrohertrag für {flaechenart} ({flaeche:.2f} m²): {jahresrohertrag_flaeche:.2f} Euro")

# Button zur Bodenrichtwertseite
st.markdown(
    f"""
    <a href="https://www.geoport-nwm.de/de/bodenrichtwertkarte-bauland-nwm.html" target="_blank">
    <button style="background-color: #4CAF50; color: white; padding: 10px; border: none; border-radius: 5px; cursor: pointer;">
    Hier können Sie den Bodenrichtwert für Ihr Grundstück ermitteln (nur für den Kreis Nordwestmecklenburg)
    </button></a>
    """,
    unsafe_allow_html=True
)

# Eingabe des Bodenrichtwerts und Grundstücksfläche
bodenrichtwert = st.number_input("Bodenrichtwert (Euro/m²) nach Ermittlung auf der verlinkten Seite", min_value=0.0, step=1.0)
bodenwert = gesamt_grundflaeche * bodenrichtwert

# Berechnung des Grundsteuerwerts
st.subheader("Berechnung des Grundsteuerwerts")
grundsteuerwert = gesamt_jahresrohertrag + bodenwert
st.write(f"Grundsteuerwert des gesamten Grundstücks: {grundsteuerwert:.2f} Euro")

# Berechnung des Grundsteuermessbetrags
st.subheader("Berechnung des Grundsteuermessbetrags")
grundsteuermessbetrag = grundsteuerwert * 0.0034  # Beispielsteuermesssatz
st.write(f"Neuer Grundsteuermessbetrag für das gesamte Grundstück: {grundsteuermessbetrag:.2f} Euro")

# Hinweise zur Orientierung und Berechnung
st.subheader("Hinweise zur Orientierung und Berechnung")
st.write("""
Die Berechnungen basieren auf pauschalen Werten für die fiktive Nettokaltmiete je Quadratmeter Wohnfläche und den Bodenrichtwert, die laut Anlage 39 des Bewertungsgesetzes festgelegt sind.
- **Fiktive Nettokaltmiete**: Entsprechend den Regelungen in Anlage 39 wird eine standardisierte Miete für die Berechnung der Grundsteuer herangezogen, unabhängig von der tatsächlichen Vermietungssituation.
- **Bodenwert**: Der Bodenrichtwert muss über das Geoportal des Kreises Nordwestmecklenburg ermittelt und hier eingegeben werden.

**Hinweis zur Orientierung**: Diese Berechnung dient nur der Schätzung und stellt keine Garantie auf Richtigkeit dar. Bei Unsicherheiten empfehlen wir, die Bauunterlagen zu prüfen oder sich an einen Fachmann zu wenden.
""")
