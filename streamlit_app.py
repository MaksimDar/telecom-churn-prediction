import streamlit as st

def main():
    run_app = 'streamlit run streamlit_app.py'
    language = st.sidebar.selectbox(
        "Мова / Language",
        ["Українська", "English"],
        key="language"
    )
    
    # if "language" not in st.session_state:
    #     st.session_state.language = "Українська"

    # Define titles based on current language
    if language == "Українська":
        risk_title = "Оцінка ризиків клієнта"
        eda_title = "Дослідницький аналіз"
        models_title = "Моделі"
    else:
        risk_title = "Customer Risk Assessment"
        eda_title = "EDA"
        models_title = "Models"
    eda_page = st.Page("pages/eda.py", title=eda_title)
    models_page = st.Page("pages/models.py", title=models_title)
    customer_risk_assessment_page = st.Page("pages/customer_risk_assessment.py",title=risk_title)
    
    pg = st.navigation([eda_page,models_page,customer_risk_assessment_page])
    pg.run()

if __name__ == '__main__':
    main()