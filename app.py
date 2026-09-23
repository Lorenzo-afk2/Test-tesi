import streamlit as st

st.title("Impostazioni Parametri per Categoria")

# 1. Creazione del menu a tendina
categoria = st.selectbox(
    "Seleziona la Categoria del Prodotto:",
    ["Scegli un'opzione...", "Congelato (Es. Hamburger)", "Fresco (Es. Insalata)","Secco (Es. Bicchieri)"]
)

# 2. Logica condizionale (if/elif)
# Se l'utente non ha ancora scelto nulla, mostriamo un messaggio
if categoria == "Scegli un'opzione...":
    st.info("Seleziona una categoria per visualizzare i parametri logistici associati.")


# Se seleziona "Congelato"
elif categoria == "Congelato (Es. Hamburger)":
    st.write("### Parametri Operativi - Cella Negativa")
    # Costo mantenimento altissimo (consumo elettrico)
    costo_mantenimento = st.number_input("Costo di Mantenimento (H) €", value=8.00, min_value=0.0)
    # Livello di servizio massimo (prodotto vitale)
    livello_servizio = st.selectbox("Livello di Servizio Desiderato:", ["95%", "99%", "99.9% (Consigliato)"], index=2)
    
    st.error("Prodotto Core: La rottura di stock non è tollerata. Verrà applicato il Safety Stock massimo (Z=3.09).")



# Se seleziona "Fresco"
elif categoria == "Fresco (Es. Insalata)":
    st.write("### Parametri Operativi - Reparto Fresco")
    # Costo di mantenimento alto (rischio scadenza)
    costo_mantenimento = st.number_input("Costo di Mantenimento (H) €", value=4.50, min_value=0.0)
    # Livello di servizio medio (se finisce l'insalata non è tragico come finire la carne)
    livello_servizio = st.selectbox("Livello di Servizio Desiderato:", ["90%", "95%", "98%"], index=1)
    
    st.warning("Attenzione: I prodotti freschi hanno un alto rischio di obsolescenza. L'algoritmo terrà l'EOQ molto basso.")


# Se seleziona "Secco"
elif categoria == "Secco (Es. Bicchieri)":
    st.write("### Parametri Operativi - Magazzino Ambiente")
    # Costo mantenimento basso (occupano solo spazio)
    costo_mantenimento = st.number_input("Costo di Mantenimento (H) €", value=0.50, min_value=0.0)
    # Livello di servizio standard
    livello_servizio = st.selectbox("Livello di Servizio Desiderato:", ["90%", "95%", "99%"], index=0)
    
    st.success("Prodotti stabili. L'algoritmo ottimizzerà per lotti di grandi dimensioni al fine di ridurre i costi di spedizione.")

# --- ESEMPIO DI STAMPA DEI VALORI (per verificare che funzioni) ---
if categoria != "Scegli un'opzione...":
    st.markdown("---")
    st.write("Le variabili salvate in memoria per la formula sono:")
    st.write(f"- Valore **H**: {costo_mantenimento} €")
    st.write(f"- Valore **Servizio**: {livello_servizio}")


