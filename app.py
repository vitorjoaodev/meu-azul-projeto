from __future__ import annotations

from typing import Final

import streamlit as st
import pandas as pd
import numpy as np
import io
import streamlit.components.v1 as components

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

components.html("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono&display=swap');

    * { margin: 0; padding: 0; box-sizing: border-box; }

    body { background: transparent; overflow-x: hidden; }

    .hero {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 20px 10px 10px;
    }

    .logo-wrapper {
        position: relative;
        width: 220px;
        height: 220px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .scan-overlay {
        position: absolute;
        top: 0; left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 10;
    }

    .scan-line {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 3px;
        background: linear-gradient(90deg, transparent, #0066CC, #66b3ff, #0066CC, transparent);
        box-shadow: 0 0 15px #0066CC, 0 0 30px #0066CC;
        opacity: 0;
        z-index: 11;
    }

    .scan-line.active {
        opacity: 1;
        animation: scanDown 1.2s ease-in-out forwards;
    }

    @keyframes scanDown {
        0% { top: 0; opacity: 1; }
        100% { top: 100%; opacity: 0.3; }
    }

    .logo-img {
        width: 200px;
        height: auto;
        border-radius: 12px;
        clip-path: inset(50% 50% 50% 50%);
        opacity: 0;
        filter: blur(20px) brightness(1.5);
        transition: none;
    }

    .logo-img.revealing {
        animation: logoReveal 1.5s cubic-bezier(0.25, 0.46, 0.45, 0.94) forwards;
    }

    @keyframes logoReveal {
        0% {
            clip-path: inset(50% 50% 50% 50%);
            opacity: 0;
            filter: blur(20px) brightness(1.5);
            transform: scale(0.8);
        }
        20% {
            clip-path: inset(40% 40% 40% 40%);
            opacity: 0.3;
            filter: blur(15px) brightness(1.4);
            transform: scale(0.85);
        }
        40% {
            clip-path: inset(25% 25% 25% 25%);
            opacity: 0.5;
            filter: blur(10px) brightness(1.3);
            transform: scale(0.9);
        }
        60% {
            clip-path: inset(12% 12% 12% 12%);
            opacity: 0.7;
            filter: blur(5px) brightness(1.15);
            transform: scale(0.95);
        }
        80% {
            clip-path: inset(4% 4% 4% 4%);
            opacity: 0.9;
            filter: blur(2px) brightness(1.05);
            transform: scale(0.98);
        }
        100% {
            clip-path: inset(0% 0% 0% 0%);
            opacity: 1;
            filter: blur(0) brightness(1);
            transform: scale(1);
        }
    }

    .glow-ring {
        position: absolute;
        width: 240px;
        height: 240px;
        border-radius: 16px;
        border: 2px solid transparent;
        opacity: 0;
        z-index: 5;
    }

    .glow-ring.active {
        animation: glowPulse 2s ease-in-out forwards;
    }

    @keyframes glowPulse {
        0% {
            opacity: 0;
            border-color: transparent;
            box-shadow: 0 0 0 rgba(0,102,204,0);
        }
        30% {
            opacity: 1;
            border-color: #0066CC;
            box-shadow: 0 0 20px rgba(0,102,204,0.5), inset 0 0 20px rgba(0,102,204,0.1);
        }
        70% {
            opacity: 1;
            border-color: #0066CC;
            box-shadow: 0 0 30px rgba(0,102,204,0.6), inset 0 0 30px rgba(0,102,204,0.15);
        }
        100% {
            opacity: 0.6;
            border-color: rgba(0,102,204,0.4);
            box-shadow: 0 0 15px rgba(0,102,204,0.3);
        }
    }

    .particles-canvas {
        position: absolute;
        top: 0; left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 12;
    }

    .title-anim {
        font-family: 'JetBrains Mono', monospace;
        font-size: 13px;
        color: #66b3ff;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-top: 18px;
        opacity: 0;
        transform: translateY(10px);
    }

    .title-anim.visible {
        animation: fadeUp 1s ease forwards;
    }

    @keyframes fadeUp {
        to { opacity: 1; transform: translateY(0); }
    }

    .typing-container {
        font-family: 'JetBrains Mono', monospace;
        font-size: 14px;
        color: #FFFFFF;
        background: linear-gradient(135deg, #001a33 0%, #003366 50%, #004080 100%);
        padding: 22px;
        border-radius: 12px;
        margin: 18px auto 0;
        border-left: 4px solid #0066CC;
        box-shadow: 0 4px 15px rgba(0, 102, 204, 0.3);
        min-height: 140px;
        width: 95%;
        max-width: 700px;
        opacity: 0;
        transform: translateY(15px);
    }

    .typing-container.visible {
        animation: fadeUp 0.8s ease forwards;
    }

    .typing-line {
        opacity: 0;
        white-space: nowrap;
        overflow: hidden;
        border-right: 2px solid #0066CC;
        width: 0;
        margin: 7px 0;
        line-height: 1.6;
    }

    .typing-line.active {
        opacity: 1;
        animation: typing 1.5s steps(50, end) forwards, blink-caret 0.6s step-end infinite;
    }

    .typing-line.done {
        opacity: 1;
        width: 100%;
        border-right: none;
    }

    .greeting-line {
        opacity: 0;
        margin-bottom: 12px;
        font-size: 15px;
        font-weight: bold;
        color: #66b3ff;
    }

    .greeting-line.visible {
        opacity: 1;
        animation: fadeUp 0.8s ease forwards;
    }

    .highlight { color: #66b3ff; font-weight: bold; }

    @keyframes typing {
        from { width: 0; }
        to { width: 100%; }
    }

    @keyframes blink-caret {
        from, to { border-color: transparent; }
        50% { border-color: #0066CC; }
    }
</style>

<div class="hero">
    <div class="logo-wrapper">
        <canvas class="particles-canvas" id="particlesCanvas"></canvas>
        <div class="glow-ring" id="glowRing"></div>
        <div class="scan-overlay">
            <div class="scan-line" id="scanLine"></div>
        </div>
        <img class="logo-img" id="logoImg"
             src="https://raw.githubusercontent.com/vitorjoaodev/meu-azul-projeto/main/logo.JPG"
             alt="Logo Azul" />
    </div>
    <div class="title-anim" id="titleAnim">Operações de Solo Safety - BRIOU</div>

    <div class="typing-container" id="typingBox">
        <div class="greeting-line" id="greetingLine">Prezado Tripulante, siga as instruções:</div>
        <div class="typing-line" id="line1">
            📋 1. Faça o upload da planilha <span class="highlight">"A"</span> e depois da <span class="highlight">"B"</span>, ambas em CSV.
        </div>
        <div class="typing-line" id="line2">
            ⏳ 2. Aguarde o carregamento completo dos arquivos.
        </div>
        <div class="typing-line" id="line3">
            ⬇️ 3. Clique no <span class="highlight">botão azul flutuante</span> para baixar sua planilha.
        </div>
        <div class="typing-line" id="line4">
            <span class="highlight">#oceuéazul</span> ✈️💙
        </div>
    </div>
</div>

<script>
(function() {
    const logo = document.getElementById('logoImg');
    const scanLine = document.getElementById('scanLine');
    const glowRing = document.getElementById('glowRing');
    const titleAnim = document.getElementById('titleAnim');
    const typingBox = document.getElementById('typingBox');
    const greetingLine = document.getElementById('greetingLine');
    const canvas = document.getElementById('particlesCanvas');
    const ctx = canvas.getContext('2d');

    canvas.width = 220;
    canvas.height = 220;

    let particles = [];

    function createParticle() {
        const cx = canvas.width / 2;
        const cy = canvas.height / 2;
        return {
            x: cx, y: cy,
            vx: (Math.random() - 0.5) * 3,
            vy: (Math.random() - 0.5) * 3,
            life: 1,
            decay: 0.008 + Math.random() * 0.015,
            size: 1 + Math.random() * 2,
            color: Math.random() > 0.5 ? '0, 102, 204' : '102, 179, 255'
        };
    }

    function animateParticles() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        for (let i = particles.length - 1; i >= 0; i--) {
            const p = particles[i];
            p.x += p.vx;
            p.y += p.vy;
            p.life -= p.decay;
            if (p.life <= 0) { particles.splice(i, 1); continue; }
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            ctx.fillStyle = 'rgba(' + p.color + ',' + p.life + ')';
            ctx.fill();
        }
        if (particles.length > 0) requestAnimationFrame(animateParticles);
    }

    function burstParticles() {
        for (let i = 0; i < 60; i++) particles.push(createParticle());
        animateParticles();
    }

    setTimeout(function() {
        scanLine.classList.add('active');
        glowRing.classList.add('active');
    }, 100);

    setTimeout(function() {
        logo.classList.add('revealing');
        burstParticles();
    }, 200);

    setTimeout(function() {
        titleAnim.classList.add('visible');
    }, 1800);

    setTimeout(function() {
        typingBox.classList.add('visible');
        greetingLine.classList.add('visible');

        const lines = typingBox.querySelectorAll('.typing-line');
        let current = 0;
        const delay = 1800;

        function typeLine() {
            if (current > 0) {
                lines[current - 1].classList.remove('active');
                lines[current - 1].classList.add('done');
            }
            if (current < lines.length) {
                lines[current].classList.add('active');
                current++;
                setTimeout(typeLine, delay);
            }
        }
        setTimeout(typeLine, 400);
    }, 2300);
})();
</script>
""", height=520)

st.title("Transferência de Planilhas - Operações de Solo Safety - BRIOU")

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


THANK_YOU_HTML = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono&display=swap');

    .thank-container {
        font-family: 'JetBrains Mono', monospace;
        font-size: 14px;
        color: #FFFFFF;
        background: linear-gradient(135deg, #001a33 0%, #003366 50%, #004080 100%);
        padding: 22px;
        border-radius: 12px;
        margin: 18px auto 0;
        border-left: 4px solid #0066CC;
        box-shadow: 0 4px 15px rgba(0, 102, 204, 0.3);
        width: 95%;
        max-width: 700px;
        opacity: 0;
        transform: translateY(15px);
        position: relative;
        overflow: hidden;
    }

    .thank-container.visible {
        animation: thankFadeUp 0.8s ease forwards;
    }

    @keyframes thankFadeUp {
        to { opacity: 1; transform: translateY(0); }
    }

    .thank-glow {
        position: absolute;
        top: 0; left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 1;
    }

    .thank-scan-line {
        position: absolute;
        top: 0; left: 0;
        width: 100%;
        height: 3px;
        background: linear-gradient(90deg, transparent, #0066CC, #66b3ff, #0066CC, transparent);
        box-shadow: 0 0 15px #0066CC, 0 0 30px #0066CC;
        opacity: 0;
        z-index: 2;
    }

    .thank-scan-line.active {
        opacity: 1;
        animation: thankScanDown 1.2s ease-in-out forwards;
    }

    @keyframes thankScanDown {
        0% { top: 0; opacity: 1; }
        100% { top: 100%; opacity: 0.3; }
    }

    .thank-text {
        position: relative;
        z-index: 3;
        opacity: 0;
        white-space: nowrap;
        overflow: hidden;
        border-right: 2px solid #0066CC;
        width: 0;
        line-height: 1.8;
        font-size: 16px;
        text-align: center;
    }

    .thank-text.active {
        opacity: 1;
        animation: thankTyping 2s steps(50, end) forwards, thankBlink 0.6s step-end infinite;
    }

    .thank-text.done {
        opacity: 1;
        width: 100%;
        border-right: none;
    }

    .thank-highlight { color: #66b3ff; font-weight: bold; }

    @keyframes thankTyping {
        from { width: 0; }
        to { width: 100%; }
    }

    @keyframes thankBlink {
        from, to { border-color: transparent; }
        50% { border-color: #0066CC; }
    }

    .thank-particles {
        position: absolute;
        top: 0; left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 4;
    }
</style>

<div class="thank-container" id="thankBox">
    <div class="thank-glow">
        <div class="thank-scan-line" id="thankScanLine"></div>
    </div>
    <canvas class="thank-particles" id="thankParticles"></canvas>
    <div class="thank-text" id="thankText">
        Obrigado! Segurança é nosso primeiro valor! <span class="thank-highlight">#voeazul</span> ✈️💙
    </div>
</div>

<script>
(function() {
    const box = document.getElementById('thankBox');
    const scanLine = document.getElementById('thankScanLine');
    const text = document.getElementById('thankText');
    const canvas = document.getElementById('thankParticles');
    const ctx = canvas.getContext('2d');

    canvas.width = canvas.parentElement.offsetWidth || 700;
    canvas.height = canvas.parentElement.offsetHeight || 80;

    let particles = [];

    function createParticle() {
        const cx = canvas.width / 2;
        const cy = canvas.height / 2;
        return {
            x: cx, y: cy,
            vx: (Math.random() - 0.5) * 3,
            vy: (Math.random() - 0.5) * 3,
            life: 1,
            decay: 0.008 + Math.random() * 0.015,
            size: 1 + Math.random() * 2,
            color: Math.random() > 0.5 ? '0, 102, 204' : '102, 179, 255'
        };
    }

    function animateParticles() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        for (let i = particles.length - 1; i >= 0; i--) {
            const p = particles[i];
            p.x += p.vx;
            p.y += p.vy;
            p.life -= p.decay;
            if (p.life <= 0) { particles.splice(i, 1); continue; }
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            ctx.fillStyle = 'rgba(' + p.color + ',' + p.life + ')';
            ctx.fill();
        }
        if (particles.length > 0) requestAnimationFrame(animateParticles);
    }

    function burstParticles() {
        for (let i = 0; i < 40; i++) particles.push(createParticle());
        animateParticles();
    }

    setTimeout(function() {
        box.classList.add('visible');
        scanLine.classList.add('active');
        burstParticles();
    }, 100);

    setTimeout(function() {
        text.classList.add('active');
    }, 800);

    setTimeout(function() {
        text.classList.remove('active');
        text.classList.add('done');
    }, 3000);
})();
</script>
"""


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
                components.html(THANK_YOU_HTML, height=120)

    except Exception as e:
        st.error(f"Erro ao ler arquivos: {e}")
        import traceback
        st.code(traceback.format_exc())
