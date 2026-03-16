import streamlit as st
import pandas as pd
import io

st.title("Transferência de Planilhas")

arquivo_a = st.file_uploader("📎 Suba a Planilha A aqui", type=["csv", "xls", "xlsx"])
arquivo_b = st.file_uploader("📎 Suba a Planilha B aqui", type=["csv", "xls", "xlsx"])

def ler_arquivo(arquivo):
    nome = arquivo.name.lower()
    if nome.endswith(".csv"):
        return pd.read_csv(arquivo)
    elif nome.endswith(".xlsx"):
        return pd.read_excel(arquivo, engine='openpyxl')
    elif nome.endswith(".xls"):
        return pd.read_excel(arquivo, engine='xlrd')
    else:
        raise ValueError("Formato não suportado")

if arquivo_a and arquivo_b:
    try:
        df_a = ler_arquivo(arquivo_a)
        df_b = ler_arquivo(arquivo_b)
        
        st.subheader("Planilha A")
        st.dataframe(df_a)
        
        st.subheader("Planilha B")
        st.dataframe(df_b)
        
    except Exception as e:
        st.error(f"Erro ao ler arquivos: {e}")
