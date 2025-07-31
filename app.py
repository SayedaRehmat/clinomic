import streamlit as st
import requests
import pandas as pd

API_URL = "https://clinomicsai-pro.onrender.com"

st.set_page_config(page_title="ClinOmics AI Pro", page_icon="🧬", layout="centered")
st.title("🔬 ClinOmics AI Pro")

st.markdown("""
Enter a gene symbol (e.g., **TP53**, **BRCA1**) to explore:
- 🧬 Gene Expression Levels
- 🔎 Mutations
- 💊 Drug Matches
""")

gene = st.text_input("Gene Symbol", placeholder="e.g., TP53")

if st.button("Analyze") and gene:
    with st.spinner("Fetching data from backend API..."):
        try:
            expr = requests.get(f"{API_URL}/expression/{gene}", timeout=20).json()
            muts = requests.get(f"{API_URL}/mutation/{gene}", timeout=20).json()
            drugs = requests.get(f"{API_URL}/drug/{gene}", timeout=20).json()

        except requests.exceptions.Timeout:
            st.warning("⏱ API timed out — server may be cold-starting. Try again shortly.")
            st.stop()
        except Exception as e:
            st.error(f"API Error: {e}")
            st.stop()

    # ------------------- Expression -------------------
    if expr and "normal_tpm" in expr and "tumor_tpm" in expr:
        st.subheader("🧬 Expression Levels")
        expr_df = pd.DataFrame({
            "Type": ["Normal", "Tumor"],
            "TPM": [expr["normal_tpm"], expr["tumor_tpm"]]
        })
        st.table(expr_df)
    else:
        st.warning("No expression data found.")

    # ------------------- Mutations -------------------
    if muts and isinstance(muts, list) and len(muts) > 0 and "error" not in muts[0]:
        st.subheader("🔎 Mutation Info")
        st.table(pd.DataFrame(muts))
    else:
        st.warning("No mutation data found.")

    # ------------------- Drug Matches -------------------
    if drugs and isinstance(drugs, list) and len(drugs) > 0 and "error" not in drugs[0]:
        st.subheader("💊 Drug Matches")
        st.table(pd.DataFrame(drugs))
    else:
        st.warning("No drug matches found.")
