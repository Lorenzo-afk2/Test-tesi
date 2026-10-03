import streamlit as st
import pandas as pd
import numpy as np
import math
import os
import plotly.express as px

# =====================================================================
# 1. SETUP INIZIALE E COLLEGAMENTO CSS
# =====================================================================
st.set_page_config(page_title="HAVIConnect - Store", layout="wide", initial_sidebar_state="expanded")

if os.path.exists("style.css"):
    with open("style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# =====================================================================
# 2. SISTEMA DI AUTENTICAZIONE E MEMORIA (Carrello)
# =====================================================================
if 'autenticato' not in st.session_state:
    st.session_state['autenticato'] = False

if 'carrello' not in st.session_state:
    st.session_state['carrello'] = []

if 'mostra_carrello' not in st.session_state:
    st.session_state['mostra_carrello'] = False

def toggle_carrello():
    st.session_state['mostra_carrello'] = not st.session_state['mostra_carrello']


if not st.session_state['autenticato']:
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    with st.form("login_form"):
        col_left, col_right = st.columns([1.2, 2])
        
        with col_left:
            st.markdown("""
                <div class="login-left-panel">
                    <div class="login-brand-row">
                        <span class="login-brand-m">M</span>
                        <span class="login-brand-text">HAVI & McD</span>
                    </div>
                    <div class="login-desc">Portale Ottimizzazione Scorte & Riordino Lotti</div>
                </div>
            """, unsafe_allow_html=True)
            
        with col_right:
            st.markdown("""
                <div class="login-right-header">
                    <div class="login-title">Accesso Store Manager</div>
                </div>
            """, unsafe_allow_html=True)
            
            username = st.text_input("Codice Ristorante o ID Utente", value="")
            password = st.text_input("Chiave di Sicurezza (PIN / Password)", type="password", value="")
            
            submitted = st.form_submit_button("Accedi allo store")
            
        if submitted:
            if username == "IT-07100-SASSARI" and password == "RistoranteSS":
                st.session_state['autenticato'] = True
                st.rerun() 
            else:
                st.error("❌ Credenziali errate. Riprova.")
    
    st.stop() 


# =====================================================================
# 3. DATI IN MEMORIA E FUNZIONI
# =====================================================================
catalogo_prodotti = {
    "❄️ Congelato": ["Hamburger di Manzo 4:1", "Patatine Fritte (Scatole)", "McNuggets di Pollo"],
    "🥬 Fresco": ["Insalata Iceberg (Buste)", "Pomodori a Fette", "Latte Intero (Brik)"],
    "📦 Secco": ["Panini Regular (Casse)", "Bicchieri Carta (Manicotti)", "Salsa Ketchup (Scatole)"],
    "🧹 Operativo": ["Guanti in Nitrile (Box)", "Sgrassatore Superfici (Taniche)", "Rotoli Asciugatutto"]
}

prezzi_prodotti = {
    "Hamburger di Manzo 4:1": 45.00, "Patatine Fritte (Scatole)": 28.50, "McNuggets di Pollo": 55.00,
    "Insalata Iceberg (Buste)": 15.00, "Pomodori a Fette": 18.00, "Latte Intero (Brik)": 12.00,
    "Panini Regular (Casse)": 22.00, "Bicchieri Carta (Manicotti)": 35.00, "Salsa Ketchup (Scatole)": 20.00,
    "Guanti in Nitrile (Box)": 8.50, "Sgrassatore Superfici (Taniche)": 14.00, "Rotoli Asciugatutto": 19.00
}

@st.cache_data 
def genera_database_simulato(nome_prodotto):
    date_storiche = pd.date_range(start="2021-01-01", end="2023-12-31", freq="D")
    np.random.seed(len(nome_prodotto) * 42) 
    vendite = np.random.normal(loc=200, scale=30, size=len(date_storiche))
    df = pd.DataFrame({'Data': date_storiche, 'Domanda_Scatole': vendite})
    df['Giorno_Num'] = df['Data'].dt.dayofweek 
    df.loc[df['Giorno_Num'] >= 5, 'Domanda_Scatole'] *= 1.40 
    df['Domanda_Scatole'] = np.maximum(df['Domanda_Scatole'].round(), 0).astype(int)
    return df


# =====================================================================
# 4. SIDEBAR - MENU DI NAVIGAZIONE
# =====================================================================
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/McDonald%27s_Golden_Arches.svg/120px-McDonald%27s_Golden_Arches.svg.png", width=60)
st.sidebar.title("Menu Principale")

pagina_selezionata = st.sidebar.radio(
    "",
    ["🏠 Home Page", "📦 Compilazione Ordine", "📋 Inventario", "📄 File Consumazioni"]
)

st.sidebar.markdown("---")

if st.sidebar.button("🚪 Log out"):
    st.session_state['autenticato'] = False
    st.rerun()


# =====================================================================
# 5. ROUTING: PAGINA HOME
# =====================================================================
if pagina_selezionata == "🏠 Home Page":
    st.title("Dashboard Direzionale | IT-07100-SASSARI")
    
    st.markdown("#### Benvenuto nel sistema di gestione logistica. Seleziona un modulo dal menu laterale per iniziare.")
    
    st.markdown("---")
    st.subheader("Stato Operativo Ristorante")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""<div class="card-kpi-mini"><div class="kpi-titolo">Stato Rifornimenti</div><div class="kpi-valore kpi-valore-green">REGOLARE</div></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="card-kpi-mini card-kpi-mini-yellow"><div class="kpi-titolo">Prossima Consegna</div><div class="kpi-valore">DOMANI</div></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class="card-kpi-mini card-kpi-mini-green"><div class="kpi-titolo">Allarmi Scorte</div><div class="kpi-valore kpi-valore-green">0</div></div>""", unsafe_allow_html=True)
    with col4:
        st.markdown("""<div class="card-kpi-mini"><div class="kpi-titolo">Livello Servizio</div><div class="kpi-valore">98.5%</div></div>""", unsafe_allow_html=True)


# =====================================================================
# 6. ROUTING: COMPILAZIONE ORDINE E CARRELLO
# =====================================================================
elif pagina_selezionata == "📦 Compilazione Ordine":
    st.title("Compilazione Ordine")
    st.markdown("Seleziona il prodotto e i relativi parametri, poi aggiungilo alla distinta d'ordine.")

    # --- 1. PRIMA RIGA: REPARTO E PRODOTTO ---
    col_rep, col_prod = st.columns(2)
    with col_rep:
        reparto_scelto = st.selectbox("1. Seleziona il Reparto", list(catalogo_prodotti.keys()))
    with col_prod:
        prodotto_scelto = st.selectbox("2. Seleziona il Prodotto", catalogo_prodotti[reparto_scelto])

    prezzo_base = prezzi_prodotti[prodotto_scelto]

    # --- 2. SECONDA RIGA: LIVELLO SERVIZIO E COSTO MANTENIMENTO (Spostati qui) ---
    col_srv, col_mnt = st.columns(2)
    with col_srv:
        livello_servizio = st.selectbox("Livello di Servizio desiderato (%)", [90, 95, 99], index=1)
    with col_mnt:
        costo_mantenimento_default = round(prezzo_base * 0.15, 2)
        costo_mantenimento = st.number_input("Costo Mantenimento unitario (€)", value=costo_mantenimento_default, step=0.1)

    # --- 3. TERZA RIGA: PREZZO E QUANTITA' ---
    col_prz, col_qta = st.columns(2)
    with col_prz:
        prezzo_unitario = st.number_input("Prezzo Unitario Prodotto (€)", value=prezzo_base, step=1.0, disabled=True)
    with col_qta:
        quantita_ordine = st.number_input("Quantità manuale da ordinare (Scatole)", value=150, step=10)

    # --- 4. QUARTA RIGA: I DUE BOTTONI DI AZIONE ---
    st.markdown("<br>", unsafe_allow_html=True)
    col_add, col_view = st.columns(2)
    
    with col_add:
        # type="primary" applica il nuovo Blu Corporate elegante
        if st.button("AGGIUNGI ALL'ORDINE", type="primary"):
            st.session_state['carrello'].append({
                "Reparto": reparto_scelto,
                "Prodotto": prodotto_scelto,
                "Quantità": quantita_ordine,
                "Prezzo Unit.": f"{prezzo_unitario:.2f} €",
                "Totale": quantita_ordine * prezzo_unitario
            })
            st.session_state['mostra_carrello'] = True
            st.success(f"Dato acquisito. {quantita_ordine} scatole di '{prodotto_scelto}' in distinta.")
            
    with col_view:
        st.button("RIEPILOGO ORDINE", on_click=toggle_carrello)


    # --- RIEPILOGO ORDINE (VISIBILE SOLO SE ATTIVATO DAL BOTTONE) ---
    if st.session_state['mostra_carrello']:
        st.markdown("---")
        st.markdown("## Riepilogo Ordine in Corso")

        if len(st.session_state['carrello']) > 0:
            # Creazione della tabella con colonna esplicita per il Numero Riga
            dati_tabella = []
            for i, item in enumerate(st.session_state['carrello']):
                dati_tabella.append({
                    "N° Riga": i + 1,
                    "Reparto": item["Reparto"],
                    "Prodotto": item["Prodotto"],
                    "Quantità": item["Quantità"],
                    "Prezzo Unit.": item["Prezzo Unit."]
                })
            
            df_carrello_visivo = pd.DataFrame(dati_tabella)
            st.dataframe(df_carrello_visivo, use_container_width=True, hide_index=True)
            
            totale_complessivo = sum([item["Totale"] for item in st.session_state['carrello']])
            
            st.markdown(f"""
                <div class="cart-total-box">
                    <div class="cart-total-label">Totale Provvisorio Ordine:</div>
                    <div class="cart-total-value">{totale_complessivo:,.2f} €</div>
                </div>
            """, unsafe_allow_html=True)
            
            # --- CANCELLAZIONE SINGOLA RIGA TRAMITE NUMERO RIGA CHIARO ---
            st.markdown("### Modifica Carrello")
            opzioni_cancellazione = [f"Riga {i+1} | {item['Prodotto']} (Q.tà: {item['Quantità']})" for i, item in enumerate(st.session_state['carrello'])]
            
            col_sel_del, col_btn_del = st.columns([2, 1])
            with col_sel_del:
                prodotto_da_cancellare = st.selectbox("Seleziona la riga da rimuovere:", opzioni_cancellazione)
            with col_btn_del:
                st.markdown("<br>", unsafe_allow_html=True) 
                if st.button("CANCELLA PRODOTTO"):
                    idx = opzioni_cancellazione.index(prodotto_da_cancellare)
                    st.session_state['carrello'].pop(idx)
                    st.rerun()
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # --- BOTTONI FINALI ---
            col_btn_clear, col_btn_submit = st.columns(2)
            
            with col_btn_clear:
                if st.button("SVUOTA DISTINTA"):
                    st.session_state['carrello'] = []
                    st.rerun() 
                    
            with col_btn_submit:
                if st.button("TRASMETTI ORDINE AD HAVI", type="primary"):
                    st.success("Protocollo approvato. Ordine trasmesso con successo ai sistemi HAVI.")
                    st.session_state['carrello'] = [] 
        else:
            st.info("La distinta d'ordine è attualmente vuota. Seleziona i prodotti in alto per iniziare.")


    # --- CALCOLI EOQ ---
    df_storico = genera_database_simulato(prodotto_scelto)
    d_media = df_storico['Domanda_Scatole'].mean()
    sigma = df_storico['Domanda_Scatole'].std()
    D_annua = d_media * 365
    z_scores = {90: 1.28, 95: 1.65, 99: 2.33}
    z = z_scores[livello_servizio]


    # --- ANALISI LOGISTICA (In basso per consultazione) ---
    st.markdown("---")
    st.markdown("### Dati Storici di Consumo")

    col_dem1, col_dem2 = st.columns(2)
    with col_dem1:
        st.markdown(f"""<div class="metric-box"><div class="metric-title">Domanda Media Giornaliera (d)</div><div class="metric-value">{int(d_media)}</div><div class="metric-subtitle">Scatole al giorno</div></div>""", unsafe_allow_html=True)
    with col_dem2:
        st.markdown(f"""<div class="metric-box"><div class="metric-title">Domanda Annua Stimata (D)</div><div class="metric-value">{int(D_annua):,}</div><div class="metric-subtitle">Scatole totali previste</div></div>""".replace(',', '.'), unsafe_allow_html=True) 

    st.markdown("---")
    st.subheader("Suggerimenti dell'Algoritmo (Modello EOQ)")
    spazio_algoritmo = st.container() 

    st.markdown("---")
    st.markdown("### Parametri Contrattuali (Bloccati da Corporate)")
    
    lead_time = 3
    costo_ordine = 50.0

    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.markdown(f"""<div class="contract-box"><div class="contract-title">Lead Time di Consegna [L]</div><div class="contract-value">🔒 {lead_time} Giorni</div></div>""", unsafe_allow_html=True)
    with col_c2:
        st.markdown(f"""<div class="contract-box"><div class="contract-title">Costo Fisso di Consegna/Ordine [Co]</div><div class="contract-value">🔒 {costo_ordine} €</div></div>""", unsafe_allow_html=True)

    eoq = math.sqrt((2 * D_annua * costo_ordine) / costo_mantenimento)
    scorta_sicurezza = z * sigma * math.sqrt(lead_time)
    rop = (d_media * lead_time) + scorta_sicurezza

    with spazio_algoritmo:
        col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
        with col_kpi1:
            st.markdown(f"""<div class="card-kpi"><div class="kpi-titolo">Quantità Ottimale (EOQ)</div><div class="kpi-valore">{int(eoq)}</div><div class="kpi-dettaglio">Scatole per minimizzare i costi</div></div>""", unsafe_allow_html=True)
        with col_kpi2:
            st.markdown(f"""<div class="card-kpi card-kpi-yellow"><div class="kpi-titolo">Soglia di Riordino (ROP)</div><div class="kpi-valore">{int(rop)}</div><div class="kpi-dettaglio">Ordinare a questa giacenza</div></div>""", unsafe_allow_html=True)
        with col_kpi3:
            st.markdown(f"""<div class="card-kpi card-kpi-green"><div class="kpi-titolo">Scorta di Sicurezza (S)</div><div class="kpi-valore">{int(scorta_sicurezza)}</div><div class="kpi-dettaglio">Copertura imprevisti</div></div>""", unsafe_allow_html=True)


# =====================================================================
# 7. ROUTING: INVENTARIO (Pagina Segnaposto)
# =====================================================================
elif pagina_selezionata == "📋 Inventario":
    st.title("📋 Inventario di Magazzino")
    st.markdown("Visualizzazione giacenze attuali in tempo reale.")
    df_inventario = pd.DataFrame({
        "Reparto": ["Congelato", "Congelato", "Fresco", "Secco", "Operativo"],
        "Prodotto": ["Hamburger di Manzo 4:1", "Patatine Fritte", "Pomodori a Fette", "Panini Regular", "Guanti Nitrile"],
        "Giacenza (Scatole)": [45, 12, 5, 80, 2],
        "Stato": ["🟢 Regolare", "🟡 Attenzione", "🔴 Critico", "🟢 Regolare", "🔴 Critico"]
    })
    st.dataframe(df_inventario, use_container_width=True, hide_index=True)


# =====================================================================
# 8. ROUTING: FILE CONSUMAZIONI (Pagina Segnaposto)
# =====================================================================
elif pagina_selezionata == "📄 File Consumazioni":
    st.title("📄 File Consumazioni")
    st.markdown("Carica il file esportato dalle casse (formato CSV o Excel) per aggiornare il database storico.")
    file_caricato = st.file_uploader("Trascina qui il file", type=['csv', 'xlsx'])
    if file_caricato:
        st.success("✅ File caricato ed elaborato con successo. I dati sono stati aggiornati.")
