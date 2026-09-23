import streamlit as st

st.header("📦 Aggiunta Nuovo Prodotto al Database")

# 1. st.text_input (Testo libero)
# Perfetto per far digitare nomi, codici a barre o descrizioni
nome_prodotto = st.text_input("Nome del nuovo prodotto:", placeholder="Es. Nuova Salsa Barbecue")

# 2. st.multiselect (Scelta multipla)
# A differenza della selectbox, qui l'utente può cliccare più di una voce
zone_stoccaggio = st.multiselect(
    "In quali zone può essere stoccato?",
    ["Cella Frigo Positiva (Fresco)", "Cella Frigo Negativa (Surgelato)", "Magazzino (Secco)"]
)

# 3. st.number_input (Inserimento numeri esatti)
# Usiamo i parametri min_value e step per controllare i tastini + e -
costo_unitario = st.number_input("Costo d'acquisto per collo (€):", min_value=0.0, step=0.50)

# 4. st.slider (Barra a scorrimento)
# Ottimo per percentuali o range visivi (da 80 a 100 in questo caso)
livello_servizio = st.slider("Livello di Servizio Desiderato (%):", min_value=80, max_value=100, value=95)

st.write("---")

# 5. st.button (Pulsante di azione)
# Tutto ciò che è indentato sotto l'if viene eseguito SOLO quando l'utente clicca il bottone
if st.button("Salva Prodotto nel Sistema"):
    
    # Facciamo un piccolo controllo di sicurezza: ha inserito il nome?
    if nome_prodotto == "":
        st.error("Errore: Devi inserire il nome del prodotto prima di salvare!")
    else:
        st.success(f"✅ Il prodotto '{nome_prodotto}' è stato registrato con successo!")
        
        # Mostriamo il riepilogo di ciò che ha inserito usando st.write
        st.write("**Riepilogo dati inseriti:**")
        st.write(f"- Costo: {costo_unitario} €")
        st.write(f"- Livello servizio: {livello_servizio} %")
        st.write(f"- Zone autorizzate: {zone_stoccaggio}")
