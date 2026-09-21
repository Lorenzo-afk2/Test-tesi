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


# Titolo della pagina di test
st.title("Test Menu a Tendina per la Tesi")

# Creazione del menu a tendina
scelta_livello = st.selectbox(
    "Seleziona il Livello di Servizio (Rischio rottura di stock):",
    ["90% (Standard base)", "95% (Standard medio)", "99% (Alta priorità)"]
)

# Output dinamico in base alla scelta
st.write(f"Il sistema imposterà i calcoli basandosi su: **{scelta_livello}**")

# Esempio di logica collegata (come funzionerà nel tuo software)
if "90%" in scelta_livello:
    st.info("Valore Z applicato: 1.28")
elif "95%" in scelta_livello:
    st.info("Valore Z applicato: 1.65")
else:
    st.info("Valore Z applicato: 2.33 (Scorta di sicurezza massima)")


