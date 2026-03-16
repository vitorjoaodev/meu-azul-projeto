
#alteração: min_linhas = min(len(df_a), len(df_b))
df_b.iloc[:min_linhas, 3] = df_a.iloc[:min_linhas, 0].values

import streamlit as st
import pandas as pd
import io

st.title("Transferência de Planilhas")

arquivo_a = st.file_uploader("📎 Suba a Planilha A aqui", type=["csv"])
arquivo_b = st.file_uploader("📎 Suba a Planilha B aqui", type=["csv"])

if arquivo_a and arquivo_b:
    try:
        df_a = pd.read_csv(arquivo_a, encoding="utf-8", sep=",")
    except:
        df_a = pd.read_csv(arquivo_a, encoding="latin1", sep=";")

    try:
        df_b = pd.read_csv(arquivo_b, encoding="utf-8", sep=",")
    except:
        df_b = pd.read_csv(arquivo_b, encoding="latin1", sep=";")

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

    # Coluna A de A vai para coluna D de B
    df_b.iloc[:, 3] = df_a.iloc[:, 0].values

    output = io.StringIO()
    df_b.to_csv(output, index=False)

    st.success("✅ Dados transferidos!")

    st.download_button(
        label="⬇️ Baixar Planilha B preenchida",
        data=output.getvalue(),
        file_name="planilha_b_preenchida.csv",
        mime="text/csv"
    )
