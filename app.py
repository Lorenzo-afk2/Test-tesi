import streamlit as st
import pandas as pd

st.set_page_config(layout="wide", page_title="Portale HAVI")

# ==========================================
# 1. LA SIDEBAR (Filtri Globali)
# ==========================================
# La sidebar è visibile SEMPRE, indipendentemente dalla tab in cui ci troviamo.
st.sidebar.title("⚙️ Impostazioni Globali")
st.sidebar.write("Seleziona il contesto di lavoro:")

# Questi filtri influenzeranno i dati mostrati in tutte le schede
ristorante = st.sidebar.selectbox("Seleziona Ristorante:", ["Milano Duomo", "Roma Termini", "Napoli Centrale"])
reparto = st.sidebar.radio("Reparto di analisi:", ["Cella Negativa (Surgelati)", "Cella Positiva (Fresco)", "Magazzino Secco"])

st.sidebar.divider()
st.sidebar.success(f"Sistema connesso al server HAVI.\nUtente attivo su: {ristorante}")

# ==========================================
# IL CORPO PRINCIPALE
# ==========================================
st.title(f"🍔 Gestione Logistica - {ristorante}")
st.write(f"Stai visualizzando i dati per il reparto: **{reparto}**")

# ==========================================
# 2. LE TABS (Schede di Navigazione)
# ==========================================
# Creiamo 3 schede per dividere il lavoro.
tab_panoramica, tab_calcolo, tab_storico = st.tabs([
    "📊 Panoramica Scorte", 
    "🧮 Calcolatore EOQ", 
    "📂 Storico Consegne"
])

# --- CONTENUTO SCHEDA 1: PANORAMICA ---
with tab_panoramica:
    st.subheader("Situazione attuale in tempo reale")
    st.write("Qui il manager vede a colpo d'occhio se ci sono emergenze.")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Hamburger di Manzo", "45 colli", "-12 (sotto scorta minima)", delta_color="inverse")
    col2.metric("Patatine Fritte", "120 colli", "+30")
    col3.metric("Olio per frittura", "15 fusti", "Stabile", delta_color="off")

# --- CONTENUTO SCHEDA 2: CALCOLATORE EOQ ---
with tab_calcolo:
    st.subheader("Simulazione Nuovo Ordine (Modello EOQ)")
    st.write("Usa questo strumento per calcolare la quantità ottimale da ordinare.")
    
    # Mettiamo gli input specifici solo in questa scheda
    col_input1, col_input2 = st.columns(2)
    with col_input1:
        domanda_annua = st.number_input("Domanda annua prevista (D):", value=10000, step=100)
        costo_ordine = st.number_input("Costo per singolo ordine (S):", value=50.0)
    
    with col_input2:
        costo_mantenimento = st.number_input("Costo mantenimento unitario (H):", value=2.5)
        
    if st.button("Calcola Lotto Ottimale", type="primary"):
        st.success("Calcolo eseguito con successo! (Qui andrà inserita la formula matematica)")

# --- CONTENUTO SCHEDA 3: STORICO ---
with tab_storico:
    st.subheader("Ultime consegne da HAVI Logistics")
    
    # Creiamo una tabella finta per l'esempio
    dati_storici = pd.DataFrame({
        "Data Ordine": ["25-Set-2026", "22-Set-2026", "18-Set-2026"],
        "Prodotto": ["Hamburger di Manzo", "Patatine Fritte", "Salse miste"],
        "Quantità (Colli)": [150, 300, 50],
        "Stato": ["Consegnato", "Consegnato", "Consegnato"]
    })
    
    st.dataframe(dati_storici, use_container_width=True)


# (Codice precedente: st.set_page_config e inizializzazione session_state)

if not st.session_state["autenticato"]:
    
    # 1. INIEZIONE DELLO SFONDO DINAMICO (CSS)
    # Creiamo un gradiente che sfuma tra grigio scuro, nero e il rosso McDonald's
    sfondo_dinamico = """
    <style>
    .stApp {
        background: linear-gradient(-45deg, #1a1a1a, #2c3e50, #8b0000, #DA291C);
        background-size: 400% 400%;
        animation: movimento_sfondo 15s ease infinite;
    }
    
    @keyframes movimento_sfondo {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Rende la Card di login leggermente trasparente per un effetto "Vetro" (Glassmorphism) */
    [data-testid="stVerticalBlock"] > div > div {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 20px;
    }
    </style>
    """
    st.markdown(sfondo_dinamico, unsafe_allow_html=True)
    
    # 2. IL TUO MODULO DI LOGIN
    spazio_sx, col_centro, spazio_dx = st.columns([1, 2, 1])
    with col_centro:
        with st.container(border=True):
            st.markdown("<h2 style='text-align: center; color: #DA291C;'>Area Riservata HAVI</h2>", unsafe_allow_html=True)
            # ... resto del form di login (text_input, button, ecc.) ...

