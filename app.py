import streamlit as st
import pandas as pd
import numpy as np
import math
import plotly.express as px
import os

# =====================================================================
# 1. SETUP INIZIALE E CSS ESTESO
# =====================================================================
st.set_page_config(page_title="HAVIConnect - Ordini", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
.metric-box { background-color: #003366 !important; border-radius: 10px !important; padding: 20px !important; text-align: center !important; border-bottom: 4px solid #ffc107 !important; box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2) !important; }
.metric-title { color: #ffffff !important; font-size: 14px !important; font-weight: bold !important; text-transform: uppercase !important; letter-spacing: 1px !important; }
.metric-value { color: #ffc107 !important; font-size: 38px !important; font-weight: 900 !important; margin: 5px 0px !important; }
</style>
""", unsafe_allow_html=True)

if os.path.exists("style.css"):
    with open("style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


# =====================================================================
# 2. SISTEMA DI AUTENTICAZIONE (LOGIN)
# =====================================================================
# Inizializziamo lo stato della sessione per ricordare se l'utente è loggato
if 'autenticato' not in st.session_state:
    st.session_state['autenticato'] = False

# Se NON è autenticato, mostriamo la pagina di Login
if not st.session_state['autenticato']:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
            <div style="background-color: white; padding: 40px; border-radius: 15px; text-align: center; box-shadow: 0px 10px 20px rgba(0,0,0,0.2); border-top: 5px solid #DA291C;">
                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/McDonald%27s_Golden_Arches.svg/120px-McDonald%27s_Golden_Arches.svg.png" width="80" style="margin-bottom: 20px;">
                <h2 style="color: #0a111a; margin-bottom: 5px;">HAVIConnect</h2>
                <p style="color: #7b8898; font-style: italic; margin-bottom: 20px;">Portale Logistico Enterprise</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Form di Login
        with st.form("login_form"):
            username = st.text_input("👤 ID Dipendente (usa: manager)")
            password = st.text_input("🔒 Password (usa: logistica)", type="password")
            submitted = st.form_submit_button("ACCEDI AL SISTEMA")
            
            if submitted:
                # Credenziali di default per la tesi
                if username == "manager" and password == "logistica":
                    st.session_state['autenticato'] = True
                    st.rerun() # Ricarica la pagina per far sparire il login
                else:
                    st.error("❌ Credenziali errate. Riprova.")
    
    st.stop() # FERMA IL CODICE QUI: Se non sei loggato, non puoi vedere il resto!


# =====================================================================
# 3. CATALOGO PRODOTTI E LISTINO PREZZI
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


# =====================================================================
# 4. INTERFACCIA: SELEZIONE E QUANTITA'
# =====================================================================
st.title("HAVIConnect | Compilazione Ordine")
st.markdown("Seleziona il prodotto e compila la distinta base dell'ordine.")

col_rep, col_prod = st.columns(2)
with col_rep:
    reparto_scelto = st.selectbox("1. Seleziona il Reparto", list(catalogo_prodotti.keys()))
with col_prod:
    prodotto_scelto = st.selectbox("2. Seleziona il Prodotto", catalogo_prodotti[reparto_scelto])

prezzo_base = prezzi_prodotti[prodotto_scelto]

col_prz, col_qta = st.columns(2)
with col_prz:
    prezzo_unitario = st.number_input("Prezzo Unitario Prodotto (€)", value=prezzo_base, step=1.0)
with col_qta:
    quantita_ordine = st.number_input("Quantità manuale da ordinare (Scatole)", value=150, step=10)

st.markdown("---")
st.markdown(f"### ⚙️ Parametri Operativi per: **{prodotto_scelto}**")


# =====================================================================
# 5. PARAMETRI OPERATIVI (Solo Servizio e Mantenimento)
# =====================================================================
col_in1, col_in2 = st.columns(2)

with col_in1:
    livello_servizio = st.selectbox("Livello di Servizio (%)", [90, 95, 99], index=1)
with col_in2:
    costo_mantenimento_default = round(prezzo_base * 0.15, 2)
    costo_mantenimento = st.number_input("Costo Mantenimento unitario (€)", value=costo_mantenimento_default, step=0.1)


# =====================================================================
# 6. GENERAZIONE DATABASE E CALCOLI
# =====================================================================
@st.cache_data 
def genera_database_simulato(nome_prodotto):
    date_storiche = pd.date_range(start="2021-01-01", end="2023-12-31", freq="D")
    np.random.seed(len(nome_prodotto) * 42) 
    
    vendite = np.random.normal(loc=200, scale=30, size=len(date_storiche))
    df = pd.DataFrame({'Data': date_storiche, 'Domanda_Scatole': vendite})
    
    df['Giorno_Num'] = df['Data'].dt.dayofweek 
    df.loc[df['Giorno_Num'] >= 5, 'Domanda_Scatole'] *= 1.40 
    df['Domanda_Scatole'] = np.maximum(df['Domanda_Scatole'].round(), 0).astype(int)
    
    mappa_giorni = {0: 'Lunedì', 1: 'Martedì', 2: 'Mercoledì', 3: 'Giovedì', 4: 'Venerdì', 5: 'Sabato', 6: 'Domenica'}
    df['Giorno Settimana'] = df['Giorno_Num'].map(mappa_giorni)
    df['Data Formattata'] = df['Data'].dt.strftime('%d-%m-%Y')
    
    return df

df_storico = genera_database_simulato(prodotto_scelto)

d_media = df_storico['Domanda_Scatole'].mean()
sigma = df_storico['Domanda_Scatole'].std()
D_annua = d_media * 365

z_scores = {90: 1.28, 95: 1.65, 99: 2.33}
z = z_scores[livello_servizio]


# =====================================================================
# 7. DATI DI CONSUMO (Le Card Blu)
# =====================================================================
st.markdown("---")
st.markdown("### 📊 Dati Storici di Consumo")

col_dem1, col_dem2 = st.columns(2)
with col_dem1:
    st.markdown(f"""<div class="metric-box"><div class="metric-title">Domanda Media Giornaliera (d)</div><div class="metric-value">{int(d_media)}</div><div style="color: white; font-size: 12px;">Scatole al giorno</div></div>""", unsafe_allow_html=True)
with col_dem2:
    st.markdown(f"""<div class="metric-box"><div class="metric-title">Domanda Annua Stimata (D)</div><div class="metric-value">{int(D_annua):,}</div><div style="color: white; font-size: 12px;">Scatole totali previste</div></div>""".replace(',', '.'), unsafe_allow_html=True) 


# =====================================================================
# 8. SIDEBAR (Si aggiorna col prodotto)
# =====================================================================
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/McDonald%27s_Golden_Arches.svg/120px-McDonald%27s_Golden_Arches.svg.png", width=60)
st.sidebar.title("Dati di Supporto")
tab_grafico, tab_database = st.sidebar.tabs(["📈 Trend Vendite", "📝 Database Storico"])

with tab_grafico:
    fig = px.line(df_storico.tail(30), x='Data', y='Domanda_Scatole', markers=True, color_discrete_sequence=['#DA291C'], line_shape='spline')
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white', margin=dict(l=0, r=0, t=10, b=0), xaxis_title=None, yaxis_title=None)
    fig.add_hline(y=float(d_media), line_dash="dash", line_color="#76c04f", annotation_text="Media")
    st.plotly_chart(fig, use_container_width=True)

with tab_database:
    st.dataframe(df_storico[['Data Formattata', 'Giorno Settimana', 'Domanda_Scatole']].head(15), hide_index=True, use_container_width=True)


# =====================================================================
# 9. SUGGERIMENTI ALGORITMO (USO DEL CONTAINER)
# =====================================================================
st.markdown("---")
st.subheader("📦 Suggerimenti dell'Algoritmo (Modello EOQ)")
# Creiamo una "scatola vuota". La riempiremo dopo aver letto i parametri contrattuali in basso!
spazio_algoritmo = st.container() 


# =====================================================================
# 10. PARAMETRI CONTRATTUALI
# =====================================================================
st.markdown("---")
st.markdown("### 📄 Parametri Contrattuali")
col_c1, col_c2 = st.columns(2)
with col_c1:
    lead_time = st.number_input("Lead Time di Consegna (Giorni) [L]", value=3, step=1)
with col_c2:
    costo_ordine = st.number_input("Costo Fisso di Consegna/Ordine (€) [Co]", value=50.0, step=5.0)


# =====================================================================
# 11. CALCOLO E INSERIMENTO MATEMATICO NEL CONTAINER IN ALTO
# =====================================================================
# Ora che abbiamo TUTTI i dati (compresi i parametri contrattuali), facciamo la matematica
eoq = math.sqrt((2 * D_annua * costo_ordine) / costo_mantenimento)
scorta_sicurezza = z * sigma * math.sqrt(lead_time)
rop = (d_media * lead_time) + scorta_sicurezza

# Usiamo il blocco vuoto creato al passo 9 per iniettare i risultati visivamente SOPRA
with spazio_algoritmo:
    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    with col_kpi1:
        st.markdown(f"""<div class="card-kpi"><div class="kpi-titolo">Quantità Ottimale (EOQ)</div><div class="kpi-valore">{int(eoq)}</div><div class="kpi-dettaglio">Scatole per minimizzare i costi</div></div>""", unsafe_allow_html=True)
    with col_kpi2:
        st.markdown(f"""<div class="card-kpi" style="border-top-color: #f2a900 !important;"><div class="kpi-titolo">Soglia di Riordino (ROP)</div><div class="kpi-valore">{int(rop)}</div><div class="kpi-dettaglio">Ordinare a questa giacenza</div></div>""", unsafe_allow_html=True)
    with col_kpi3:
        st.markdown(f"""<div class="card-kpi" style="border-top-color: #76c04f !important;"><div class="kpi-titolo">Scorta di Sicurezza (S)</div><div class="kpi-valore">{int(scorta_sicurezza)}</div><div class="kpi-dettaglio">Copertura imprevisti</div></div>""", unsafe_allow_html=True)


# =====================================================================
# 12. TOTALE E TRASMISSIONE ORDINE
# =====================================================================
st.markdown("<br>", unsafe_allow_html=True)

totale_ordine = quantita_ordine * prezzo_unitario

_, col_btn, _ = st.columns([1, 1, 1])
with col_btn:
    if st.button("APPROVA E TRASMETTI ORDINE"):
        st.success(f"✅ Protocollo approvato. Ordine di **{quantita_ordine} scatole** di '{prodotto_scelto}' trasmesso ai sistemi HAVI.")
        st.info(f"💶 Valore totale dell'ordine generato: **{totale_ordine:,.2f} €**")
        st.balloons()
