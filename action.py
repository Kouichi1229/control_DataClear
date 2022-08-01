import streamlit as st

encoding='utf-8-sig'
@st.cache
def convert_df(df):
# IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode(encoding)