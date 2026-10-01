import streamlit as st
import pandas as pd
import numpy as np
import math
import plotly.express as px

# =====================================================================
# 1. SETUP INIZIALE E INIEZIONE CSS
# =====================================================================
st.set_page_config(page_title="HAVIConnect - Gestione Scorte", layout="wide")

# Funzione per leggere il file style.css e applicarlo a Streamlit
def applica_css_esterno(nome_file):
    try:
        with open(nome_file) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("Attenzione: file style.css non trovato nella cartella.")

applica_css_esterno("style.css")


# =====================================================================
# 2. GENERAZIONE DEL DATABASE (3 ANNI STORICI SIMULATI)
# =====================================================================
@st.cache_data # Memorizza i dati per non ricalcolarli ad ogni click
def genera_database_simulato():
    # A. Creazione del calendario di 1095 giorni (3 anni)
    date_storiche = pd.date_range(start="2021-01-01", end="2023-12-31", freq="D")
    
    # B. Generazione vendite base con Curva di Gauss (Media=200, Dev.Std=30)
    np.random.seed(42) # Seed fisso per stabilità dei dati
    vendite = np.random.normal(loc=200, scale=30, size=len(date_storiche))
    
    # C. Creazione della Tabella
    df = pd.DataFrame({'Data': date_storiche, 'Domanda_Scatole': vendite})
    
    # D. Logica Weekend (Sabato e Domenica = +40% di vendite)
    df['Giorno_Num'] = df['Data'].dt.dayofweek # 0=Lunedì, 6=Domenica
    df.loc[df['Giorno_Num'] >= 5, 'Domanda_Scatole'] *= 1.40 
    
    # E. Pulizia matematica (Nessun decimale, nessun numero negativo)
    df['Domanda_Scatole'] = np.maximum(df['Domanda_Scatole'].round(), 0).astype(int)
    
    # F. Mappatura dei giorni in Italiano per l'interfaccia utente
    mappa_giorni = {
        0: 'Lunedì', 1: 'Martedì', 2: 'Mercoledì', 3: 'Giovedì', 
        4: 'Venerdì', 5: 'Sabato', 6: 'Domenica'
    }
    df['Giorno Settimana'] = df['Giorno_Num'].map(mappa_giorni)
    
    # G. Formattazione data leggibile (GG-MM-AAAA)
    df['Data Formattata'] = df['Data'].dt.strftime('%d-%m-%Y')
    
    return df

df_storico = genera_database_simulato()


# =====================================================================
# 3. ESTRAZIONE PARAMETRI MATEMATICI DAL DATABASE
# =====================================================================
d_media = df_storico['Domanda_Scatole'].mean()       # Domanda media giornaliera (d)
sigma = df_storico['Domanda_Scatole'].std()          # Variabilità / Deviazione Standard
D_annua = d_media * 365                              # Domanda Annua Totale (D)


# =====================================================================
# 4. INTERFACCIA UTENTE: SIDEBAR (INPUT MANUALE)
# =====================================================================
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/McDonald%27s_Golden_Arches.svg/120px-McDonald%27s_Golden_Arches.svg.png")
st.sidebar.title("Parametri Logistici")
st.sidebar.markdown("Modifica i valori per ricalcolare il piano in tempo reale.")

costo_ordine = st.sidebar.number_input("Costo per singolo ordine (€) [Co]", value=50.0, step=5.0)
costo_mantenimento = st.sidebar.number_input("Costo mantenimento annuo per scatola (€) [Cm]", value=2.5, step=0.1)
lead_time = st.sidebar.number_input("Lead Time di Consegna (Giorni) [L]", value=3, step=1)
livello_servizio = st.sidebar.selectbox("Livello di Servizio Desiderato", [90, 95, 99], index=1)

# Conversione del Livello di Servizio in Z-Score Statistico
z_scores = {90: 1.28, 95: 1.65, 99: 2.33}
z = z_scores[livello_servizio]


# =====================================================================
# 5. IL MOTORE MATEMATICO (CALCOLO EOQ E ROP)
# =====================================================================
# EOQ = Radice quadrata di [ (2 * Domanda Annua * Costo Ordine) / Costo Mantenimento ]
eoq = math.sqrt((2 * D_annua * costo_ordine) / costo_mantenimento)

# Scorta di Sicurezza (S) = Z * Sigma * Radice quadrata(Lead Time)
scorta_sicurezza = z * sigma * math.sqrt(lead_time)

# Punto di Riordino (ROP) = (Domanda giornaliera * Lead Time) + Scorta di Sicurezza
rop = (d_media * lead_time) + scorta_sicurezza


# =====================================================================
# 6. INTERFACCIA UTENTE: DASHBOARD PRINCIPALE
# =====================================================================
st.title("HAVIConnect | Ottimizzazione Rifornimenti")
st.markdown("Analisi basata sulla simulazione statistica di 1.095 giorni di esercizio (3 anni).")

# A. Le Card KPI (Usiamo l'HTML per agganciarci alle classi CSS personalizzate)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
        <div class="card-kpi">
            <div class="kpi-titolo">Lotto Economico (EOQ)</div>
            <div class="kpi-valore">{int(eoq)}</div>
            <div class="kpi-dettaglio">Scatole da ordinare per minimizzare i costi</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="card-kpi" style="border-top-color: #f2a900 !important;">
            <div class="kpi-titolo">Punto di Riordino (ROP)</div>
            <div class="kpi-valore">{int(rop)}</div>
            <div class="kpi-dettaglio">Effettuare l'ordine quando la giacenza tocca questa soglia</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="card-kpi" style="border-top-color: #76c04f !important;">
            <div class="kpi-titolo">Scorta di Sicurezza (S)</div>
            <div class="kpi-valore">{int(scorta_sicurezza)}</div>
            <div class="kpi-dettaglio">Cuscinetto matematico per coprire variabilità e ritardi</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True) # Spazio vuoto

# B. Analisi Visiva: Grafico e Tabella Dati
col_grafico, col_tabella = st.columns([2, 1])

with col_grafico:
    st.subheader("📈 Trend Domanda (Ultimi 30 giorni)")
    df_grafico = df_storico.tail(30) # Prendiamo solo l'ultimo mese
    
    fig = px.line(df_grafico, x='Data', y='Domanda_Scatole', markers=True, 
                  color_discrete_sequence=['#DA291C'], line_shape='spline')
    
    # Sfondo trasparente per il grafico per fondersi col tema scuro
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white')
    # Linea tratteggiata verde della media matematica
    fig.add_hline(y=d_media, line_dash="dashed", line_color="#76c04f", annotation_text="Media Giornaliera")
    
    st.plotly_chart(fig, use_container_width=True)

with col_tabella:
    st.subheader("📝 Estratto Database Storico")
    st.markdown("Prime righe dei dati simulati:")
    # Mostriamo solo le colonne formattate per l'utente finale
    df_visivo = df_storico[['Data Formattata', 'Giorno Settimana', 'Domanda_Scatole']]
    st.dataframe(df_visivo.head(10), hide_index=True, use_container_width=True)

# C. Bottone di Esecuzione Finale
st.markdown("---")
_, col_btn, _ = st.columns([1, 1, 1]) # Centriamo il bottone
with col_btn:
    if st.button("APPROVA E TRASMETTI ORDINE"):
        st.success("✅ Protocollo logistico approvato. Ordine trasmesso ai sistemi HAVI centrali.")
        st.balloons()

