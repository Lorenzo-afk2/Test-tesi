import streamlit as st

st.title("Test Colori e Dimensioni")

# 1. Metodo Standard (Il modo in cui Streamlit VUOLE che tu faccia)
st.write("Questo è il testo normale.")
st.write("Questo è in **grassetto**.")

st.divider()

# 2. Il trucco dell'HTML (Per colori specifici e dimensioni personalizzate)
# Devi usare st.markdown e impostare unsafe_allow_html=True
st.markdown(
    """
    <p style='color: #004D40; font-size: 28px; font-weight: bold;'>
        Questo testo è Verde Scuro, gigante e in grassetto!
    </p>
    """, 
    unsafe_allow_html=True
)

st.markdown(
    """
    <p style='color: red; font-size: 14px;'>
        Questo testo è rosso e piccolo per un avviso.
    </p>
    """, 
    unsafe_allow_html=True
)



