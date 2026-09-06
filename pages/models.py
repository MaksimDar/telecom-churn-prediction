import streamlit as st

language = st.sidebar.selectbox(
    "Мова / Language",
    ["Українська", "English"]
)

if language == "Українська":
    st.title('Розроблені моделі')
else:
    st.title('Developed models')
