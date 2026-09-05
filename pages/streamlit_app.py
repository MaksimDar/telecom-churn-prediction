import streamlit as st

run_app = 'streamlit run streamlit_app.py'

eda_page = st.Page("eda.py", title="eda")
models_page = st.Page("models.py", title="models")

pg = st.navigation([eda_page,models_page])
pg.run()