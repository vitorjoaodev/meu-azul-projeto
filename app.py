import streamlit as st
import pandas as pd
import io

st.title("Transferência de Planilhas")

# Campo 1 - Planilha A
arquivo_a = st.file_uploader("📎 Suba a Planilha A aqui", type=["csv"])

# Campo 2 - Planilha B
arquivo_b = st.file_uploader("📎 Suba a Planilha B aqui", type=["csv"])

if arquivo_a and arquivo_b:
    # Lê os dois CSVs
    df_a = pd.read_csv(arquivo_a)
    df_b = pd.read_csv(arquivo_b)

    # Pega coluna A da planilha A (primeira coluna)
    # e joga na coluna D da planilha B (quarta coluna)
    df_b.iloc[:, 3] = df_a.iloc[:, 0].values

    # Gera o arquivo para baixar
    output = io.StringIO()
    df_b.to_csv(output, index=False)

    st.success("✅ Dados transferidos com sucesso!")

    st.download_button(
        label="⬇️ Baixar Planilha B preenchida",
        data=output.getvalue(),
        file_name="planilha_b_preenchida.csv",
        mime="text/csv"
    )
