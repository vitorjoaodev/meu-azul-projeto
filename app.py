#import pandas as pd

# ler arquivos
df1 = pd.read_csv("planilha1.csv")
df2 = pd.read_excel("planilha2.xlsx")

# transformar
dados1 = df1.to_dict(orient="records")
dados2 = df2.to_dict(orient="records")

# usar na lógica (ou IA)
for linha in dados1:
    print(linha)



import streamlit as st
import pandas as pd
import numpy as np
import io

st.markdown("""
<style>
div.stDownloadButton > button {
    background-color: #0066CC !important;
    color: white !important;
    position: fixed;
    bottom: 30px;
    right: 30px;
    z-index: 999;
    padding: 15px 30px;
    font-size: 18px;
    border-radius: 10px;
    border: none;
    box-shadow: 0 4px 15px rgba(0, 102, 204, 0.4);
    animation: pulse 2s infinite;
}

div.stDownloadButton > button:hover {
    background-color: #0052A3 !important;
    transform: scale(1.05);
}

@keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(0, 102, 204, 0.7); }
    70% { box-shadow: 0 0 0 15px rgba(0, 102, 204, 0); }
    100% { box-shadow: 0 0 0 0 rgba(0, 102, 204, 0); }
}
</style>
""", unsafe_allow_html=True)

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
        return pd.read_csv(arquivo, on_bad_lines='skip', encoding='latin-1', sep=';')
    elif nome.endswith(".xlsx"):
        return pd.read_excel(arquivo, engine='openpyxl')
    elif nome.endswith(".xls"):
        return pd.read_excel(arquivo, engine='xlrd')
    else:
        raise ValueError("Formato não suportado")

def extrair_timestamp(valor):
    try:
        texto = str(valor)
        if "103 " in texto:
            parte = texto.split("103 ")[1]
            if parte.endswith("108"):
                parte = parte[:-3]
            return parte
        return valor
    except:
        return valor

if arquivo_a and arquivo_b:
    try:
        df_a = ler_arquivo(arquivo_a)
        df_b = ler_arquivo(arquivo_b)
        
        st.subheader("Planilha A - Data SK")
        st.dataframe(df_a)
        
        st.subheader("Planilha B - Emissoes")
        st.dataframe(df_b)
        
        if len(df_a.columns) < 6:
            st.error(f"Planilha A precisa ter pelo menos 6 colunas (A-F). Tem apenas {len(df_a.columns)}.")
        elif len(df_b.columns) < 23:
            st.error(f"Planilha B precisa ter pelo menos 23 colunas (A-W). Tem apenas {len(df_b.columns)}.")
        else:
            col_f = df_a.columns[5]
            col_w = df_b.columns[22]
            col_l = df_b.columns[11]
            col_b = df_b.columns[1]
            col_e = df_b.columns[4]
            col_c = df_b.columns[2]
            
            st.info(f"**Etapa 1:** Coluna F ({col_f}) → Coluna W ({col_w})")
            st.info(f"**Etapa 2:** SE Coluna L ({col_l}) = 'General' → 'INTL', senão → 'DOM' na Coluna B ({col_b})")
            st.info(f"**Etapa 3:** NÚM.CARACT da Coluna E ({col_e}) → Coluna C ({col_c})")
            
            df_final = df_b.copy()
            min_len = min(len(df_a), len(df_final))
            
            valores_tratados = df_a.iloc[:min_len, 5].apply(extrair_timestamp).values
            df_final.iloc[:min_len, 22] = valores_tratados
            
            df_final.iloc[:, 1] = np.where(df_final.iloc[:, 11] == 'General', 'INTL', 'DOM')
            
            df_final.iloc[:, 2] = df_final.iloc[:, 4].astype(str).apply(len)
            
            st.subheader("Planilha Final (Resultado)")
            st.dataframe(df_final)
            
            csv = df_final.to_csv(index=False, encoding='latin-1', sep=';')
            
            baixou = st.download_button(
                label="⬇️ Baixar Planilha Final",
                data=csv,
                file_name="planilha_final.csv",
                mime="text/csv"
            )
            
            if baixou:
                st.success("Obrigado! Segurança é o nosso primeiro valor! ✈️💙")
                st.image("https://raw.githubusercontent.com/vitorjoaodev/meu-azul-projeto/main/logo.JPG", width=200)
        
    except Exception as e:
        st.error(f"Erro ao ler arquivos: {e}")
