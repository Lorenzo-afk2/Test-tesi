import streamlit as st
import pandas as pd
import numpy as np
import math
import plotly.express as px
import os

# =====================================================================
# 1. SETUP INIZIALE E CSS ESTESO (Aggiunte le metriche blu)
# =====================================================================
st.set_page_config(page_title="HAVIConnect - Ordini", layout="wide", initial_sidebar_state="expanded")

# Aggiungiamo un po' di CSS extra per le due metriche di consumo
st.markdown("""
<style>
.metric-box {
    background-color: #003366 !important; /* Blu HAVI */
    border-radius: 10px !important;
    padding: 20px !important;
    text-align: center !important;
    border-bottom: 4px solid #ffc107 !important; /* Giallo McDonald's */
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2) !important;
}
.metric-title {
    color: #ffffff !important;
    font-size: 14px !important;
    font-weight: bold !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
}
.metric-value {
    color: #ffc107 !important;
    font-size: 38px !important;
    font-weight: 900 !important;
    margin: 5px 0px !important;
}
</style>
""", unsafe_allow_html=True)

if os.path.exists("style.css"):
    with open("style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# =====================================================================
# 2. CATALOGO PRODOTTI E LISTINO PREZZI DINAMICO
# =====================================================================
catalogo_prodotti = {
    "❄️ Congelato": ["Hamburger di Manzo 4:1", "Patatine Fritte (Scatole)", "McNuggets di Pollo"],
    "🥬 Fresco": ["Insalata Iceberg (Buste)", "Pomodori a Fette", "Latte Intero (Brik)"],
    "📦 Secco": ["Panini Regular (Casse)", "Bicchieri Carta (Manicotti)", "Salsa Ketchup (Scatole)"],
    "🧹 Operativo": ["Guanti in Nitrile (Box)", "Sgrassatore Superfici (Taniche)", "Rotoli Asciugatutto"]
}

prezzi_prodotti = {
    "Hamburger di Manzo 4:1": 45.00,
    "Patatine Fritte (Scatole)": 28.50,
    "McNuggets di Pollo": 55.00,
    "Insalata Iceberg (Buste)": 15.00,
    "Pomodori a Fette": 18.00,
    "Latte Intero (Brik)": 12.00,
    "Panini Regular (Casse)": 22.00,
    "Bicchieri Carta (Manicotti)": 35.00,
    "Salsa Ketchup (Scatole)": 20.00,
    "Guanti in Nitrile (Box)": 8.50,
    "Sgrassatore Superfici (Taniche)": 14.00,
    "Rotoli Asciugatutto": 19.00
}

# =====================================================================
# 3. INTERFACCIA: SELEZIONE REPARTO E PRODOTTO (RIGA 1)
# =====================================================================
st.title("HAVIConnect | Compilazione Ordine")
st.markdown("Seleziona il prodotto e compila la distinta base dell'ordine.")

col_rep, col_prod = st.columns(2)
with col_rep:
    reparto_scelto = st.selectbox("1. Seleziona il Reparto", list(catalogo_prodotti.keys()))
with col_prod:
    prodotto_scelto = st.selectbox("2. Seleziona il Prodotto", catalogo_prodotti[reparto_scelto])

# =====================================================================
# 4. INTERFACCIA: PREZZO E QUANTITA' (RIGA 2)
# =====================================================================
prezzo_base = prezzi_prodotti[prodotto_scelto]

col_prz, col_qta = st.columns(2)
with col_prz:
    prezzo_unitario = st.number_input("Prezzo Unitario Prodotto (€)", value=prezzo_base, step=1.0)
with col_qta:
    quantita_ordine = st.number_input("Quantità manuale da ordinare (Scatole)", value=150, step=10, 
                                      help="Confronta questo valore con l'EOQ calcolato dal sistema in basso.")

st.markdown("---")
st.markdown(f"### ⚙️ Parametri Logistici per: **{prodotto_scelto}**")

# =====================================================================
# 5. INPUT PARAMETRI LOGISTICI (RIGA 3)
# =====================================================================
col_in1, col_in2, col_in3, col_in4 = st.columns(4)

with col_in1:
    livello_servizio = st.selectbox("Livello di Servizio (%)", [90, 95, 99], index=1)
with col_in2:
    costo_mantenimento_default = round(prezzo_base * 0.15, 2)
    costo_mantenimento = st.number_input("Costo Mantenimento (€)", value=costo_mantenimento_default, step=0.1)
with col_in3:
    lead_time = st.number_input("Lead Time (Giorni)", value=3, step=1)
with col_in4:
    costo_ordine = st.number_input("Costo Consegna/Ordine (€)", value=50.0, step=5.0)

# =====================================================================
# 6. GENERAZIONE DATABASE DINAMICO E CALCOLI STATISTICI
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
# 7. NUOVA SEZIONE: DATI DI CONSUMO EVIDENZIATI CON STILE HAVI
# =====================================================================
st.markdown("---")
st.markdown("### 📊 Dati Storici di Consumo")

col_dem1, col_dem2 = st.columns(2)

with col_dem1:
    st.markdown(f"""
        <div class="metric-box">
            <div class="metric-title">Domanda Media Giornaliera (d)</div>
            <div class="metric-value">{int(d_media)}</div>
            <div style="color: white; font-size: 12px;">Scatole al giorno</div>
        </div>
    """, unsafe_allow_html=True)

with col_dem2:
    st.markdown(f"""
        <div class="metric-box">
            <div class="metric-title">Domanda Annua Stimata (D)</div>
            <div class="metric-value">{int(D_annua):,}</div>
            <div style="color: white; font-size: 12px;">Scatole totali previste</div>
        </div>
    """.replace(',', '.'), unsafe_allow_html=True) # Sostituisce la virgola delle migliaia col punto

# =====================================================================
# 8. SIDEBAR: GRAFICI E DATABASE AGGIORNATI
# =====================================================================
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/McDonald%27s_Golden_Arches.svg/120px-McDonald%27s_Golden_Arches.svg.png", width=60)
st.sidebar.title("Dati di Supporto")
st.sidebar.markdown(f"**Focus Storico:** {prodotto_scelto}")

tab_grafico, tab_database = st.sidebar.tabs(["📈 Trend Vendite", "📝 Database Storico"])

with tab_grafico:
    fig = px.line(df_storico.tail(30), x='Data', y='Domanda_Scatole', markers=True, color_discrete_sequence=['#DA291C'], line_shape='spline')
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white', margin=dict(l=0, r=0, t=10, b=0), xaxis_title=None, yaxis_title=None)
    fig.add_hline(y=float(d_media), line_dash="dash", line_color="#76c04f", annotation_text="Media")
    st.plotly_chart(fig, use_container_width=True)

with tab_database:
    st.dataframe(df_storico[['Data Formattata', 'Giorno Settimana', 'Domanda_Scatole']].head(15), hide_index=True, use_container_width=True)

# =====================================================================
# 9. MOTORE MATEMATICO (EOQ / ROP) E DASHBOARD KPI
# =====================================================================
eoq = math.sqrt((2 * D_annua * costo_ordine) / costo_mantenimento)
scorta_sicurezza = z * sigma * math.sqrt(lead_time)
rop = (d_media * lead_time) + scorta_sicurezza

st.markdown("---")
st.subheader("📦 Suggerimenti dell'Algoritmo (Modello EOQ)")

col_kpi1, col_kpi2, col_kpi3 = st.columns(3)

with col_kpi1:
    st.markdown(f"""<div class="card-kpi"><div class="kpi-titolo">Quantità Ottimale (EOQ)</div><div class="kpi-valore">{int(eoq)}</div><div class="kpi-dettaglio">Scatole per minimizzare i costi</div></div>""", unsafe_allow_html=True)
with col_kpi2:
    st.markdown(f"""<div class="card-kpi" style="border-top-color: #f2a900 !important;"><div class="kpi-titolo">Soglia di Riordino (ROP)</div><div class="kpi-valore">{int(rop)}</div><div class="kpi-dettaglio">Ordinare a questa giacenza</div></div>""", unsafe_allow_html=True)
with col_kpi3:
    st.markdown(f"""<div class="card-kpi" style="border-top-color: #76c04f !important;"><div class="kpi-titolo">Scorta di Sicurezza (S)</div><div class="kpi-valore">{int(scorta_sicurezza)}</div><div class="kpi-dettaglio">Copertura imprevisti</div></div>""", unsafe_allow_html=True)

# =====================================================================
# 10. TOTALE E TRASMISSIONE ORDINE
# =====================================================================
st.markdown("<br>", unsafe_allow_html=True)

totale_ordine = quantita_ordine * prezzo_unitario

_, col_btn, _ = st.columns([1, 1, 1])
with col_btn:
    if st.button("APPROVA E TRASMETTI ORDINE"):
        st.success(f"✅ Protocollo approvato. Ordine di **{quantita_ordine} scatole** di '{prodotto_scelto}' trasmesso ai sistemi HAVI.")
        st.info(f"💶 Valore totale dell'ordine generato: **{totale_ordine:,.2f} €**")
        st.balloons()
