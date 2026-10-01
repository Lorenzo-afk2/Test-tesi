import streamlit as st
import pandas as pd
import numpy as np
import math
import plotly.express as px
import os

# =====================================================================
# 1. SETUP INIZIALE E CSS
# =====================================================================
st.set_page_config(page_title="HAVIConnect - Ordini", layout="wide", initial_sidebar_state="expanded")

if os.path.exists("style.css"):
    with open("style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# =====================================================================
# 2. INTESTAZIONE E SELEZIONE REPARTO (LOGICA DINAMICA)
# =====================================================================
st.title("HAVIConnect | Compilazione Ordine")
st.markdown("Seleziona la categoria merceologica e il prodotto per configurare il piano logistico.")

# Dizionario dei reparti con i relativi prodotti aziendali
catalogo_prodotti = {
    "❄️ Congelato": ["Hamburger di Manzo 4:1", "Patatine Fritte (Scatole)", "McNuggets di Pollo"],
    "🥬 Fresco": ["Insalata Iceberg (Buste)", "Pomodori a Fette", "Latte Intero (Brik)"],
    "📦 Secco": ["Panini Regular (Casse)", "Bicchieri Carta (Manicotti)", "Salsa Ketchup (Scatole)"],
    "🧹 Operativo": ["Guanti in Nitrile (Box)", "Sgrassatore Superfici (Taniche)", "Rotoli Asciugatutto"]
}

# Layout a due colonne per la selezione
col_rep, col_prod = st.columns(2)
with col_rep:
    reparto_scelto = st.selectbox("1. Seleziona il Reparto", list(catalogo_prodotti.keys()))
with col_prod:
    prodotto_scelto = st.selectbox("2. Seleziona il Prodotto", catalogo_prodotti[reparto_scelto])

st.markdown("---")
st.markdown(f"### Parametri Logistici per: **{prodotto_scelto}**")

# =====================================================================
# 3. INPUT DEI PARAMETRI (Layout a 4 colonne per massima compattezza)
# =====================================================================
col_in1, col_in2, col_in3, col_in4 = st.columns(4)

with col_in1:
    livello_servizio = st.selectbox("Livello di Servizio", [90, 95, 99], index=1)
with col_in2:
    costo_mantenimento = st.number_input("Costo Mantenimento (€)", value=2.5, step=0.1)
with col_in3:
    lead_time = st.number_input("Lead Time (Giorni)", value=3, step=1)
with col_in4:
    costo_ordine = st.number_input("Costo Consegna/Ordine (€)", value=50.0, step=5.0)

# =====================================================================
# 4. GENERAZIONE DATABASE DINAMICO (Basato sul prodotto scelto)
# =====================================================================
@st.cache_data 
def genera_database_simulato(nome_prodotto):
    date_storiche = pd.date_range(start="2021-01-01", end="2023-12-31", freq="D")
    
    # Trucco: Usiamo la lunghezza del nome del prodotto come "seme" per 
    # generare dati casuali diversi per ogni prodotto!
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

# Generiamo i dati passando il nome del prodotto
df_storico = genera_database_simulato(prodotto_scelto)

# Calcoli matematici sui dati del prodotto
d_media = df_storico['Domanda_Scatole'].mean()
sigma = df_storico['Domanda_Scatole'].std()
D_annua = d_media * 365

z_scores = {90: 1.28, 95: 1.65, 99: 2.33}
z = z_scores[livello_servizio]

# =====================================================================
# 5. SIDEBAR: GRAFICI E DATABASE AGGIORNATI
# =====================================================================
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/McDonald%27s_Golden_Arches.svg/120px-McDonald%27s_Golden_Arches.svg.png", width=60)
st.sidebar.title("Dati di Supporto")
st.sidebar.markdown(f"**Focus:** {prodotto_scelto}")

tab_grafico, tab_database = st.sidebar.tabs(["📈 Trend Vendite", "📝 Database Storico"])

with tab_grafico:
    fig = px.line(df_storico.tail(30), x='Data', y='Domanda_Scatole', markers=True, color_discrete_sequence=['#DA291C'], line_shape='spline')
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white', margin=dict(l=0, r=0, t=10, b=0), xaxis_title=None, yaxis_title=None)
    fig.add_hline(y=float(d_media), line_dash="dash", line_color="#76c04f", annotation_text="Media")
    st.plotly_chart(fig, use_container_width=True)

with tab_database:
    st.dataframe(df_storico[['Data Formattata', 'Giorno Settimana', 'Domanda_Scatole']].head(15), hide_index=True, use_container_width=True)

# =====================================================================
# 6. MOTORE MATEMATICO (EOQ / ROP) E DASHBOARD KPI
# =====================================================================
eoq = math.sqrt((2 * D_annua * costo_ordine) / costo_mantenimento)
scorta_sicurezza = z * sigma * math.sqrt(lead_time)
rop = (d_media * lead_time) + scorta_sicurezza

st.markdown("---")

col_kpi1, col_kpi2, col_kpi3 = st.columns(3)

with col_kpi1:
    st.markdown(f"""<div class="card-kpi"><div class="kpi-titolo">Quantità da Ordinare (EOQ)</div><div class="kpi-valore">{int(eoq)}</div><div class="kpi-dettaglio">Lotto economico ottimale</div></div>""", unsafe_allow_html=True)
with col_kpi2:
    st.markdown(f"""<div class="card-kpi" style="border-top-color: #f2a900 !important;"><div class="kpi-titolo">Soglia di Riordino (ROP)</div><div class="kpi-valore">{int(rop)}</div><div class="kpi-dettaglio">Giacenza d'allarme</div></div>""", unsafe_allow_html=True)
with col_kpi3:
    st.markdown(f"""<div class="card-kpi" style="border-top-color: #76c04f !important;"><div class="kpi-titolo">Scorta di Sicurezza (S)</div><div class="kpi-valore">{int(scorta_sicurezza)}</div><div class="kpi-dettaglio">Copertura imprevisti</div></div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

_, col_btn, _ = st.columns([1, 1, 1])
with col_btn:
    if st.button("APPROVA E TRASMETTI ORDINE"):
        st.success(f"✅ Protocollo approvato. Richiesta per {int(eoq)} unità di '{prodotto_scelto}' trasmessa ai sistemi HAVI.")
        st.balloons()
