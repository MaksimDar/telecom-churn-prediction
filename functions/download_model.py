import streamlit as st

def download_model(model_direction,label,filename): 
    with open(model_direction, "rb") as file:
        st.download_button(
            label=label,
            data=file,
            file_name=filename,
            mime="application/octet-stream",
        )