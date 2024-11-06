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
Dieser Rechner unterstützt die Berechnung des neuen Grundsteuermessbetrags unter Berücksichtigung der Verfahren zur Bewertung des Einheitswerts.
**Hinweis**: Diese Berechnung ist nur für Grundstücke in Mecklenburg-Vorpommern geeignet.
Die Berechnung erfolgt je nach Immobilienart im Ertragswertverfahren oder Sachwertverfahren.

Benötigte Informationen:
- **Art der Immobilie**: Auswahl des Bewertungsverfahrens (Ertragswert- oder Sachwertverfahren).
- **Wohnfläche, Garagenfläche und andere Flächenarten**: Geben Sie die Flächen für jede Art von Fläche an.
- **Bodenrichtwert**: Sie können den Bodenrichtwert für Ihr Grundstück ermitteln, indem Sie auf den Button unten klicken (nur gültig für den Kreis Nordwestmecklenburg).
""")

# Art der Immobilie auswählen
immobilien_art = st.selectbox("Wählen Sie die Art Ihrer Immobilie", ["Wohngebäude (eigengenutzt)", "Miet- oder Gewerbeimmobilie"])

# Bewertungsverfahren basierend auf der Immobilienart
if immobilien_art == "Miet- oder Gewerbeimmobilie":
    st.subheader("Berechnung nach dem Ertragswertverfahren")
    jahresrohertrag = st.number_input("Jahresrohertrag (Euro)", min_value=0.0, step=1.0)
    bewirtschaftungskosten = st.number_input("Bewirtschaftungskosten (Euro)", min_value=0.0, step=1.0)
    liegenschaftszinssatz = st.number_input("Liegenschaftszinssatz (%)", min_value=0.0, max_value=100.0, step=0.1)
    
    # Ertragswertberechnung
    reinertrag = jahresrohertrag - bewirtschaftungskosten
    kapitalwert = reinertrag / (liegenschaftszinssatz / 100)
    st.write(f"Kapitalwert der Immobilie: {kapitalwert:.2f} Euro")
else:
    st.subheader("Berechnung nach dem Sachwertverfahren")
    herstellungskosten = st.number_input("Herstellungskosten des Gebäudes (Euro)", min_value=0.0, step=1.0)
    wertminderung = st.number_input("Wertminderung des Gebäudes (in Prozent)", min_value=0.0, max_value=100.0, step=0.1)
    bodenwert = st.number_input("Bodenwert des Grundstücks (Euro)", min_value=0.0, step=1.0)

    # Sachwertberechnung
    gebaeudewert = herstellungskosten * (1 - wertminderung / 100)
    sachwert = gebaeudewert + bodenwert
    st.write(f"Sachwert der Immobilie: {sachwert:.2f} Euro")

# Berechnung des Grundsteuermessbetrags
st.subheader("Berechnung des Grundsteuermessbetrags")
if immobilien_art == "Miet- oder Gewerbeimmobilie":
    grundsteuermessbetrag = kapitalwert * 0.0031  # Beispiel für den Steuermesssatz, je nach Region variabel
else:
    grundsteuermessbetrag = sachwert * 0.0034  # Beispiel für den Steuermesssatz, je nach Region variabel

st.write(f"Neuer Grundsteuermessbetrag für das gesamte Grundstück: {grundsteuermessbetrag:.2f} Euro")

# Hinweis zur Orientierung
st.subheader("Hinweis zur Orientierung")
st.write("""
Die hier dargestellte Berechnung dient ausschließlich der Orientierung und stellt keine Garantie auf Richtigkeit dar. 
Für eine genaue Berechnung wird empfohlen, die Bauunterlagen zu konsultieren oder sich an einen Fachmann zu wenden.
""")
