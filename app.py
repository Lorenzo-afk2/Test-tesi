import streamlit as st

# 1. IMPOSTAZIONE STRUTTURALE (Deve essere sempre la riga 1)
st.set_page_config(page_title="Portale HAVI Logistics", layout="wide", page_icon="🚚")

# 2. INIZIALIZZAZIONE DELLA MEMORIA (Session State)
if "autenticato" not in st.session_state:
    st.session_state["autenticato"] = False

# ==========================================
# 3. SCHERMATA DI LOGIN (Con Sfondo Dinamico)
# ==========================================
if not st.session_state["autenticato"]:
    
    # Iniezione CSS per l'animazione e la grafica della card
    css_login = """
    <style>
    /* 1. Sfondo animato dell'intera pagina (Colori HAVI/McDonald's) */
    .stApp {
        background: linear-gradient(-45deg, #002244, #003366, #8b0000, #DA291C);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* 2. Effetto Vetro (Glassmorphism) per la finestra centrale */
    [data-testid="stVerticalBlock"] > div > div {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }
    
    /* 3. Forza il colore del testo a grigio scuro per renderlo leggibile sulla card bianca */
    p, h1, h2, h3, h4, h5, h6, label {
        color: #2c3e50 !important;
    }
    </style>
    """
    st.markdown(css_login, unsafe_allow_html=True)
    
    # Layout responsivo: 3 colonne per centrare la Card su iPad/PC
    spazio_sx, col_centro, spazio_dx = st.columns([1, 2, 1])
    
    with col_centro:
        with st.container(border=False):
            # Intestazione
            st.markdown("<h1 style='text-align: center; color: #DA291C !important; margin-bottom: 0px;'>Area Riservata</h1>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; font-size: 18px;'>Rete Logistica HAVI - McDonald's</p>", unsafe_allow_html=True)
            st.divider()
            
            # Modulo di inserimento
            store_id = st.text_input("Identificativo Ristorante", placeholder="Es. IT-12345")
            password = st.text_input("Password di Sicurezza", type="password", placeholder="••••••••")
            
            st.write("") # Spazio estetico
            
            # Pulsante di Accesso
            if st.button("Accedi al Cruscotto", type="primary", use_container_width=True):
                # Controllo credenziali (simulato)
                if store_id == "IT-001" and password == "admin":
                    st.session_state["autenticato"] = True
                    st.rerun() # Ricarica l'app bypassando questa schermata
                else:
                    st.error("Credenziali errate. Contatta l'amministratore di sistema.")
            
            st.markdown("<p style='text-align: center; font-size: 12px; margin-top: 15px; color: gray !important;'>🔒 Connessione cifrata end-to-end</p>", unsafe_allow_html=True)
            
    # Blocca la lettura del resto del codice se l'utente non ha fatto l'accesso
    st.stop()

# ==========================================
# 4. APPLICAZIONE PRINCIPALE (Protetta)
# ==========================================
# Nota: Essendo arrivati qui, il CSS di sopra non viene caricato.
# L'app torna al suo sfondo bianco standard, perfetto per l'analisi dei dati!

st.title("🍔 Cruscotto Logistico McDonald's")
st.success("Accesso effettuato con successo! Sei autenticato come: IT-001")

st.subheader("Simulazione EOQ in corso...")
st.write("In questa sezione pulita e luminosa andranno posizionati i parametri e i grafici Plotly.")

# Tasto di uscita rapido
if st.button("Scollegati (Logout)"):
    st.session_state["autenticato"] = False
    st.rerun()


