"""
Comparador Genérico de Planilhas
=================================
Execução:
    pip install streamlit pandas openpyxl
    streamlit run app.py
"""

import io
import re
import pandas as pd
import streamlit as st

# ── Configuração da página ────────────────────────────────────────────────────
st.set_page_config(
    page_title="Comparador Genérico de Planilhas",
    page_icon="🔀",
    layout="wide",
)

# ── Design System ─────────────────────────────────────────────────────────────
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;0,9..40,800;1,9..40,400&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">

<style>
/* ── Base ─────────────────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
}
.stApp { background-color: #F7F8FC !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 2.5rem 3rem 4rem !important;
    max-width: 1200px !important;
}

/* ── Sidebar ──────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    display: none !important;
}
[data-testid="collapsedControl"] {
    display: none !important;
}

/* ── Page Header ──────────────────────────────────────────────────── */
.page-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #4F46E5;
    margin-bottom: 0.5rem;
}
.page-title {
    font-size: 2rem;
    font-weight: 800;
    color: #0F172A;
    letter-spacing: -0.03em;
    margin-bottom: 0.35rem;
    line-height: 1.2;
}
.page-subtitle {
    color: #64748B;
    font-size: 0.95rem;
    font-weight: 400;
    margin-bottom: 0;
}

/* ── Section Label ────────────────────────────────────────────────── */
.section-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #94A3B8;
    margin-bottom: 1rem;
    margin-top: 0.25rem;
}

/* ── Upload Panel ─────────────────────────────────────────────────── */
.upload-panel {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    padding: 1.6rem 1.8rem 0.8rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    margin-bottom: 0.5rem;
}
.upload-panel-title {
    font-size: 0.92rem;
    font-weight: 700;
    color: #0F172A;
    margin-bottom: 0.25rem;
}
.upload-panel-caption {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    color: #94A3B8;
    letter-spacing: 0.04em;
    margin-bottom: 0.75rem;
}

/* ── Config Panel ─────────────────────────────────────────────────── */
.config-panel {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    padding: 1.5rem 1.8rem 1.2rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    margin-bottom: 1.2rem;
    position: relative;
}
.config-panel-header {
    font-size: 0.88rem;
    font-weight: 700;
    color: #0F172A;
    margin-bottom: 0.2rem;
    display: flex;
    align-items: center;
    gap: 8px;
}
.config-panel-hint {
    font-size: 0.8rem;
    color: #94A3B8;
    margin-bottom: 1rem;
    line-height: 1.5;
}

/* ── Step Badge ───────────────────────────────────────────────────── */
.step-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 22px; height: 22px;
    background: #4F46E5;
    color: #fff;
    border-radius: 6px;
    font-size: 0.72rem;
    font-weight: 700;
    flex-shrink: 0;
    font-family: 'DM Mono', monospace;
}

