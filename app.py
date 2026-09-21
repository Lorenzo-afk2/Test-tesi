import streamlit as st
import math

st.title("Calcolatore EOQ Semplificato")

# L'utente inserisce i dati
domanda = st.number_input("Domanda annua:", value=1000)
costo_s = st.number_input("Costo ordine (€):", value=50)
costo_h = st.number_input("Costo mantenimento (€):", value=2.5)

# Il blocco del pulsante
if st.button("Calcola l'Ordine Perfetto"):
    
    # Questo codice (rientrato) parte SOLO se premo il pulsante
    risultato = math.sqrt((2 * domanda * costo_s) / costo_h)
    
    # st.success è come st.write, ma disegna un bel box verde!
    st.success(f"Dovresti ordinare {round(risultato)} pezzi alla volta.")
