import streamlit as st

# La parola chiave type accetta una lista di formati
file_dati = st.file_uploader(
    "Carica lo storico vendite:", 
    type=["csv", "xlsx", "xls"]
)



