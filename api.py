from fastapi import FastAPI
import pandas as pd

app = FastAPI(title="ClinOmics AI Backend")

# Load and normalize CSVs
expression_df = pd.read_csv("expression.csv")
mutation_df = pd.read_csv("mutations.csv")
drug_df = pd.read_csv("dgidb_drugs.csv")

# Normalize gene column
mutation_df["Gene"] = mutation_df["Gene"].str.upper()
drug_df["Gene"] = drug_df["Gene"].str.upper()

@app.get("/")
def root():
    return {"message": "ClinOmics AI API is running"}

@app.get("/expression/{gene}")
def get_expression(gene: str):
    gene = gene.upper()
    row = expression_df[expression_df["Gene"].str.upper() == gene]
    if row.empty:
        return {"error": "No expression data"}
    return {
        "gene": gene,
        "normal_tpm": row.iloc[0]["Normal_TPM"],
        "tumor_tpm": row.iloc[0]["Tumor_TPM"]
    }

@app.get("/mutation/{gene}")
def get_mutation(gene: str):
    gene = gene.upper()
    result = mutation_df[mutation_df["Gene"] == gene]
    if result.empty:
        return []
    return result.to_dict(orient="records")

@app.get("/drug/{gene}")
def get_drugs(gene: str):
    gene = gene.upper()
    result = drug_df[drug_df["Gene"] == gene]
    if result.empty:
        return []
    return result[["Drug", "Interaction"]].to_dict(orient="records")
