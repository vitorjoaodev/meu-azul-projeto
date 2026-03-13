import streamlit as st
import pandas as pd
import io

st.title("Transferência de Planilhas")

arquivo_a = st.file_uploader("📎 Suba a Planilha A aqui", type=["csv"])
arquivo_b = st.file_uploader("📎 Suba a Planilha B aqui", type=["csv"])

if arquivo_a and arquivo_b:
    try:
        # Tenta ler com separador vírgula
        df_a = pd.read_csv(arquivo_a, encoding="utf-8", sep=",")
    except:
        try:
            # Tenta com ponto e vírgula
            df_a = pd.read_csv(arquivo_a, encoding="latin1", sep=";")
        except:
            st.error("❌ Erro ao ler Planilha A")
            st.stop()

    try:
        df_b = pd.read_csv(arquivo_b, encoding="utf-8", sep=",")
    except:
        try:
            df_b = pd.read_csv(arquivo_b, encoding="latin1", sep=";")
        except:
            st.error("❌ Erro ao ler Planilha B")
            st.stop()

    # Mostra preview das planilhas
    st.write("👀 Preview Planilha A:")
    st.dataframe(df_a.head(3))

    st.write("👀 Preview Planilha B:")
    st.dataframe(df_b.head(3))

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
