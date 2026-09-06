import pandas as pd
import streamlit as st
import joblib


def prepare_data(uploaded_file):
    scaler = joblib.load('models/scaler/scaler.pkl')
    df = pd.read_csv(uploaded_file)
    
    duplications_amount = df.duplicated().sum()
    if duplications_amount > 0:
        df = df.drop_duplicates()
    
    df['has_contract_info'] =  df['remaining_contract'].notna().astype(int)
    df['remaining_contract'] = df['remaining_contract'].fillna(0)
    df['has_active_contract'] = (df['remaining_contract'] > 0).astype(int)
    
    if 'id' in df.columns:
        df = df.drop(columns=['id'])
    st.write(df)
    df_clean = df.fillna(df.median())
    expected_columns = ['is_tv_subscriber', 'is_movie_package_subscriber', 'subscription_age','bill_avg', 'remaining_contract', 'service_failure_count','download_avg', 'upload_avg', 'download_over_limit','has_contract_info', 'has_active_contract']
    df_clean = df_clean[expected_columns] 
    input_scaled = scaler.transform(df_clean)  
    return df_clean,input_scaled