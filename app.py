import streamlit as st

st.title("Ottimizzazione Scorte (EOQ)")
st.write("Benvenuto nel sistema di calcolo logistico.")

st.divider() # <--- Prima riga per separare l'intestazione

# --- ZONA INPUT ---
st.subheader("1. Inserimento Dati")
st.file_uploader("Carica Storico Vendite", type=["csv"])

st.write("---") # <--- Seconda riga per separare gli input dai risultati

# --- ZONA OUTPUT ---
st.subheader("2. Risultati Calcolati")
st.metric(label="Lotto Economico (EOQ)", value="150 colli")



