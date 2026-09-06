import streamlit as st

def predict_show_model_results(model,df,input_scaled,language):
       
    if hasattr(model, 'predict_proba'):
        predictions = model.predict(input_scaled)
        probabilities = model.predict_proba(input_scaled)[:, 1]  
    else:
        raw_preds = model.predict(input_scaled).flatten()
        probabilities = raw_preds
        predictions = (probabilities >= 0.5).astype(int)

    results_df = df.copy()
    if language == 'Українська':
        lang_dict = ['Ймовірність відтоку (%)', 'Результат','Висока ймовірність відтоку','Низька ймовірність відтоку',"### Результати прогнозування","Відсоток потенційного відтоку від усіх клієнтів становить"]
    else:
        lang_dict = ['Churn Probability (%)', 'Result','High churn probability','Low churn probability',"### Prediction Results","The percentage of potential churn across all customers is"]
    results_df[lang_dict[0]] = (probabilities * 100).round(2)
    results_df[lang_dict[1]] = [lang_dict[2] if p == 1 else lang_dict[3] for p in predictions]

    st.write(lang_dict[4])
    st.dataframe(results_df[[lang_dict[1], lang_dict[0]]])
    mean_value = round(results_df[lang_dict[0]].mean(),2)
    st.write(f'{lang_dict[5]} {mean_value}%')