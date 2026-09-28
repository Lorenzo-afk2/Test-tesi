import streamlit as st
import pandas as pd
import plotly.express as px  # Importiamo Plotly per i grafici

st.set_page_config(layout="wide")
st.title("📦 Analisi Scorte: Hamburger di Manzo (Core Product)")

# Creiamo due colonne per affiancare l'immagine e il grafico
col_sinistra, col_destra = st.columns([1, 2]) # La destra è grande il doppio della sinistra

with col_sinistra:
    st.subheader("Scheda Prodotto")
    
    # 1. Spiegazione st.image
    # st.image serve per mostrare immagini STATICHE (foto, loghi, schemi).
    # Non ha interattività. Prende un file dal tuo PC o un link web e lo fa vedere.
    # L'attributo use_container_width=True fa sì che l'immagine occupi tutta la colonna.
    
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/4/4b/McDonald%27s_burger_patties.jpg", 
        caption="Cartone Standard da 50 pezzi (HAVI Logistics)",
        use_container_width=True
    )
    
    st.write("Questo è il prodotto ad alta rotazione che stiamo analizzando.")

with col_destra:
    st.subheader("Andamento Livello Scorte (Ultimi 5 Giorni)")
    
    # Prepariamo dei dati inventati per far funzionare il grafico
    dati_finti = pd.DataFrame({
        "Giorno": ["Lun", "Mar", "Mer", "Gio", "Ven"],
        "Pezzi in Cella": [200, 150, 90, 250, 180] # Il giovedì è arrivato il rifornimento (EOQ)
    })
    
    # Prima: Diciamo a Plotly Express di "costruire" un grafico a linee
    grafico_linee = px.line(
        dati_finti, 
        x="Giorno", 
        y="Pezzi in Cella", 
        markers=True, # Mette un pallino su ogni giorno
        title="Modello a dente di sega (Simulazione)"
    )
    
    # 2. Spiegazione st.plotly_chart
    # st.plotly_chart è il "proiettore". Prende l'oggetto matematico creato da Plotly 
    # e lo stampa sullo schermo del tuo iPad rendendolo INTERATTIVO.
    # L'utente può zoomare, scorrere o scaricare il grafico come immagine (PNG).
    
    st.plotly_chart(
        grafico_linee, 
        use_container_width=True # Anche qui usiamo questo attributo per allargarlo!
    )
