import streamlit as st
import requests

API_URL = "https://clinomicsai-pro.onrender.com"

st.set_page_config(page_title="ClinOmics AI")
st.title("🧬 ClinOmics AI - Gene Insight")

gene = st.text_input("Enter Gene Symbol (e.g., TP53):")

if st.button("Analyze") and gene:
    try:
        expr = requests.get(f"{API_URL}/expression/{gene}", timeout=5).json()
        st.subheader("Gene Expression")
        st.json(expr)
    except Exception as e:
        st.error(f"API Error: {e}")