/* ── Metric Cards ─────────────────────────────────────────────────── */
.metric-strip {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    text-align: center;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    position: relative;
    overflow: hidden;
}
.metric-strip::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 0 0 14px 14px;
}
.metric-strip.tot::after { background: #4F46E5; }
.metric-strip.ok::after  { background: #10B981; }
.metric-strip.div::after { background: #EF4444; }
.metric-strip.miss::after{ background: #F59E0B; }

.metric-num {
    font-size: 2.4rem;
    font-weight: 800;
    line-height: 1;
    letter-spacing: -0.04em;
    margin-bottom: 0.35rem;
}
.metric-num.tot  { color: #4F46E5; }
.metric-num.ok   { color: #10B981; }
.metric-num.div  { color: #EF4444; }
.metric-num.miss { color: #F59E0B; }

.metric-label {
    font-size: 0.78rem;
    font-weight: 600;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

/* ── Buttons ──────────────────────────────────────────────────────── */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #4F46E5, #6366F1) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.01em !important;
    padding: 0.6rem 1.8rem !important;
    box-shadow: 0 4px 14px rgba(79,70,229,0.35) !important;
    transition: all 0.2s ease !important;
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 20px rgba(79,70,229,0.4) !important;
}
.stButton > button[kind="primary"]:disabled {
    background: #E2E8F0 !important;
    color: #94A3B8 !important;
    box-shadow: none !important;
    transform: none !important;
}
.stDownloadButton > button {
    background: #0F172A !important;
    color: #F8FAFC !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    transition: background 0.2s !important;
}
.stDownloadButton > button:hover { background: #1E293B !important; }

/* ── Misc ─────────────────────────────────────────────────────────── */
hr[data-testid="stDivider"] {
    border-color: #E2E8F0 !important;
    margin: 1.8rem 0 !important;
}
[data-testid="stDataFrame"] {
    border-radius: 12px !important;
    border: 1px solid #E2E8F0 !important;
    overflow: hidden !important;
}
label, .stSelectbox label, .stMultiSelect label {
    font-weight: 600 !important;
    color: #374151 !important;
    font-size: 0.875rem !important;
}
.stAlert, .stInfo, .stWarning, .stError {
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
}
</style>
""", unsafe_allow_html=True)

NONE_LABEL = "— nenhuma —"

# ── Helpers ───────────────────────────────────────────────────────────────────

@st.cache_data(show_spinner=False)
def load_file(file_bytes: bytes, filename: str) -> pd.DataFrame:
    """
    Carrega Excel (.xlsx/.xls) ou texto tabular (.txt/.csv/.tsv).

    Estratégia para TXT:
      1. Tenta TAB como separador (exportações de ERP/sistema)
      2. Se resultar em 1 coluna só, tenta ponto-e-vírgula e depois vírgula
      3. Testa encodings: utf-8-sig → latin-1 → cp1252

    Para Excel usa openpyxl normalmente.
    """
    ext = filename.rsplit(".", 1)[-1].lower()

    if ext in ("xlsx", "xls"):
        try:
            return pd.read_excel(io.BytesIO(file_bytes))
        except Exception as e:
            st.error(f"❌ Erro ao ler **{filename}**: {e}")
            return pd.DataFrame()

    # ── Arquivo de texto ──────────────────────────────────────────────────────
    encodings = ["utf-8-sig", "latin-1", "cp1252"]
    separators = ["\t", ";", ","]

    for enc in encodings:
        try:
            text = file_bytes.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    else:
        st.error(f"❌ Não foi possível decodificar **{filename}** (utf-8, latin-1, cp1252 falharam).")
        return pd.DataFrame()

    for sep in separators:
        try:
            df = pd.read_csv(io.StringIO(text), sep=sep, dtype=str)
            if len(df.columns) > 1:          # separador correto → mais de 1 coluna
                return df
        except Exception:
            continue

    st.error(f"❌ Não foi possível determinar o separador de **{filename}**.")
    return pd.DataFrame()


def load_and_concat(files):
    frames, names = [], []
    for f in files:
        df = load_file(f.read(), f.name)
        if not df.empty:
            df["_origem"] = f.name
            frames.append(df)
            names.append(f.name)
    if not frames:
        return pd.DataFrame(), []
    return pd.concat(frames, ignore_index=True), names


def safe_col_options(df: pd.DataFrame) -> list:
    return [c for c in df.columns if c != "_origem"]


def multiselect_slots(label_prefix: str, options: list, max_items: int, key: str) -> list:
    """
    Renderiza até max_items selectboxes encadeados.
    Para de mostrar slots opcionais assim que o usuário deixa um vazio.
    """
    selected = []
    for i in range(max_items):
        required = i == 0
        lbl = f"{'★ ' if required else ''}  Campo {i + 1}" + (" (obrigatório)" if required else " (opcional)")
        choice = st.selectbox(
            lbl,
            [NONE_LABEL] + [o for o in options if o not in selected],
            key=f"{key}_{i}",
        )
        if choice != NONE_LABEL:
            selected.append(choice)
        elif not required:
            break
    return selected


def parse_monetary(value) -> float:
    """
    Converte qualquer representação monetária para float.

    Exemplos suportados:
        "499.9"          → 499.9
        "379,88"         → 379.88
        "BRL 379.88"     → 379.88
        "R$ 1.299,90"    → 1299.90
        "1,299.90"       → 1299.90   (padrão americano com milhar)
        1299.90          → 1299.90   (já é número)
        ""  / None / NaN → NaN
    """
    if value is None:
        return float("nan")
    if isinstance(value, (int, float)):
        return float(value)

    s = str(value).strip()
    if not s or s.lower() in ("nan", "none", "-", ""):
        return float("nan")

    # Remove prefixos de moeda e espaços  (BRL, R$, USD, $, €, £ …)
    s = re.sub(r"(?i)\b(brl|usd|eur|gbp)\b", "", s)
    s = re.sub(r"[R\$€£¥]", "", s)
    s = s.strip()

    # Detecta o padrão numérico:
    #   Caso 1 — "1.299,90"  → milhar=ponto, decimal=vírgula  → BRL clássico
    #   Caso 2 — "1,299.90"  → milhar=vírgula, decimal=ponto  → padrão americano
    #   Caso 3 — "379,88"    → apenas vírgula (sem ponto)      → decimal=vírgula
    #   Caso 4 — "1299.90"   → apenas ponto                    → decimal=ponto

    has_dot   = "." in s
    has_comma = "," in s

    if has_dot and has_comma:
        # Descobre qual veio por último — esse é o separador decimal
        if s.rfind(".") > s.rfind(","):
            # "1,299.90" → remove vírgulas (milhar), ponto = decimal
            s = s.replace(",", "")
        else:
            # "1.299,90" → remove pontos (milhar), vírgula → ponto
            s = s.replace(".", "").replace(",", ".")
    elif has_comma and not has_dot:
        # "379,88" → vírgula é decimal
        s = s.replace(",", ".")
    # else: has_dot only or neither → já está no formato correto

    # Extrai o número final (ignora qualquer lixo restante)
    match = re.search(r"-?\d+(?:\.\d+)?", s)
    if not match:
        return float("nan")

    try:
        return float(match.group())
    except ValueError:
        return float("nan")


def parse_monetary_series(series: pd.Series) -> pd.Series:
    """Aplica parse_monetary em toda a série, retornando float64."""
    return series.map(parse_monetary).astype(float)


def normalize_key(s: pd.Series) -> pd.Series:
    return s.astype(str).str.strip().str.upper()


# ── Lógica de comparação ──────────────────────────────────────────────────────

def compare_generic(
    df_a: pd.DataFrame,
    keys_a: list,
    extra_a: list,
    val_cols_a: list,   # colunas de valor em A
    df_b: pd.DataFrame,
    keys_b: list,
    extra_b: list,
    val_cols_b: list,   # colunas de valor em B (pares com val_cols_a)
) -> pd.DataFrame:

    has_origem = "_origem" in df_a.columns

    # ── 1. Selecionar colunas relevantes de cada lado ─────────────────────────
    cols_needed_a = list(dict.fromkeys(
        keys_a + extra_a + val_cols_a + (["_origem"] if has_origem else [])
    ))
    cols_needed_b = list(dict.fromkeys(keys_b + extra_b + val_cols_b))

    a = df_a[[c for c in cols_needed_a if c in df_a.columns]].copy()
    b = df_b[[c for c in cols_needed_b if c in df_b.columns]].copy()

    # ── 2. Renomear colunas com prefixo _A_ / _B_ para evitar colisões ────────
    #       Apenas colunas que NÃO são chave (chaves viram merge keys neutras)
    rename_a, rename_b = {}, {}
    for c in extra_a + val_cols_a:
        rename_a[c] = f"_A_{c}"
    for c in extra_b + val_cols_b:
        rename_b[c] = f"_B_{c}"

    a = a.rename(columns=rename_a)
    b = b.rename(columns=rename_b)

    val_cols_a_r = [f"_A_{c}" for c in val_cols_a]
    val_cols_b_r = [f"_B_{c}" for c in val_cols_b]
    extra_a_r    = [f"_A_{c}" for c in extra_a]
    extra_b_r    = [f"_B_{c}" for c in extra_b]

    # ── 3. Criar colunas de merge normalizadas ─────────────────────────────────
    merge_keys = [f"_mk_{i}" for i in range(len(keys_a))]
    for mk, src in zip(merge_keys, keys_a):
        a[mk] = normalize_key(a[src])
    for mk, src in zip(merge_keys, keys_b):
        b[mk] = normalize_key(b[src])

    # ── 4. Deduplicar B e fazer merge ─────────────────────────────────────────
    b_dedup = b.drop_duplicates(subset=merge_keys, keep="first")
    merged  = a.merge(b_dedup, on=merge_keys, how="left")

    # ── 5. Calcular diferenças e status por par ────────────────────────────────
    status_cols = []
    for ca_r, cb_r, orig_a in zip(val_cols_a_r, val_cols_b_r, val_cols_a):
        merged[ca_r] = parse_monetary_series(merged[ca_r])
        merged[cb_r] = parse_monetary_series(merged[cb_r])

        diff_col   = f"Δ {orig_a}"
        status_col = f"Status [{orig_a}]"
        merged[diff_col] = merged[ca_r] - merged[cb_r]

        def _st(row, ca=ca_r, cb=cb_r):
            if pd.isna(row.get(cb)) or pd.isna(row.get(ca)):
                return "NÃO ENCONTRADO"
            return "OK" if row[ca] == row[cb] else "DIVERGENTE"

        merged[status_col] = merged.apply(_st, axis=1)
        status_cols.append(status_col)

    # ── 6. Status Geral ────────────────────────────────────────────────────────
    def _geral(row):
        if not status_cols:
            # sem colunas de valor: verifica se houve match via primeira chave B
            b_excl = [c for c in merged.columns if c.startswith("_B_")]
            if b_excl and pd.isna(row.get(b_excl[0])):
                return "NÃO ENCONTRADO"
            return "OK"
        vals = [row[sc] for sc in status_cols]
        if any(v == "NÃO ENCONTRADO" for v in vals): return "NÃO ENCONTRADO"
        if any(v == "DIVERGENTE"      for v in vals): return "DIVERGENTE"
        return "OK"

    merged["⚡ Status Geral"] = merged.apply(_geral, axis=1)

    # ── 7. Montar resultado final com nomes amigáveis ─────────────────────────
    result_cols = []

    if has_origem and "_origem" in merged.columns:
        merged = merged.rename(columns={"_origem": "Arquivo Origem"})
        result_cols.append("Arquivo Origem")

    # Chaves — usar os nomes originais de A
    result_cols += keys_a

    # Extras A → "NomeCol [A]"
    for orig, renamed in zip(extra_a, extra_a_r):
        if renamed in merged.columns:
            disp = f"{orig} [A]"
            merged = merged.rename(columns={renamed: disp})
            result_cols.append(disp)

    # Extras B → "NomeCol [B]"
    for orig, renamed in zip(extra_b, extra_b_r):
        if renamed in merged.columns:
            disp = f"{orig} [B]"
            merged = merged.rename(columns={renamed: disp})
            result_cols.append(disp)

    # Pares de valor + diferença + status
    for orig_a, orig_b, ca_r, cb_r in zip(val_cols_a, val_cols_b, val_cols_a_r, val_cols_b_r):
        disp_a = f"{orig_a} [A]"
        disp_b = f"{orig_b} [B]"
        if ca_r in merged.columns:
            merged = merged.rename(columns={ca_r: disp_a})
            result_cols.append(disp_a)
        if cb_r in merged.columns:
            merged = merged.rename(columns={cb_r: disp_b})
            result_cols.append(disp_b)
        diff_col   = f"Δ {orig_a}"
        status_col = f"Status [{orig_a}]"
        if diff_col   in merged.columns: result_cols.append(diff_col)
        if status_col in merged.columns: result_cols.append(status_col)

    result_cols.append("⚡ Status Geral")

    # Deduplicar preservando ordem
    seen, final = set(), []
    for c in result_cols:
        if c not in seen and c in merged.columns:
            seen.add(c); final.append(c)

    return merged[final]


# ── Estilo da tabela ──────────────────────────────────────────────────────────

def style_table(df: pd.DataFrame):
    def row_color(row):
        s = row.get("⚡ Status Geral", "")
        if s == "OK":             return ["background-color: #ECFDF5; color: #065F46"] * len(row)
        if s == "DIVERGENTE":     return ["background-color: #FEF2F2; color: #991B1B"] * len(row)
        if s == "NÃO ENCONTRADO": return ["background-color: #FFFBEB; color: #78350F"] * len(row)
        return [""] * len(row)

    fmt = {c: "{:,.4f}".format for c in df.columns if c.startswith("Δ ")}
    return df.style.apply(row_color, axis=1).format(fmt, na_rep="—")


def to_excel_bytes(df: pd.DataFrame) -> bytes:
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as w:
        df.to_excel(w, index=False, sheet_name="Comparação")
    return buf.getvalue()


# ── INTERFACE ─────────────────────────────────────────────────────────────────

if st.button("🏠 Voltar para a Central", type="primary"):
    st.switch_page("app.py")
st.markdown("<br>", unsafe_allow_html=True)

# Page Header
col_hdr, _ = st.columns([3, 1])
with col_hdr:
    st.markdown('<div class="page-eyebrow">Comparador · Genérico</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-title">Comparador Genérico de Planilhas</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">Configure chaves, pares de valor e colunas extras — '
        'compare qualquer estrutura de dado entre dois arquivos.</div>',
        unsafe_allow_html=True,
    )

st.divider()

# ── PASSO 1 — Upload ──────────────────────────────────────────────────────────
st.markdown(
    '<div class="section-label"><span class="step-badge">1</span>&nbsp; Upload das Planilhas</div>',
    unsafe_allow_html=True,
)
col_up1, col_up2 = st.columns(2, gap="large")

with col_up1:
    st.markdown("""
    <div class="upload-panel">
        <div class="upload-panel-title">📂 Planilha A &nbsp;<em style="font-weight:400;color:#94A3B8;font-size:0.82rem;">(Pedidos / Base)</em></div>
        <div class="upload-panel-caption">ACEITA UM OU MAIS ARQUIVOS — SERÃO CONSOLIDADOS AUTOMATICAMENTE</div>
    </div>
    """, unsafe_allow_html=True)
    files_a = st.file_uploader(
        "Arquivo(s) A",
        type=["xlsx", "xls", "txt", "csv", "tsv"],
        accept_multiple_files=True,
        key="up_a",
        label_visibility="collapsed",
    )

with col_up2:
    st.markdown("""
    <div class="upload-panel">
        <div class="upload-panel-title">📂 Planilha B &nbsp;<em style="font-weight:400;color:#94A3B8;font-size:0.82rem;">(Referência / Preço)</em></div>
        <div class="upload-panel-caption">APENAS UM ARQUIVO DE REFERÊNCIA</div>
    </div>
    """, unsafe_allow_html=True)
    file_b = st.file_uploader(
        "Arquivo B",
        type=["xlsx", "xls", "txt", "csv", "tsv"],
        key="up_b",
        label_visibility="collapsed",
    )

# ── Carregar dados ────────────────────────────────────────────────────────────
df_a, nomes_a = pd.DataFrame(), []
df_b = pd.DataFrame()

if files_a:
    df_a, nomes_a = load_and_concat(files_a)
if file_b:
    df_b = load_file(file_b.read(), file_b.name)

# ── PASSO 2 — Pré-visualização ────────────────────────────────────────────────
if not df_a.empty or not df_b.empty:
    st.divider()
    st.markdown(
        '<div class="section-label"><span class="step-badge">2</span>&nbsp; Pré-visualização</div>',
        unsafe_allow_html=True,
    )
    pv1, pv2 = st.columns(2, gap="large")

    with pv1:
        if not df_a.empty:
            badges_html = "".join(
                f'<span style="display:inline-block;background:#EEF2FF;color:#4F46E5;'
                f'border-radius:99px;padding:2px 10px;font-size:0.72rem;'
                f'font-family:\'DM Mono\',monospace;margin:2px 4px 2px 0;">'
                f'📄 {n}</span>' for n in nomes_a
            )
            st.caption(f"**Planilha A** — {len(df_a):,} linhas · {len(nomes_a)} arquivo(s)")
            st.markdown(badges_html, unsafe_allow_html=True)
            if len(nomes_a) > 1:
                with st.expander("Ver contagem por arquivo"):
                    cts = df_a["_origem"].value_counts().rename_axis("Arquivo").reset_index(name="Linhas")
                    st.dataframe(cts, use_container_width=True, hide_index=True)
            st.dataframe(
                df_a.drop(columns=["_origem"], errors="ignore").head(8),
                use_container_width=True, height=220,
            )

    with pv2:
        if not df_b.empty:
            st.caption(f"**Planilha B** — {len(df_b):,} linhas · {len(df_b.columns)} colunas")
            st.dataframe(df_b.head(8), use_container_width=True, height=220)

# ── PASSO 3 — Configuração das colunas ───────────────────────────────────────
if not df_a.empty and not df_b.empty:
    st.divider()
    st.markdown(
        '<div class="section-label"><span class="step-badge">3</span>&nbsp; Configuração das Colunas</div>',
        unsafe_allow_html=True,
    )

    cols_a = safe_col_options(df_a)
    cols_b = safe_col_options(df_b)

    # ── 3a) Chaves de merge ───────────────────────────────────────────────────
    st.markdown("""
    <div class="config-panel">
        <div class="config-panel-header">🔑 Colunas de Identificação / Chave de Cruzamento</div>
        <div class="config-panel-hint">
            Defina quais campos identificam cada registro. O merge será feito por esses campos.
            Ex.: SKU, Código do Produto, ID do Pedido.
        </div>
    </div>
    """, unsafe_allow_html=True)

    ka1, ka2 = st.columns(2, gap="large")
    with ka1:
        st.markdown("**Planilha A** — chaves")
        keys_a = multiselect_slots("Chave A", cols_a, max_items=4, key="key_a")
    with ka2:
        st.markdown("**Planilha B** — chaves correspondentes")
        keys_b = multiselect_slots("Chave B", cols_b, max_items=4, key="key_b")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── 3b) Pares de valor para comparação ───────────────────────────────────
    st.markdown("""
    <div class="config-panel">
        <div class="config-panel-header">⚖️ Pares de Colunas para Comparação de Valores</div>
        <div class="config-panel-hint">
            Para cada par, o sistema calcula a diferença (A − B) e determina OK / DIVERGENTE.
            Deixe ambos como '— nenhuma —' para parar de adicionar pares.
        </div>
    </div>
    """, unsafe_allow_html=True)

    val_cols_a, val_cols_b = [], []
    for i in range(4):
        c1, c2 = st.columns(2, gap="large")
        req = "(obrigatório)" if i == 0 else "(opcional)"
        with c1:
            va = st.selectbox(
                f"Valor A — Par {i+1} {req}",
                [NONE_LABEL] + [c for c in cols_a if c not in val_cols_a],
                key=f"va_{i}",
            )
        with c2:
            vb = st.selectbox(
                f"Valor B — Par {i+1} {req}",
                [NONE_LABEL] + [c for c in cols_b if c not in val_cols_b],
                key=f"vb_{i}",
            )
        if va != NONE_LABEL and vb != NONE_LABEL:
            val_cols_a.append(va)
            val_cols_b.append(vb)
        elif i > 0:
            break

    st.markdown("<br>", unsafe_allow_html=True)

    # ── 3c) Colunas extras para exibição ─────────────────────────────────────
    st.markdown("""
    <div class="config-panel">
        <div class="config-panel-header">👁 Colunas Adicionais para Exibição <em style="font-weight:400;color:#94A3B8;font-size:0.82rem;">(opcional)</em></div>
        <div class="config-panel-hint">
            Campos que aparecem no resultado para facilitar a leitura — sem comparação de valor.
        </div>
    </div>
    """, unsafe_allow_html=True)

    ex1, ex2 = st.columns(2, gap="large")
    used_a = set(keys_a + val_cols_a)
    used_b = set(keys_b + val_cols_b)
    with ex1:
        extra_a = st.multiselect(
            "Planilha A — extras (até 4)",
            [c for c in cols_a if c not in used_a],
            max_selections=4, key="extra_a",
        )
    with ex2:
        extra_b = st.multiselect(
            "Planilha B — extras (até 4)",
            [c for c in cols_b if c not in used_b],
            max_selections=4, key="extra_b",
        )

    # ── Validação ─────────────────────────────────────────────────────────────
    erros = []
    if not keys_a:
        erros.append("Selecione ao menos **1 coluna de chave** na Planilha A.")
    if not keys_b:
        erros.append("Selecione ao menos **1 coluna de chave** na Planilha B.")
    if len(keys_a) != len(keys_b):
        erros.append(f"Quantidade de chaves deve ser igual dos dois lados (A={len(keys_a)}, B={len(keys_b)}).")
    if len(val_cols_a) != len(val_cols_b):
        erros.append("Complete os pares de valor: cada Par precisa ter coluna em A **e** em B.")

    for e in erros:
        st.warning(f"⚠️ {e}")

    # ── Botão ─────────────────────────────────────────────────────────────────
    st.divider()
    run = st.button(
        "▶  Executar Comparação",
        type="primary",
        use_container_width=True,
        disabled=bool(erros),
    )

    # ── PASSO 4 — Resultado ───────────────────────────────────────────────────
    if run:
        with st.spinner("Processando comparação..."):
            try:
                # ── Painel de debug dos valores monetários ────────────────────
                if val_cols_a and val_cols_b:
                    with st.expander("🔬 Debug: limpeza de valores antes da comparação", expanded=False):
                        st.caption(
                            "Mostra os primeiros 10 valores originais e o resultado "
                            "após `parse_monetary`. Útil para detectar problemas de formato."
                        )
                        for orig_a, orig_b in zip(val_cols_a, val_cols_b):
                            d1, d2 = st.columns(2)
                            with d1:
                                st.markdown(f"**A → `{orig_a}`**")
                                sample_a = df_a[orig_a].dropna().head(10) if orig_a in df_a.columns else pd.Series([], dtype=object)
                                dbg_a = pd.DataFrame({
                                    "Original":  sample_a.values,
                                    "Convertido": [parse_monetary(v) for v in sample_a.values],
                                })
                                def _hi(r):
                                    return ["background-color:#FFFBEB"] * 2 if pd.isna(r["Convertido"]) else [""] * 2
                                st.dataframe(dbg_a.style.apply(_hi, axis=1), use_container_width=True, hide_index=True)
                            with d2:
                                st.markdown(f"**B → `{orig_b}`**")
                                sample_b = df_b[orig_b].dropna().head(10) if orig_b in df_b.columns else pd.Series([], dtype=object)
                                dbg_b = pd.DataFrame({
                                    "Original":  sample_b.values,
                                    "Convertido": [parse_monetary(v) for v in sample_b.values],
                                })
                                st.dataframe(dbg_b.style.apply(_hi, axis=1), use_container_width=True, hide_index=True)

                result_df = compare_generic(
                    df_a, keys_a, extra_a, val_cols_a,
                    df_b, keys_b, extra_b, val_cols_b,
                )

                total  = len(result_df)
                n_ok   = (result_df["⚡ Status Geral"] == "OK").sum()
                n_div  = (result_df["⚡ Status Geral"] == "DIVERGENTE").sum()
                n_miss = (result_df["⚡ Status Geral"] == "NÃO ENCONTRADO").sum()

                # ── Métricas ──────────────────────────────────────────────────
                st.divider()
                st.markdown('<div class="section-label">04 &nbsp;—&nbsp; Indicadores</div>', unsafe_allow_html=True)
                m1, m2, m3, m4 = st.columns(4, gap="medium")
                for col, css_cls, val, lbl in [
                    (m1, "tot",  total,  "Total Comparados"),
                    (m2, "ok",   n_ok,   "OK"),
                    (m3, "div",  n_div,  "Divergentes"),
                    (m4, "miss", n_miss, "Não Encontrados"),
                ]:
                    with col:
                        st.markdown(f"""
                        <div class="metric-strip {css_cls}">
                            <div class="metric-num {css_cls}">{val:,}</div>
                            <div class="metric-label">{lbl}</div>
                        </div>""", unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                # ── Filtros dinâmicos ─────────────────────────────────────────
                st.markdown('<div class="section-label">05 &nbsp;—&nbsp; Filtros</div>', unsafe_allow_html=True)
                f1, f2, f3 = st.columns(3, gap="medium")

                with f1:
                    sel_status = st.selectbox(
                        "Status Geral:",
                        ["Todos"] + sorted(result_df["⚡ Status Geral"].unique().tolist()),
                        key="filt_status",
                    )
                with f2:
                    if "Arquivo Origem" in result_df.columns:
                        sel_arquivo = st.selectbox(
                            "Arquivo:",
                            ["Todos"] + sorted(result_df["Arquivo Origem"].dropna().unique().tolist()),
                            key="filt_arquivo",
                        )
                    else:
                        sel_arquivo = "Todos"

                with f3:
                    if keys_a and keys_a[0] in result_df.columns:
                        chave_opts = ["Todos"] + sorted(
                            result_df[keys_a[0]].dropna().astype(str).unique().tolist()
                        )
                        sel_chave = st.selectbox(f"{keys_a[0]}:", chave_opts, key="filt_chave")
                    else:
                        sel_chave = "Todos"

                filtered = result_df.copy()
                if sel_status != "Todos":
                    filtered = filtered[filtered["⚡ Status Geral"] == sel_status]
                if sel_arquivo != "Todos" and "Arquivo Origem" in filtered.columns:
                    filtered = filtered[filtered["Arquivo Origem"] == sel_arquivo]
                if sel_chave != "Todos" and keys_a and keys_a[0] in filtered.columns:
                    filtered = filtered[filtered[keys_a[0]].astype(str) == sel_chave]

                # ── Tabela ────────────────────────────────────────────────────
                st.divider()
                st.markdown(
                    f'<div class="section-label">06 &nbsp;—&nbsp; Resultado &nbsp;'
                    f'<span style="color:#0F172A;font-size:0.8rem;">({len(filtered):,} de {total:,} registros)</span></div>',
                    unsafe_allow_html=True
                )
                st.dataframe(style_table(filtered), use_container_width=True, height=500)

                # ── Resumo estatístico das diferenças ─────────────────────────
                diff_cols = [c for c in result_df.columns if c.startswith("Δ ")]
                if diff_cols:
                    with st.expander("📈 Resumo estatístico das diferenças"):
                        stats = result_df[diff_cols].describe().T
                        stats.index = [c.replace("Δ ", "") for c in stats.index]
                        st.dataframe(
                            stats.style.format("{:,.4f}", na_rep="—"),
                            use_container_width=True,
                        )

                # ── Downloads ─────────────────────────────────────────────────
                st.divider()
                dl1, dl2, _ = st.columns([1, 1, 2], gap="medium")
                with dl1:
                    st.download_button(
                        "⬇  Baixar resultado completo",
                        data=to_excel_bytes(result_df),
                        file_name="comparacao_completa.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True,
                    )
                with dl2:
                    div_df = result_df[result_df["⚡ Status Geral"] == "DIVERGENTE"]
                    st.download_button(
                        "⬇  Baixar só divergentes",
                        data=to_excel_bytes(div_df),
                        file_name="divergentes.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True,
                        disabled=div_df.empty,
                    )

            except Exception as e:
                st.error(f"❌ Erro durante a comparação: {e}")
                st.exception(e)

else:
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("⬆  Faça upload das duas planilhas para começar.")