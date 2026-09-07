import streamlit as st
import keras
import joblib
import pandas as pd
from keras import models
from functions import prepare_data,predict_show_model_results

model_logistic_regression = joblib.load('models/logistic_regression/best_logistic_regression_model.pkl')

model_random_forest = joblib.load("models/random_forest/best_random_forest_model.pkl")

model_decision_tree = joblib.load('models/decision_tree/best_decision_tree_model.pkl')

model_svm = joblib.load('models/svm/best_svm_model.pkl')

model_nn = models.load_model("models/neural_network/neural_network.keras")


# language = st.sidebar.selectbox(
#     "Мова / Language",
#     ["Українська", "English"]
# )
language = st.session_state.language
if language == 'Українська':
    st.title('Оцінка ризику відтоку клієнтів')

    uploaded_file = st.file_uploader('Набір даних для інференції повинен містити  10 стовпців ознак, які використовувалися під час навчання (is_tv_subscriber, is_movie_package_subscriber, subscription_age, bill_avg, remaining_contract, service_failure_count, download_avg, upload_avg, download_over_limit, has_contract_info', type='csv')
    if uploaded_file is not None: 
        df,input_scaled = prepare_data(uploaded_file)
        model_type = st.selectbox(
            "Оберіть модель:",
            [
                "1. Випадковий ліс (Першочергова рекомендація)",
                "2. Логістична регресія",
                "3. Дерево рішень",
                "4. Метод опорних векторів (SVM)",
                "5. Нейронна мережа",
            ],)
        match(model_type):
            case "1. Випадковий ліс (Першочергова рекомендація)":
                predict_show_model_results(model_random_forest,df,input_scaled,language)
            case "2. Логістична регресія":
                predict_show_model_results(model_logistic_regression,df,input_scaled,language)
            case "3. Дерево рішень":
                predict_show_model_results(model_decision_tree,df,input_scaled,language)
            case "4. Метод опорних векторів (SVM)":
                predict_show_model_results(model_svm,df,input_scaled,language)
            case "5. Нейронна мережа":
                predict_show_model_results(model_nn,df,input_scaled,language)
    
else:
    st.title('Customer Churn Risk Assessment')

    uploaded_file = st.file_uploader('The dataset for inference must contain 10 columns of features that were used during training (is_tv_subscriber, is_movie_package_subscriber, subscription_age, bill_avg, remaining_contract, service_failure_count, download_avg, upload_avg, download_over_limit, has_contract_info', type='csv')
    if uploaded_file is not None: 
        df,input_scaled = prepare_data(uploaded_file)
        model_type = st.selectbox('Choose the model:',[
            "1. Random Forest (Top Recommendation)",
            "2. Logistic Regression",
            "3. Decision Tree",
            "4. Support Vector Machine (SVM)",
            "5. Neural Network",
        ],)
        match(model_type):
            case "1. Random Forest (Top Recommendation)":
                predict_show_model_results(model_random_forest,df,input_scaled,language)
            case "2. Logistic Regression":
                predict_show_model_results(model_logistic_regression,df,input_scaled,language)
            case "3. Decision Tree":
                predict_show_model_results(model_decision_tree,df,input_scaled,language)
            case "4. Support Vector Machine (SVM)":
                predict_show_model_results(model_svm,df,input_scaled,language)
            case "5. Neural Network":
                predict_show_model_results(model_nn,df,input_scaled,language)