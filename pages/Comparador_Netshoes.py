"""
Comparador de SKUs e Preços
===========================
Execução:
    python -m streamlit run app.py
"""

import io
import pandas as pd
import streamlit as st

# ── Configuração da página ────────────────────────────────────────────────────
st.set_page_config(
    page_title="Comparador de SKUs e Preços",
    page_icon="🔍",
    layout="wide",
)

# ── CSS customizado ───────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem; font-weight: 800;
        color: #1a1a2e; text-align: center; margin-bottom: 0.2rem;
    }
    .subtitle {
        text-align: center; color: #555;
        margin-bottom: 2rem; font-size: 1rem;
    }
    .metric-card {
        background: #f8f9fa; border-radius: 12px;
        padding: 1.2rem 1rem; text-align: center;
        border-left: 5px solid #ccc;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
    }
    .metric-card.total { border-color: #4361ee; }
    .metric-card.ok    { border-color: #2dc653; }
    .metric-card.div   { border-color: #e63946; }
    .metric-card.miss  { border-color: #f4a261; }
    .metric-val { font-size: 2.2rem; font-weight: 800; }
    .metric-lbl { font-size: 0.85rem; color: #666; margin-top: 0.2rem; }
    .ok-val   { color: #2dc653; }
    .div-val  { color: #e63946; }
    .miss-val { color: #f4a261; }
    .tot-val  { color: #4361ee; }
    div[data-testid="stFileUploader"] { border-radius: 10px; }
</style>
""", unsafe_allow_html=True)


# ── Funções utilitárias ───────────────────────────────────────────────────────

@st.cache_data(show_spinner=False)
def load_excel(file_bytes: bytes, filename: str) -> pd.DataFrame:
    """Carrega um arquivo Excel e retorna um DataFrame."""
    try:
        return pd.read_excel(io.BytesIO(file_bytes))
    except Exception as e:
        st.error(f"❌ Erro ao ler **{filename}**: {e}")
        return pd.DataFrame()


def normalize_sku(series: pd.Series) -> pd.Series:
    """Normaliza SKUs: strip, uppercase, converte para string."""
    return series.astype(str).str.strip().str.upper()


def to_numeric_safe(series: pd.Series) -> pd.Series:
    """Converte coluna para numérico, coercindo erros para NaN."""
    return pd.to_numeric(series, errors="coerce")


def detect_columns(df: pd.DataFrame, candidates: list[str]) -> str | None:
    """Retorna o primeiro nome de coluna (case-insensitive) que bater com algum candidato."""
    df_cols_lower = {c.lower().strip(): c for c in df.columns}
    for cand in candidates:
        if cand.lower() in df_cols_lower:
            return df_cols_lower[cand.lower()]
    return None


def find_required_columns(df, sku_candidates, val_candidates, label):
    """Detecta as colunas de SKU e valor; exibe seletores se não encontrar."""
    sku_col = detect_columns(df, sku_candidates)
    val_col = detect_columns(df, val_candidates)
    all_cols = df.columns.tolist()

    if sku_col is None:
        sku_col = st.selectbox(
            f"🔎 Coluna de SKU em **{label}** não detectada. Selecione:",
            options=all_cols, key=f"sku_{label}",
        )
    if val_col is None:
        val_col = st.selectbox(
            f"🔎 Coluna de Valor em **{label}** não detectada. Selecione:",
            options=all_cols, key=f"val_{label}",
        )
    return sku_col, val_col


def compare_skus(df_pedidos, sku_ped_col, val_ped_col, df_preco, sku_pre_col, val_pre_col):
    """Realiza a comparação entre as duas planilhas."""
    
    # Identifica colunas extras solicitadas (ignorando espaços/acentos sutis)
    extra_cols = []
    cands = ["númeropedido", "número pedido", "numeropedido", "numero pedido", 
             "nomedoproduto", "nome do produto", "nomeproduto"]
    for c in df_pedidos.columns:
        if str(c).strip().lower() in cands:
            extra_cols.append(c)
            
    ped = df_pedidos[[sku_ped_col, val_ped_col] + extra_cols].copy()
    pre = df_preco[[sku_pre_col, val_pre_col]].copy()

    # Normalização de SKUs
    ped["_sku_norm"] = normalize_sku(ped[sku_ped_col])
    pre["_sku_norm"] = normalize_sku(pre[sku_pre_col])

    # Normalização de valores
    ped[val_ped_col] = to_numeric_safe(ped[val_ped_col])
    pre[val_pre_col] = to_numeric_safe(pre[val_pre_col])

    # Sem remoção de duplicatas — mantém todos os valores integrais

    # Merge (left join — mantém todos os Pedidos)
    merged = ped.merge(pre, on="_sku_norm", how="left", suffixes=("_ped", "_pre"))

    # Colunas derivadas
    merged["diferença_valor"] = merged[val_ped_col] - merged[val_pre_col]

    def status(row):
        if pd.isna(row[val_pre_col]):
            return "SKU NÃO ENCONTRADO"
        if row[val_ped_col] == row[val_pre_col]:
            return "OK"
        return "DIVERGENTE"

    merged["status_comparação"] = merged.apply(status, axis=1)

    result = merged.rename(columns={
        sku_ped_col: "SKU Logista",
        val_ped_col: "Valor Vendido",
        sku_pre_col: "SKU Seller",
        val_pre_col: "Preço Anunciado",
        "diferença_valor": "Diferença",
        "status_comparação": "Status",
    })

    keep = extra_cols + ["SKU Logista", "SKU Seller", "Valor Vendido", "Preço Anunciado", "Diferença", "Status"]
    return result[[c for c in keep if c in result.columns]]


def style_table(df):
    """Aplica cores às linhas conforme o status."""
    def row_color(row):
        if row["Status"] == "OK":
            return ["background-color: #d4f7dc; color: #155724"] * len(row)
        if row["Status"] == "DIVERGENTE":
            if row["Diferença"] > 0:
                return ["background-color: #fde8e8; color: #721c24"] * len(row)
            elif row["Diferença"] < 0:
                return ["background-color: #ffe8cc; color: #c45e00"] * len(row)
            else:
                return ["background-color: #fde8e8; color: #721c24"] * len(row)
        return ["background-color: #fff3cd; color: #856404"] * len(row)

    fmt = {c: "R$ {:,.2f}".format for c in ["Valor Vendido", "Preço Anunciado", "Diferença"]
           if c in df.columns}
    return df.style.apply(row_color, axis=1).format(fmt, na_rep="—")


def to_excel_bytes(df: pd.DataFrame) -> bytes:
    """Serializa o DataFrame para bytes de Excel."""
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Comparação")
    return buf.getvalue()


# ── Interface ─────────────────────────────────────────────────────────────────

st.markdown('<div class="main-title">🔍 Comparador de SKUs e Preços</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Faça upload das duas planilhas e veja as divergências de preço em segundos.</div>', unsafe_allow_html=True)
st.divider()

# ── Upload lado a lado ───────────────────────────────────────────────────────
col_up1, col_up2 = st.columns(2)
with col_up1:
    st.markdown("#### 📦 Planilha de Pedidos")
    st.caption("Deve conter: SKU Logista · Valor do SKU")
    file_pedidos = st.file_uploader("Selecione o arquivo de Pedidos", type=["xlsx", "xls"], key="pedidos")
with col_up2:
    st.markdown("#### 💰 Planilha de Preço / Seller")
    st.caption("Deve conter: SKU Seller · Preço Por")
    file_preco = st.file_uploader("Selecione o arquivo de Preço/Seller", type=["xlsx", "xls"], key="preco")

# ── Pré-visualização ─────────────────────────────────────────────────────────
if file_pedidos or file_preco:
    st.divider()
    st.markdown("### 👁️ Pré-visualização das planilhas")
    prev1, prev2 = st.columns(2)
    df_pedidos, df_preco = pd.DataFrame(), pd.DataFrame()

    if file_pedidos:
        df_pedidos = load_excel(file_pedidos.read(), file_pedidos.name)
        with prev1:
            st.markdown(f"**Pedidos** — {len(df_pedidos):,} linhas · {len(df_pedidos.columns)} colunas")
            st.dataframe(df_pedidos.head(10), use_container_width=True, height=230)

    if file_preco:
        df_preco = load_excel(file_preco.read(), file_preco.name)
        with prev2:
            st.markdown(f"**Preço/Seller** — {len(df_preco):,} linhas · {len(df_preco.columns)} colunas")
            st.dataframe(df_preco.head(10), use_container_width=True, height=230)

# ── Comparação ────────────────────────────────────────────────────────────────
if file_pedidos and file_preco and not df_pedidos.empty and not df_preco.empty:
    st.divider()

    SKU_PED_CANDS = ["sku lojista", "sku logista", "sku_lojista", "SKU Lojista"]
    VAL_PED_CANDS = ["valor sku", "valor do sku", "valor_sku", "Valor sku"]
    SKU_PRE_CANDS = ["sku seller", "sku_seller", "Sku Seller"]
    VAL_PRE_CANDS = ["preço por", "preco por", "Preço Por"]

    sku_ped_col, val_ped_col = find_required_columns(df_pedidos, SKU_PED_CANDS, VAL_PED_CANDS, "Pedidos")
    sku_pre_col, val_pre_col = find_required_columns(df_preco, SKU_PRE_CANDS, VAL_PRE_CANDS, "Preço/Seller")

    if st.button("▶️  Executar Comparação", type="primary", use_container_width=True):
        with st.spinner("Processando comparação..."):
            try:
                st.session_state.result_df = compare_skus(
                    df_pedidos, sku_ped_col, val_ped_col,
                    df_preco, sku_pre_col, val_pre_col,
                )
            except Exception as e:
                st.error(f"❌ Erro durante a comparação: {e}")

    # Exibe os resultados se a comparação já foi executada
    if "result_df" in st.session_state:
        result_df = st.session_state.result_df

        # ── Métricas ──────────────────────────────────────────────
        total  = len(result_df)
        n_ok   = (result_df["Status"] == "OK").sum()
        n_div  = (result_df["Status"] == "DIVERGENTE").sum()
        n_miss = (result_df["Status"] == "SKU NÃO ENCONTRADO").sum()

        st.markdown("### 📊 Indicadores")
        m1, m2, m3, m4 = st.columns(4)
        for col, cls, val, lbl, vcls in [
            (m1, "total", total,  "Total Comparados",    "tot-val"),
            (m2, "ok",    n_ok,   "✅ OK",               "ok-val"),
            (m3, "div",   n_div,  "❌ Divergentes",      "div-val"),
            (m4, "miss",  n_miss, "⚠️ Não Encontrados",  "miss-val"),
        ]:
            with col:
                st.markdown(f"""
                <div class="metric-card {cls}">
                    <div class="metric-val {vcls}">{val:,}</div>
                    <div class="metric-lbl">{lbl}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Filtros ───────────────────────────────────────────────
        st.markdown("### 🔎 Filtros")
        status_opts = ["Todos"] + result_df["Status"].unique().tolist()
        sel_status = st.selectbox("Filtrar por Status:", status_opts)
        filtered = result_df if sel_status == "Todos" else result_df[result_df["Status"] == sel_status]

        # ── Tabela estilizada ─────────────────────────────────────
        st.markdown(f"### 📋 Resultado ({len(filtered):,} registros)")
        st.dataframe(style_table(filtered), use_container_width=True, height=450)

        # ── Download ──────────────────────────────────────────────
        st.divider()
        col_dl, _ = st.columns([1, 3])
        with col_dl:
            st.download_button(
                label="⬇️  Baixar resultado em Excel",
                data=to_excel_bytes(filtered if sel_status != "Todos" else result_df),
                file_name="comparacao_skus.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )

else:
    st.info("⬆️  Faça upload das duas planilhas para iniciar a comparação.")
