import streamlit as st
import pandas as pd
import io

st.title("Transferência de Planilhas - Operações de Solo Safety")
st.markdown("""
Siga as instruções abaixo, tripulante:

1. Faça o upload da planilha "A" primeiro e, em seguida, da planilha "B", ambas no formato CSV.
2. Aguarde o carregamento completo dos arquivos.
3. Quando aparecer a mensagem confirmando o carregamento das planilhas, clique no botão flutuante azul abaixo para baixar sua planilha.

**#oceuéazul** ✈️💙
""")

st.image("https://raw.githubusercontent.com/vitorjoaodev/meu-azul-projeto/main/logo.JPG", width=200)

arquivo_a = st.file_uploader("📎 Suba a Planilha A (Data SK.csv)", type=["csv", "xls", "xlsx"])
arquivo_b = st.file_uploader("📎 Suba a Planilha B (emissoes.csv)", type=["csv", "xls", "xlsx"])

def ler_arquivo(arquivo):
    nome = arquivo.name.lower()
    if nome.endswith(".csv"):
        return pd.read_csv(arquivo, on_bad_lines='skip', encoding='latin-1', sep=None, engine='python')
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
        
        st.subheader("Planilha A - Data SK")
        st.dataframe(df_a)
        
        st.subheader("Planilha B - Emissoes")
        st.dataframe(df_b)
        
        if len(df_a.columns) < 1:
            st.error("Planilha A não tem colunas suficientes!")
        elif len(df_b.columns) < 4:
            st.error(f"Planilha B tem apenas {len(df_b.columns)} coluna(s). Precisa ter pelo menos 4 colunas (A, B, C, D).")
            st.warning(f"Colunas disponíveis na Planilha B: {list(df_b.columns)}")
        else:
            col_a = df_a.columns[0]
            col_d = df_b.columns[3]
            
            st.info(f"Coluna A da Planilha A: **{col_a}** → Coluna D da Planilha B: **{col_d}**")
            
            df_final = df_b.copy()
            min_len = min(len(df_a), len(df_final))
            df_final.iloc[:min_len, 3] = df_a.iloc[:min_len, 0].values
            
            st.subheader("Planilha Final (Resultado)")
            st.dataframe(df_final)
            
            csv = df_final.to_csv(index=False, encoding='latin-1')
            
            baixou = st.download_button(
                label="⬇️ Baixar Planilha Final",
                data=csv,
                file_name="planilha_final.csv",
                mime="text/csv",
                type="primary"
            )
            
            if baixou:
                st.success("Obrigado!")
                st.image("https://raw.githubusercontent.com/vitorjoaodev/meu-azul-projeto/main/logo.JPG", width=200)
        
    except Exception as e:
        st.error(f"Erro ao ler arquivos: {e}")
