import streamlit as st

st.set_page_config(layout="wide") # Consente di usare tutto lo schermo, non solo il centro
st.title("🍔 Sistema di Gestione HAVI-McDonald's")

# ==========================================
# 1. st.sidebar (Il Menu Laterale)
# ==========================================
# Tutto ciò che ha la parola "sidebar" finirà nella colonna grigia a sinistra dello schermo
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/3/36/McDonald%27s_Golden_Arches.svg", width=100)
st.sidebar.title("Pannello di Controllo")
st.sidebar.write("Usa le opzioni qui sotto per impostare il calcolo.")

# Anche gli input possono stare nella sidebar!
categoria = st.sidebar.selectbox("Reparto:", ["Cella Negativa (Carne)", "Cella Positiva (Verdura)"])
giorni_copertura = st.sidebar.slider("Giorni copertura desiderati:", 1, 30, 7)

# ==========================================
# 2. st.tabs (Le Schede di Navigazione)
# ==========================================
# Crea dei bottoni in alto in stile "browser" per passare da una pagina all'altra
tab1, tab2, tab3 = st.tabs(["📝 Inserimento Dati", "📊 Analisi e Grafici", "⚙️ Impostazioni Tecniche"])

# --- CONTENUTO DELLA TAB 1 ---
with tab1:
    st.header("Caricamento Vendite Storiche")
    st.file_uploader("Carica Excel delle casse", type=["csv", "xlsx"])
    st.write("Le vendite del reparto **" + categoria + "** determineranno il lotto economico (EOQ).")
    
# --- CONTENUTO DELLA TAB 2 ---
with tab2:
    st.header("Risultati Ottimizzazione")
    
    # ==========================================
    # 3. st.columns (Affiancare gli elementi)
    # ==========================================
    # Creiamo due colonne per mostrare le metriche una accanto all'altra
    col_sinistra, col_destra = st.columns(2)
    
    # Per scrivere dentro la colonna, usiamo il suo nome al posto di "st."
    with col_sinistra:
        st.subheader("La situazione attuale")
        st.metric(label="Scorte in cella", value="45 colli", delta="-10 colli")
        st.write("Il livello è sceso sotto il punto di riordino di sicurezza.")
        
    with col_destra:
        st.subheader("L'azione richiesta")
        st.metric(label="Ordine da inviare (EOQ)", value="150 colli", delta="Ottimale", delta_color="normal")
        st.button("Invia Ordine a HAVI", type="primary") # type="primary" fa diventare il bottone colorato e in risalto

# --- CONTENUTO DELLA TAB 3 ---
with tab3:
    st.header("Parametri Algoritmo Avanzato")
    
    # ==========================================
    # 4. st.expander (Il menu a tendina nascosto)
    # ==========================================
    # Perfetto per nascondere impostazioni che servono raramente
    st.write("Questi parametri determinano il calcolo dell'EOQ e del Reorder Point.")
    
    # Tutto ciò che è dentro l'expander si vedrà solo se l'utente clicca sul titolo
    with st.expander("Mostra/Nascondi costi fissi e variabili"):
        st.write("Qui puoi modificare le costanti di sistema se cambiano le tariffe logistiche.")
        costo_ordine = st.number_input("Costo per singolo ordine emesso (S):", value=25.0)
        costo_mantenimento = st.number_input("Costo di mantenimento annuo (H):", value=4.5)
        
    with st.expander("Dettagli Matematici (Z-Score)"):
        st.write("Il calcolo della Scorta di Sicurezza usa la curva di Gauss.")
        st.selectbox("Livello di Servizio:", ["90% (Z=1.28)", "95% (Z=1.65)", "99% (Z=2.33)"])
