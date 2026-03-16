#zipfile.BadZipFile: This app has encountered an error. The original error message is redacted to prevent data leaks. Full error details have been recorded in the logs (if you're on Streamlit Cloud, click on 'Manage app' in the lower right of your app).
Traceback:
File "/mount/src/meu-azul-projeto/app.py", line 23, in <module>
    df_a = ler_arquivo(arquivo_a)
File "/mount/src/meu-azul-projeto/app.py", line 18, in ler_arquivo
    return pd.read_excel(arquivo, engine="openpyxl")
           ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.14/site-packages/pandas/io/excel/_base.py", line 495, in read_excel
    io = ExcelFile(
        io,
    ...<2 lines>...
        engine_kwargs=engine_kwargs,
    )
File "/home/adminuser/venv/lib/python3.14/site-packages/pandas/io/excel/_base.py", line 1567, in __init__
    self._reader = self._engines[engine](
                   ~~~~~~~~~~~~~~~~~~~~~^
        self._io,
        ^^^^^^^^^
        storage_options=storage_options,
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        engine_kwargs=engine_kwargs,
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
File "/home/adminuser/venv/lib/python3.14/site-packages/pandas/io/excel/_openpyxl.py", line 553, in __init__
    super().__init__(
    ~~~~~~~~~~~~~~~~^
        filepath_or_buffer,
        ^^^^^^^^^^^^^^^^^^^
        storage_options=storage_options,
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        engine_kwargs=engine_kwargs,
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
File "/home/adminuser/venv/lib/python3.14/site-packages/pandas/io/excel/_base.py", line 573, in __init__
    self.book = self.load_workbook(self.handles.handle, engine_kwargs)
                ~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.14/site-packages/pandas/io/excel/_openpyxl.py", line 572, in load_workbook
    return load_workbook(
        filepath_or_buffer,
        **(default_kwargs | engine_kwargs),
    )
File "/home/adminuser/venv/lib/python3.14/site-packages/openpyxl/reader/excel.py", line 346, in load_workbook
    reader = ExcelReader(filename, read_only, keep_vba,
                         data_only, keep_links, rich_text)
File "/home/adminuser/venv/lib/python3.14/site-packages/openpyxl/reader/excel.py", line 123, in __init__
    self.archive = _validate_archive(fn)
                   ~~~~~~~~~~~~~~~~~^^^^
File "/home/adminuser/venv/lib/python3.14/site-packages/openpyxl/reader/excel.py", line 95, in _validate_archive
    archive = ZipFile(filename, 'r')
File "/usr/local/lib/python3.14/zipfile/__init__.py", line 1471, in __init__
    self._RealGetContents()
    ~~~~~~~~~~~~~~~~~~~~~^^
File "/usr/local/lib/python3.14/zipfile/__init__.py", line 1538, in _RealGetContents
    raise BadZipFile("File is not a zip file")  

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
        return pd.read_excel(arquivo, engine="openpyxl")
    else:
        return pd.read_excel(arquivo, engine="xlrd")

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
