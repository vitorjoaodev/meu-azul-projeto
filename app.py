from __future__ import annotations

from typing import Final

import streamlit as st
import pandas as pd
import numpy as np
import io

MIN_COLS_A: Final[int] = 6
MIN_COLS_B: Final[int] = 23
IDX_COL_F: Final[int] = 5
IDX_COL_W: Final[int] = 22
IDX_COL_L: Final[int] = 11
IDX_COL_B: Final[int] = 1
IDX_COL_E: Final[int] = 4
IDX_COL_C: Final[int] = 2
MARKER: Final[str] = "103 "
SUFFIX: Final[str] = "108"
GENERAL_LABEL: Final[str] = "General"
INTL_LABEL: Final[str] = "INTL"
DOM_LABEL: Final[str] = "DOM"

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

st.title("Transferência de Planilhas - Operações de Solo Safety - BRIOU")
st.markdown("""
Siga as instruções abaixo, tripulante:

1. Faça o upload da planilha "A" primeiro e, em seguida, da planilha "B", ambas no formato CSV.
2. Aguarde o carregamento completo dos arquivos.
3. Quando aparecer a mensagem confirmando o carregamento das planilhas, clique no botão flutuante azul abaixo para baixar sua planilha.

**#oceuéazul** ✈️💙
""")

st.image("https://raw.githubusercontent.com/vitorjoaodev/meu-azul-projeto/main/logo.JPG", width=200)

arquivo_a: st.runtime.uploaded_file_manager.UploadedFile | None = st.file_uploader(
    "📎 Suba a Planilha A (Data SK)", type=["csv", "xls", "xlsx"]
)
arquivo_b: st.runtime.uploaded_file_manager.UploadedFile | None = st.file_uploader(
    "📎 Suba a Planilha B (Emissões)", type=["csv", "xls", "xlsx"]
)


def _detectar_separador(primeira_linha: str) -> str:
    if ";" in primeira_linha:
        return ";"
    if "\t" in primeira_linha:
        return "\t"
    return ","


def _ler_csv(arquivo: st.runtime.uploaded_file_manager.UploadedFile) -> pd.DataFrame:
    raw: bytes = arquivo.read()
    arquivo.seek(0)
    try:
        conteudo: str = raw.decode("utf-8")
    except UnicodeDecodeError:
        conteudo = raw.decode("latin-1", errors="replace")

    sep: str = _detectar_separador(conteudo.split("\n")[0])

    try:
        df: pd.DataFrame = pd.read_csv(arquivo, sep=sep, on_bad_lines="skip", encoding="utf-8")
    except UnicodeDecodeError:
        arquivo.seek(0)
        df = pd.read_csv(arquivo, sep=sep, on_bad_lines="skip", encoding="latin-1")
    return df


def ler_arquivo(arquivo: st.runtime.uploaded_file_manager.UploadedFile) -> pd.DataFrame:
    nome: str = arquivo.name.lower()
    if nome.endswith(".csv"):
        return _ler_csv(arquivo)
    if nome.endswith(".xlsx"):
        return pd.read_excel(arquivo, engine="openpyxl")
    if nome.endswith(".xls"):
        return pd.read_excel(arquivo, engine="xlrd")
    raise ValueError(f"Formato não suportado: {nome}")


def extrair_timestamp(valor: object) -> object:
    texto: str = str(valor)
    if MARKER not in texto:
        return valor
    parte: str = texto.split(MARKER, maxsplit=1)[1]
    if parte.endswith(SUFFIX):
        parte = parte[: -len(SUFFIX)]
    return parte


def _validar_colunas(df_a: pd.DataFrame, df_b: pd.DataFrame) -> bool:
    if len(df_a.columns) < MIN_COLS_A:
        st.error(
            f"Planilha A precisa ter pelo menos {MIN_COLS_A} colunas (A-F). "
            f"Tem apenas {len(df_a.columns)}."
        )
        st.write("Colunas encontradas:", list(df_a.columns))
        return False
    if len(df_b.columns) < MIN_COLS_B:
        st.error(
            f"Planilha B precisa ter pelo menos {MIN_COLS_B} colunas (A-W). "
            f"Tem apenas {len(df_b.columns)}."
        )
        st.write("Colunas encontradas:", list(df_b.columns))
        return False
    return True


def _processar(df_a: pd.DataFrame, df_b: pd.DataFrame) -> pd.DataFrame:
    col_f: str = str(df_a.columns[IDX_COL_F])
    col_w: str = str(df_b.columns[IDX_COL_W])
    col_l: str = str(df_b.columns[IDX_COL_L])
    col_b: str = str(df_b.columns[IDX_COL_B])
    col_e: str = str(df_b.columns[IDX_COL_E])
    col_c: str = str(df_b.columns[IDX_COL_C])

    st.info(f"**Etapa 1:** Coluna F da A (`{col_f}`) → Coluna W da B (`{col_w}`)")
    st.info(f"**Etapa 2:** SE Coluna L (`{col_l}`) = 'General' → 'INTL', senão → 'DOM' na Coluna B (`{col_b}`)")
    st.info(f"**Etapa 3:** NÚM.CARACT da Coluna E (`{col_e}`) → Coluna C (`{col_c}`)")

    df_final: pd.DataFrame = df_b.copy()
    min_len: int = min(len(df_a), len(df_final))

    valores_tratados: np.ndarray = df_a.iloc[:min_len, IDX_COL_F].apply(extrair_timestamp).values
    df_final.iloc[:min_len, IDX_COL_W] = valores_tratados

    col_l_valores: pd.Series[str] = df_final.iloc[:, IDX_COL_L].astype(str).str.strip()
    df_final.iloc[:, IDX_COL_B] = np.where(col_l_valores == GENERAL_LABEL, INTL_LABEL, DOM_LABEL)

    df_final.iloc[:, IDX_COL_C] = df_final.iloc[:, IDX_COL_E].astype(str).apply(len)

    return df_final


if arquivo_a is not None and arquivo_b is not None:
    try:
        df_a: pd.DataFrame = ler_arquivo(arquivo_a)
        df_b: pd.DataFrame = ler_arquivo(arquivo_b)

        st.subheader("Planilha A - Data SK")
        st.write(f"Linhas: {len(df_a)} | Colunas: {len(df_a.columns)}")
        st.dataframe(df_a)

        st.subheader("Planilha B - Emissões")
        st.write(f"Linhas: {len(df_b)} | Colunas: {len(df_b.columns)}")
        st.dataframe(df_b)

        if _validar_colunas(df_a, df_b):
            df_final: pd.DataFrame = _processar(df_a, df_b)

            st.subheader("Planilha Final (Resultado)")
            st.write(f"Linhas: {len(df_final)} | Colunas: {len(df_final.columns)}")
            st.dataframe(df_final)

            csv: str = df_final.to_csv(index=False, encoding="latin-1", sep=";")

            baixou: bool = st.download_button(
                label="⬇️ Baixar Planilha Final",
                data=csv,
                file_name="planilha_final.csv",
                mime="text/csv",
            )

            if baixou:
                st.success("Obrigado! Segurança é o nosso primeiro valor! ✈️💙")
                st.image("https://raw.githubusercontent.com/vitorjoaodev/meu-azul-projeto/main/logo.JPG", width=200)

    except Exception as e:
        st.error(f"Erro ao ler arquivos: {e}")
        import traceback
        st.code(traceback.format_exc())
