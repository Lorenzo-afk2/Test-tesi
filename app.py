import streamlit as st

# Simuliamo il risultato finale del tuo algoritmo
st.subheader("Risultato Ottimizzazione")
st.metric(label="Lotto Economico Consigliato (EOQ)", value="150 cartoni")

# Utilizziamo st.caption per dare un'informazione tecnica secondaria
st.caption("📌 Nota: Il valore è stato arrotondato per eccesso al multiplo di spedizione imposto da HAVI Logistics (50 pezzi per pallet).")
st.caption("Formula teorica applicata: √(2DS/H)")

# Un altro ottimo utilizzo: indicare l'origine dei dati
st.write("---")
st.dataframe({"Prodotto": ["Carne", "Pane"], "Scorte": [45, 120]})
st.caption("Ultimo aggiornamento dati: estrazione dal gestionale di cassa del 23 Settembre.")
