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
Dieser Rechner unterstützt die Berechnung des neuen Grundsteuermessbetrags unter Berücksichtigung der fiktiven Miete und der Bewertung des Einheitswerts.
Die Berechnung erfolgt je nach Immobilienart im Ertragswertverfahren oder Sachwertverfahren.

Bitte wählen Sie die Art Ihrer Immobilie und ob es sich um ein Ein- oder Zweifamilienhaus handelt, um das passende Verfahren anzuwenden.
""")

# Art der Immobilie und Haustyp auswählen
immobilien_art = st.selectbox("Wählen Sie die Art Ihrer Immobilie", ["Wohngebäude (eigengenutzt)", "Miet- oder Gewerbeimmobilie"])
haustyp = st.selectbox("Wählen Sie den Haustyp", ["Einfamilienhaus", "Zweifamilienhaus"])

# Fiktive Miete basierend auf Haustyp
if haustyp == "Einfamilienhaus":
    fiktive_miete = 8  # Beispielwert €/m², spezifisch je nach Region
else:
    fiktive_miete = 6  # Beispielwert €/m² für Zweifamilienhäuser

st.write(f"Fiktive Miete für {haustyp}: {fiktive_miete} €/m²")

# Bewertungsverfahren basierend auf der Immobilienart
if immobilien_art == "Miet- oder Gewerbeimmobilie":
    st.subheader("Berechnung nach dem Ertragswertverfahren")
    wohnflaeche = st.number_input("Wohnfläche (m²)", min_value=0.0, step=1.0)
    jahresfiktivemiete = wohnflaeche * fiktive_miete * 12
    st.write(f"Berechnete Jahresfiktivemiete: {jahresfiktivemiete:.2f} Euro")

    bewirtschaftungskosten = st.number_input("Bewirtschaftungskosten (Euro)", min_value=0.0, step=1.0,
                                             help="Laufende Kosten für Betrieb und Instandhaltung.")
    liegenschaftszinssatz = st.number_input("Liegenschaftszinssatz (%)", min_value=0.0, max_value=10.0, step=0.1,
                                            help="Regionstypische Verzinsung, meist zwischen 3-5%.")

    # Ertragswertberechnung
    reinertrag = jahresfiktivemiete - bewirtschaftungskosten
    kapitalwert = reinertrag / (liegenschaftszinssatz / 100)
    st.write(f"Kapitalwert der Immobilie: {kapitalwert:.2f} Euro")
else:
    st.subheader("Berechnung nach dem Sachwertverfahren")
    
    # Auswahl des Baujahrs zur Anwendung allgemeiner Baukosten und Wertminderungssätze
    baujahr = st.selectbox("Baujahr des Gebäudes", ["vor 1948", "1949–1978", "1979–1999", "2000 oder später"])
    
    # Standardisierte Herstellungskosten und Wertminderung basierend auf Baujahr
    if baujahr == "vor 1948":
        herstellungskosten = 1000  # €/m²
        wertminderung = 0.7
    elif baujahr == "1949–1978":
        herstellungskosten = 1250  # €/m²
        wertminderung = 0.5
    elif baujahr == "1979–1999":
        herstellungskosten = 1500  # €/m²
        wertminderung = 0.3
    else:
        herstellungskosten = 1750  # €/m²
        wertminderung = 0.2

    # Eingabe der Grundstücks- und Wohnfläche
    wohnflaeche = st.number_input("Wohnfläche (m²)", min_value=0.0, step=1.0)
    grundstuecksflaeche = st.number_input("Grundstücksfläche (m²)", min_value=0.0, step=1.0)

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

    # Eingabe des Bodenrichtwerts nach Abruf über das Geoportal
    bodenrichtwert = st.number_input("Bodenrichtwert (Euro/m²) nach Ermittlung auf der verlinkten Seite", min_value=0.0, step=1.0)
    bodenwert = grundstuecksflaeche * bodenrichtwert

    # Sachwertberechnung
    gebaeudewert = wohnflaeche * herstellungskosten * (1 - wertminderung)
    sachwert = gebaeudewert + bodenwert
    st.write(f"Sachwert der Immobilie: {sachwert:.2f} Euro")

# Berechnung des Grundsteuermessbetrags
st.subheader("Berechnung des Grundsteuermessbetrags")
if immobilien_art == "Miet- oder Gewerbeimmobilie":
    grundsteuermessbetrag = kapitalwert * 0.0031  # Beispielsteuermesssatz
else:
    grundsteuermessbetrag = sachwert * 0.0034  # Beispielsteuermesssatz

st.write(f"Neuer Grundsteuermessbetrag für das gesamte Grundstück: {grundsteuermessbetrag:.2f} Euro")

# Hinweise zur Orientierung und Berechnung
st.subheader("Hinweise zur Orientierung und Berechnung")
st.write("""
Die Berechnungen basieren auf pauschalen Werten für Herstellungskosten und Wertminderung, die allgemein für verschiedene Baujahre gelten:
- **Fiktive Miete**: Für die Grundsteuerberechnung wird eine fiktive Miete verwendet, die nicht auf tatsächlichen Mieteinnahmen beruht. Diese beträgt typischerweise 8 €/m² für Einfamilienhäuser und 6 €/m² für Zweifamilienhäuser.
- **Herstellungskosten** und **Wertminderung**: Berücksichtigen das Baujahr und den typischen Zustand des Gebäudes.
- **Bodenwert**: Der Bodenrichtwert muss über das Geoportal des Kreises Nordwestmecklenburg ermittelt und hier eingegeben werden.

**Hinweis zur Orientierung**: Diese Berechnung dient nur der Schätzung und stellt keine Garantie auf Richtigkeit dar. Bei Unsicherheiten empfehlen wir, die Bauunterlagen zu prüfen oder sich an einen Fachmann zu wenden.
""")
