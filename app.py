import streamlit as st
import pandas as pd
import io

st.title("Transferência de Planilhas")

arquivo_a = st.file_uploader("📎 Suba a Planilha A aqui", type=["csv", "xls", "xlsx"])
arquivo_b = st.file_uploader("📎 Suba a Planilha B aqui", type=["csv", "xls", "xlsx"])

def ler_arquivo(arquivo):
    nome = arquivo.name.lower()
    if nome.endswith(".csv"):
        try:
            return pd.read_csv(arquivo, encoding="utf-8", sep=",")
        except:
            return pd.read_csv(arquivo, encoding="latin1", sep=";")
    elif nome.endswith(".xlsx"):
        try:
            return pd.read_excel(arquivo, engine="openpyxl")
        except:
            try:
                return pd.read_csv(arquivo, encoding="utf-8", sep=",")
            except:
                return pd.read_csv(arquivo, encoding="latin1", sep=";")
    else:
        try:
            return pd.read_excel(arquivo, engine="xlrd")
        except:
            try:
                return pd.read_csv(arquivo, encoding="utf-8", sep=",")
            except:
                return pd.read_csv(arquivo, encoding="latin1", sep=";")

if arquivo_a and arquivo_b:
    df_a = ler_arquivo(arquivo_a)
    df_b = ler_arquivo(arquivo_b)

    # Mostra preview
    st.write("👀 Preview Planilha A:")
    st.dataframe(df_a.head(3))

    st.write("👀 Preview Planilha B:")
    st.dataframe(df_b.head(3))

    # Mostra quantas colunas cada uma tem
    st.info(f"Planilha A tem {len(df_a.columns)} colunas")
    st.info(f"Planilha B tem {len(df_b.columns)} colunas")

    # Cria coluna D se não existir
    while len(df_b.columns) < 4:
        df_b[f"coluna_nova_{len(df_b.columns)}"] = None

    # Coluna A de A vai para coluna D de B (respeitando o menor tamanho)
    min_linhas = min(len(df_a), len(df_b))
    df_b.iloc[:min_linhas, 3] = df_a.iloc[:min_linhas, 0].values

    output = io.StringIO()
    df_b.to_csv(output, index=False)

    st.success("✅ Dados transferidos!")

    st.download_button(
        label="⬇️ Baixar Planilha B preenchida",
        data=output.getvalue(),
        file_name="planilha_b_preenchida.csv",
        mime="text/csv"
    )
