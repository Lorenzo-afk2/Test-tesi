import streamlit as st
import pandas as pd # Ci serve per creare la tabella dati

st.title("📊 Cruscotto Direzionale Scorte (DSS)")

# ==========================================
# 1. st.metric (I numeri che contano)
# ==========================================
st.subheader("Indicatori Chiave (KPI)")
st.write("st.metric crea quei bellissimi riquadri con il numero in grande e la variazione in piccolo.")

# Usiamo st.columns per metterli uno di fianco all'altro
col1, col2, col3 = st.columns(3)

# La metrica base
col1.metric(label="Lotto Ottimale (EOQ)", value="150 colli")

# La metrica con variazione (delta). Di default, positivo è verde.
col2.metric(label="Scorta di Sicurezza", value="45 colli", delta="+12 colli da ieri")

# Se una variazione in aumento è negativa (es. i costi salgono), possiamo invertire il colore 
# usando delta_color="inverse". L'aumento diventa rosso.
col3.metric(label="Costo Totale Logistico", value="€ 1.250", delta="€ 350", delta_color="inverse")

st.divider()

# Creiamo un piccolo database inventato per fare l'esempio delle tabelle
dati_magazzino = pd.DataFrame({
    "Prodotto": ["Hamburger di Manzo", "Insalata Iceberg", "Bicchieri Carta"],
    "Giacenza (colli)": [40, 15, 300],
    "Valore a Scaffale (€)": [1200, 45, 150],
    "Stato Rifornimento": ["Urgente", "Nella norma", "Eccesso"]
})

# ==========================================
# 2. st.dataframe (La tabella interattiva)
# ==========================================
st.subheader("Visione Operativa (st.dataframe)")
st.write("Questa è una tabella 'viva'. L'utente può scorrere, allargare le colonne, ordinarle cliccando sull'intestazione e scaricare i dati in CSV passando il mouse in alto a destra. Perfetta per elenchi con centinaia di righe.")

# Mostra la tabella interattiva
st.dataframe(dati_magazzino)

st.write("---")

# ==========================================
# 3. st.table (La tabella statica da report)
# ==========================================
st.subheader("Visione Report (st.table)")
st.write("Questa è una tabella statica, come quella di un documento PDF. Occupa tutto lo schermo in larghezza, non ha barre di scorrimento, l'utente non può cliccarci sopra o ordinarla. Perfetta per riepiloghi finali corti o ricevute d'ordine.")

# Mostra la tabella statica
st.table(dati_magazzino)

