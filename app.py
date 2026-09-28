import streamlit as st

# 1. Inizializziamo la "memoria" dell'app
# Se è la prima volta che l'utente apre la pagina, impostiamo l'accesso a False
if "autenticato" not in st.session_state:
    st.session_state["autenticato"] = False

# ==========================================
# SCHERMATA DI LOGIN
# ==========================================
if st.session_state["autenticato"] == False:
    st.title("🔒 Accesso Area Riservata")
    st.write("Inserisci le credenziali per accedere al sistema ordini HAVI.")
    
    # Creiamo i campi di input
    username = st.text_input("Nome Utente")
    # type="password" nasconde il testo digitato sostituendolo con dei pallini neri
    password = st.text_input("Password", type="password")
    
    if st.button("Accedi"):
        # Controlliamo se le credenziali sono corrette (qui usiamo admin / mcdonalds2024)
        if username == "admin" and password == "mcdonalds2024":
            st.session_state["autenticato"] = True # Salviamo in memoria che l'utente è loggato
            st.rerun() # Ricarica la pagina istantaneamente per mostrare l'app
        else:
            # Se sbaglia, mostriamo l'errore esatto che mi hai chiesto
            st.error("Credenziali errate. Riprova.")

# ==========================================
# APPLICAZIONE VERA E PROPRIA (Protetta)
# ==========================================
if st.session_state["autenticato"] == True:
    st.title("🍔 Dashboard Ordini HAVI")
    st.success("Accesso effettuato con successo. Benvenuto Direttore!")
    
    st.header("Nuovo Ordine")
    st.selectbox("Seleziona Prodotto", ["Hamburger di Manzo", "Patatine", "Coca-Cola"])
    st.number_input("Quantità (Cartoni)", min_value=1)
    
    st.button("Invia Ordine")
    
    st.write("---")
    # Tasto per uscire (Logout)
    if st.button("Esci (Logout)"):
        st.session_state["autenticato"] = False # Cancelliamo l'accesso dalla memoria
        st.rerun() # Ricarica la pagina tornando al login
