import streamlit as st

run_app = 'streamlit run streamlit_app.py'

eda_page = st.Page("pages/eda.py", title="eda")
models_page = st.Page("pages/models.py", title="models")
customer_risk_assessment_page = st.Page("pages/customer_risk_assessment.py", title="customer_risk_assessment")

pg = st.navigation([eda_page,models_page,customer_risk_assessment_page])
pg.run()