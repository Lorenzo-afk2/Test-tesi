import streamlit as st
import pandas as pd
import numpy as np
import math
import plotly.express as px
import os

# =====================================================================
# 1. SETUP INIZIALE
# =====================================================================
st.set_page_config(page_title="HAVIConnect - Ordini", layout="wide", initial_sidebar_state="expanded")

# Iniezione sicura del CSS aziendale
if os.path.exists("style.css"):
    with open("style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# =====================================================================
# 2. GENERAZIONE DATABASE (3 ANNI)
# =====================================================================
@st.cache_data 
def genera_database_simulato():
    date_storiche = pd.date_range(start="2021-01-01", end="2023-12-31", freq="D")
    np.random.seed(42)
    vendite = np.random.normal(loc=200, scale=30, size=len(date_storiche))
    df = pd.DataFrame({'Data': date_storiche, 'Domanda_Scatole': vendite})
    
    df['Giorno_Num'] = df['Data'].dt.dayofweek 
    df.loc[df['Giorno_Num'] >= 5, 'Domanda_Scatole'] *= 1.40 
    df['Domanda_Scatole'] = np.maximum(df['Domanda_Scatole'].round(), 0).astype(int)
    
    mappa_giorni = {0: 'Lunedì', 1: 'Martedì', 2: 'Mercoledì', 3: 'Giovedì', 4: 'Venerdì', 5: 'Sabato', 6: 'Domenica'}
    df['Giorno Settimana'] = df['Giorno_Num'].map(mappa_giorni)
    df['Data Formattata'] = df['Data'].dt.strftime('%d-%m-%Y')
    
    return df

df_storico = genera_database_simulato()

# Calcoli base sui dati
d_media = df_storico['Domanda_Scatole'].mean()
sigma = df_storico['Domanda_Scatole'].std()
D_annua = d_media * 365

# =====================================================================
# 3. SIDEBAR: TAB GRAFICI E DATABASE
# =====================================================================
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/McDonald%27s_Golden_Arches.svg/120px-McDonald%27s_Golden_Arches.svg.png", width=60)
st.sidebar.title("Dati di Supporto")
st.sidebar.markdown("Consulta lo storico prima di compilare l'ordine.")

# Creazione dei Tab nella Sidebar
tab_grafico, tab_database = st.sidebar.tabs(["📈 Trend Vendite", "📝 Database Storico"])

with tab_grafico:
    st.markdown("**Ultimi 30 giorni**")
    fig = px.line(df_storico.tail(30), x='Data', y='Domanda_Scatole', markers=True, color_discrete_sequence=['#DA291C'], line_shape='spline')
    # Ottimizzazione degli spazi per far entrare il grafico nella barra laterale
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)', 
        font_color='white',
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis_title=None,
        yaxis_title=None
    )
    # Linea della media corretta con "dash"
    fig.add_hline(y=float(d_media), line_dash="dash", line_color="#76c04f", annotation_text="Media")
    st.plotly_chart(fig, use_container_width=True)

with tab_database:
    st.markdown("**Estratto Dati Simulati**")
    st.dataframe(df_storico[['Data Formattata', 'Giorno Settimana', 'Domanda_Scatole']].head(15), hide_index=True, use_container_width=True)


# =====================================================================
# 4. PAGINA PRINCIPALE: INSERIMENTO DATI (INPUT MANAGER)
# =====================================================================
st.title("HAVIConnect | Compilazione Ordine")
st.markdown("Inserisci i parametri contrattuali e logistici per generare il piano di rifornimento ottimizzato.")

# Impaginazione elegante a due colonne per gli input manuali
col_in1, col_in2 = st.columns(2)

with col_in1:
    costo_ordine = st.number_input("Costo per singolo ordine (€) [Co]", value=50.0, step=5.0)
    lead_time = st.number_input("Lead Time di Consegna (Giorni) [L]", value=3, step=1)

with col_in2:
    costo_mantenimento = st.number_input("Costo mantenimento annuo per scatola (€) [Cm]", value=2.5, step=0.1)
    livello_servizio = st.selectbox("Livello di Servizio Desiderato (%)", [90, 95, 99], index=1)

# Motore di Conversione Statistica
z_scores = {90: 1.28, 95: 1.65, 99: 2.33}
z = z_scores[livello_servizio]

# =====================================================================
# 5. MOTORE MATEMATICO (EOQ / ROP)
# =====================================================================
eoq = math.sqrt((2 * D_annua * costo_ordine) / costo_mantenimento)
scorta_sicurezza = z * sigma * math.sqrt(lead_time)
rop = (d_media * lead_time) + scorta_sicurezza

# =====================================================================
# 6. PAGINA PRINCIPALE: ANTEPRIMA ORDINE E INVIO
# =====================================================================
st.markdown("---")
st.subheader("📦 Anteprima dell'Ordine Calcolato")

# Le 3 Card KPI affiancate
col_kpi1, col_kpi2, col_kpi3 = st.columns(3)

with col_kpi1:
    st.markdown(f"""<div class="card-kpi"><div class="kpi-titolo">Quantità da Ordinare (EOQ)</div><div class="kpi-valore">{int(eoq)}</div><div class="kpi-dettaglio">Scatole (Minimizzazione Costi)</div></div>""", unsafe_allow_html=True)
with col_kpi2:
    st.markdown(f"""<div class="card-kpi" style="border-top-color: #f2a900 !important;"><div class="kpi-titolo">Soglia di Riordino (ROP)</div><div class="kpi-valore">{int(rop)}</div><div class="kpi-dettaglio">Ordinare a questa giacenza</div></div>""", unsafe_allow_html=True)
with col_kpi3:
    st.markdown(f"""<div class="card-kpi" style="border-top-color: #76c04f !important;"><div class="kpi-titolo">Scorta di Sicurezza (S)</div><div class="kpi-valore">{int(scorta_sicurezza)}</div><div class="kpi-dettaglio">Copertura imprevisti</div></div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Tasto di approvazione centrato
_, col_btn, _ = st.columns([1, 1, 1])
with col_btn:
    if st.button("APPROVA E TRASMETTI ORDINE"):
        st.success(f"✅ Protocollo logistico approvato. Richiesta per {int(eoq)} scatole trasmessa ai sistemi HAVI.")
        st.balloons()
