import streamlit as st
import pandas as pd
import numpy as np
import math
import plotly.express as px
import os

# 1. SETUP INIZIALE
st.set_page_config(page_title="HAVIConnect - Gestione Scorte", layout="wide")

# Iniezione sicura del CSS
if os.path.exists("style.css"):
    with open("style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# 2. GENERAZIONE DATABASE (3 ANNI)
@st.cache_data 
def genera_database_simulato():
    date_storiche = pd.date_range(start="2021-01-01", end="2023-12-31", freq="D")
    
    np.random.seed(42)
    vendite = np.random.normal(loc=200, scale=30, size=len(date_storiche))
    
    df = pd.DataFrame({'Data': date_storiche, 'Domanda_Scatole': vendite})
    
    # Logica aziendale (picchi weekend)
    df['Giorno_Num'] = df['Data'].dt.dayofweek 
    df.loc[df['Giorno_Num'] >= 5, 'Domanda_Scatole'] *= 1.40 
    
    df['Domanda_Scatole'] = np.maximum(df['Domanda_Scatole'].round(), 0).astype(int)
    
    # Traduzione giorni
    mappa_giorni = {0: 'Lunedì', 1: 'Martedì', 2: 'Mercoledì', 3: 'Giovedì', 4: 'Venerdì', 5: 'Sabato', 6: 'Domenica'}
    df['Giorno Settimana'] = df['Giorno_Num'].map(mappa_giorni)
    df['Data Formattata'] = df['Data'].dt.strftime('%d-%m-%Y')
    
    return df

df_storico = genera_database_simulato()

# 3. PARAMETRI MATEMATICI BASE
d_media = df_storico['Domanda_Scatole'].mean()
sigma = df_storico['Domanda_Scatole'].std()
D_annua = d_media * 365

# 4. SIDEBAR - INPUT MANAGER
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/McDonald%27s_Golden_Arches.svg/120px-McDonald%27s_Golden_Arches.svg.png")
st.sidebar.title("Parametri Logistici")

costo_ordine = st.sidebar.number_input("Costo per singolo ordine (€) [Co]", value=50.0, step=5.0)
costo_mantenimento = st.sidebar.number_input("Costo mantenimento annuo (€) [Cm]", value=2.5, step=0.1)
lead_time = st.sidebar.number_input("Lead Time (Giorni) [L]", value=3, step=1)
livello_servizio = st.sidebar.selectbox("Livello di Servizio", [90, 95, 99], index=1)

z_scores = {90: 1.28, 95: 1.65, 99: 2.33}
z = z_scores[livello_servizio]

# 5. MOTORE MATEMATICO (EOQ / ROP)
eoq = math.sqrt((2 * D_annua * costo_ordine) / costo_mantenimento)
scorta_sicurezza = z * sigma * math.sqrt(lead_time)
rop = (d_media * lead_time) + scorta_sicurezza

# 6. DASHBOARD PRINCIPALE
st.title("HAVIConnect | Ottimizzazione Rifornimenti")
st.markdown("Analisi basata sulla simulazione statistica di 1.095 giorni di esercizio (3 anni).")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""<div class="card-kpi"><div class="kpi-titolo">Lotto Economico (EOQ)</div><div class="kpi-valore">{int(eoq)}</div><div class="kpi-dettaglio">Scatole da ordinare per minimizzare i costi</div></div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""<div class="card-kpi" style="border-top-color: #f2a900 !important;"><div class="kpi-titolo">Punto di Riordino (ROP)</div><div class="kpi-valore">{int(rop)}</div><div class="kpi-dettaglio">Effettuare l'ordine a questa soglia</div></div>""", unsafe_allow_html=True)
with col3:
    st.markdown(f"""<div class="card-kpi" style="border-top-color: #76c04f !important;"><div class="kpi-titolo">Scorta di Sicurezza (S)</div><div class="kpi-valore">{int(scorta_sicurezza)}</div><div class="kpi-dettaglio">Cuscinetto per coprire variabilità e ritardi</div></div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col_grafico, col_tabella = st.columns([2, 1])

with col_grafico:
    st.subheader("📈 Trend Domanda (Ultimi 30 giorni)")
    fig = px.line(df_storico.tail(30), x='Data', y='Domanda_Scatole', markers=True, color_discrete_sequence=['#DA291C'], line_shape='spline')
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white')
    fig.add_hline(y=d_media, line_dash="dash", line_color="#76c04f", annotation_text="Media Giornaliera")
    st.plotly_chart(fig, use_container_width=True)

with col_tabella:
    st.subheader("📝 Estratto Database")
    st.dataframe(df_storico[['Data Formattata', 'Giorno Settimana', 'Domanda_Scatole']].head(10), hide_index=True, use_container_width=True)

st.markdown("---")
_, col_btn, _ = st.columns([1, 1, 1])
with col_btn:
    if st.button("APPROVA E TRASMETTI ORDINE"):
        st.success("✅ Protocollo logistico approvato. Ordine trasmesso ai sistemi HAVI centrali.")
        st.balloons()
