import streamlit as st

# 1. IMPOSTAZIONE STRUTTURALE OBLIGATORIA
st.set_page_config(page_title="HAVIConnect", layout="wide")

# 2. INIEZIONE CSS PER REPLICARE L'ESTETICA DELL'IMMAGINE
css_havi = """
<style>
/* Imposta lo sfondo scuro generale (simile al tema dell'immagine) */
.stApp {
    background-color: #0a111a;
    background-image: radial-gradient(circle at 50% 30%, #15263b 0%, #0a111a 70%);
    color: white;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Nasconde l'header e il menu standard di Streamlit */
header {visibility: hidden;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Stile della barra superiore (Top Bar) */
.top-bar {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    display: flex;
    justify-content: space-between;
    padding: 15px 30px;
    font-size: 12px;
    color: #7b8898;
    z-index: 999;
}

/* Stile della casella di testo (Input) */
div[data-baseweb="input"] {
    background-color: white !important;
    border-radius: 30px !important;
    border: none !important;
    padding: 2px 10px !important;
}
input[class*="st-"] {
    color: #333333 !important;
    font-size: 11px !important;
    font-weight: bold !important;
}
/* Nasconde l'etichetta dell'input nativa di Streamlit */
.stTextInput label {
    display: none;
}

/* Stile del bottone verde HAVI */
.stButton > button {
    background-color: #76c04f !important; /* Verde chiaro dell'immagine */
    color: white !important;
    border-radius: 30px !important;
    border: none !important;
    padding: 12px 24px !important;
    font-weight: bold !important;
    font-size: 13px !important;
    width: 100%;
    margin-top: -10px;
    transition: background-color 0.3s;
}
.stButton > button:hover {
    background-color: #5da03b !important;
}

/* Stile dei link di supporto sotto il bottone */
.support-links {
    text-align: center;
    margin-top: 20px;
    font-size: 12px;
}
.support-links p {
    color: #7b8898;
    margin-bottom: 5px;
}
.support-links a {
    color: white;
    text-decoration: none;
}
.support-links a:hover {
    text-decoration: underline;
}

/* Sezione delle 3 icone inferiori */
.features-container {
    display: flex;
    justify-content: center;
    gap: 60px;
    margin-top: 50px;
    text-align: center;
    font-size: 11px;
    color: #b0bec5;
}
.feature-icon {
    font-size: 24px;
    margin-bottom: 8px;
    color: #4285f4;
}

/* Footer a fondo pagina */
.bottom-footer {
    position: fixed;
    bottom: 10px;
    width: 100%;
    text-align: center;
    font-size: 10px;
    color: #54667a;
}
</style>
"""
st.markdown(css_havi, unsafe_allow_html=True)

# 3. TOP BAR (Lingua e Testo in alto)
st.markdown("""
<div class="top-bar">
    <div>Ora sei su haviconnect.com</div>
    <div style="display: flex; align-items: center; gap: 5px;">
        Lingua / Paese <img src="https://flagcdn.com/w20/it.png" width="16" style="border-radius:50%;">
    </div>
</div>
""", unsafe_allow_html=True)

# Spaziatura verticale per centrare il contenuto
st.write("\n" * 4)

# 4. LAYOUT CENTRALE
# Usiamo 3 colonne per stringere il form di login al centro (come nell'immagine)
spazio_sx, col_centro, spazio_dx = st.columns([1, 1.2, 1])

with col_centro:
    
    # LOGO E TITOLO HAVIConnect
    # Il logo è simulato tramite SVG inline per replicare i quadratini sfalsati blu e verdi
    logo_html = """
    <div style="text-align: center; margin-bottom: 20px;">
        <svg width="60" height="60" viewBox="0 0 60 60">
            <!-- Quadrato Blu Superiore -->
            <rect x="15" y="10" width="15" height="15" fill="#3b6998" transform="skewY(-15)"/>
            <!-- Quadrato Verde -->
            <rect x="32" y="14.5" width="15" height="15" fill="#76c04f" transform="skewY(-15)"/>
            <!-- Quadrato Blu Inferiore -->
            <rect x="15" y="27" width="15" height="15" fill="#3b6998" transform="skewY(-15)"/>
        </svg>
        <h1 style="color: white; font-size: 32px; font-weight: bold; margin-top: -10px; margin-bottom: 5px;">HAVIConnect</h1>
        <p style="color: white; font-size: 14px;">Entra con il tuo account Havi Connect</p>
    </div>
    """
    st.markdown(logo_html, unsafe_allow_html=True)
    
    # CAMPO DI INPUT (ID Utente)
    # label_visibility="collapsed" serve a togliere l'etichetta testuale standard di Streamlit
    utente_id = st.text_input(
        "ID", 
        placeholder="PER FAVORE ENTRA CON IL TUO UTENTE ID CONNECT NON LA TUA MAIL", 
        label_visibility="collapsed"
    )
    
    # BOTTONE VERDE
    if st.button("CONTINUA CON IL TUO ACCOUNT CONNECT!"):
        if utente_id:
            st.success(f"Tentativo di accesso per: {utente_id}")
        else:
            st.error("Inserisci un ID valido.")
            
    # LINK DI SUPPORTO
    supporto_html = """
    <div class="support-links">
        <p>Problemi con il login?</p>
        <a href="#">Svuota la cache</a> &nbsp;|&nbsp; <a href="#">Contattaci</a>
    </div>
    """
    st.markdown(supporto_html, unsafe_allow_html=True)

# 5. ICONE INFERIORI (Comodità, Collaborazione, Sicurezza)
icone_html = """
<div class="features-container">
    <div>
        <div class="feature-icon">🛡️</div>
        Comodità
    </div>
    <div>
        <div class="feature-icon">💬</div>
        Collaborazione
    </div>
    <div>
        <div class="feature-icon">🔒</div>
        Sicurezza
    </div>
</div>
<div style="text-align: center; margin-top: 15px; font-size: 12px;">
    <a href="#" style="color: white; text-decoration: none;">Scopri di più...</a>
</div>
"""
st.markdown(icone_html, unsafe_allow_html=True)

# 6. FOOTER COPYRIGHT
st.markdown("""
<div class="bottom-footer">
    © Copyright - HAVI | All rights reserved | Dichiarazione della Privacy
</div>
""", unsafe_allow_html=True)

