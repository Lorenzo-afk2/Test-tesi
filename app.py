import streamlit as st

# (Codice precedente: st.set_page_config e inizializzazione session_state)

if not st.session_state["autenticato"]:
    
    # 1. INIEZIONE DELLO SFONDO DINAMICO (CSS)
    # Creiamo un gradiente che sfuma tra grigio scuro, nero e il rosso McDonald's
    sfondo_dinamico = """
    <style>
    .stApp {
        background: linear-gradient(-45deg, #1a1a1a, #2c3e50, #8b0000, #DA291C);
        background-size: 400% 400%;
        animation: movimento_sfondo 15s ease infinite;
    }
    
    @keyframes movimento_sfondo {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Rende la Card di login leggermente trasparente per un effetto "Vetro" (Glassmorphism) */
    [data-testid="stVerticalBlock"] > div > div {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 20px;
    }
    </style>
    """
    st.markdown(sfondo_dinamico, unsafe_allow_html=True)
    
    # 2. IL TUO MODULO DI LOGIN
    spazio_sx, col_centro, spazio_dx = st.columns([1, 2, 1])
    with col_centro:
        with st.container(border=True):
            st.markdown("<h2 style='text-align: center; color: #DA291C;'>Area Riservata HAVI</h2>", unsafe_allow_html=True)
            # ... resto del form di login (text_input, button, ecc.) ...

