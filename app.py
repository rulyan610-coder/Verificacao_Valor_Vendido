"""
Central de Comparadores
===========================
Execução:
    python -m streamlit run app.py
"""

import streamlit as st

st.set_page_config(
    page_title="Central de Comparadores",
    page_icon="⬡",
    layout="wide",
)

# ── Design System Global ──────────────────────────────────────────────────────
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;0,9..40,800;1,9..40,400&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">

<style>
/* ── Reset & Base ─────────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Page Background ──────────────────────────────────────────────── */
.stApp {
    background-color: #F7F8FC !important;
}

/* ── Hide Streamlit chrome ────────────────────────────────────────── */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 3rem 3rem 4rem !important;
    max-width: 1100px !important;
}

/* ── Sidebar ──────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    display: none !important;
}
[data-testid="collapsedControl"] {
    display: none !important;
}

/* ── Home Page Styles ─────────────────────────────────────────────── */
.home-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #4F46E5;
    text-align: center;
    margin-bottom: 0.75rem;
}

.home-title {
    font-size: clamp(2.2rem, 4vw, 3.2rem);
    font-weight: 800;
    color: #0F172A;
    text-align: center;
    line-height: 1.15;
    letter-spacing: -0.03em;
    margin-bottom: 0.6rem;
}

.home-subtitle {
    text-align: center;
    color: #64748B;
    font-size: 1.05rem;
    font-weight: 400;
    max-width: 520px;
    margin: 0 auto 3.5rem;
    line-height: 1.6;
}

/* ── Product Cards ────────────────────────────────────────────────── */
.product-card {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 2rem 2rem 1.6rem;
    border: 1px solid #E2E8F0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 4px 16px rgba(0,0,0,0.04);
    transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
    position: relative;
    overflow: hidden;
    height: 100%;
    cursor: default;
}

.product-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 16px 16px 0 0;
}

.product-card.blue::before  { background: linear-gradient(90deg, #4F46E5, #818CF8); }
.product-card.green::before { background: linear-gradient(90deg, #10B981, #34D399); }

.product-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.10), 0 2px 8px rgba(0,0,0,0.06);
    border-color: #C7D2FE;
}

.card-icon-wrap {
    width: 48px; height: 48px;
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.4rem;
    margin-bottom: 1.2rem;
}

.card-icon-wrap.blue  { background: #EEF2FF; }
.card-icon-wrap.green { background: #ECFDF5; }

.card-title {
    font-size: 1.2rem;
    font-weight: 700;
    color: #0F172A;
    margin-bottom: 0.6rem;
    letter-spacing: -0.02em;
}

.card-desc {
    color: #64748B;
    font-size: 0.92rem;
    line-height: 1.65;
    margin-bottom: 1.4rem;
}

.card-tag {
    display: inline-block;
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    font-weight: 500;
    padding: 3px 10px;
    border-radius: 99px;
    margin-right: 6px;
    margin-top: 0.2rem;
    letter-spacing: 0.04em;
}

.card-tag.blue  { background: #EEF2FF; color: #4F46E5; }
.card-tag.green { background: #ECFDF5; color: #059669; }

.card-nav-hint {
    font-size: 0.82rem;
    color: #94A3B8;
    margin-top: 1.2rem;
    display: flex;
    align-items: center;
    gap: 6px;
}

/* ── Divider ──────────────────────────────────────────────────────── */
.divider-line {
    border: none;
    border-top: 1px solid #E2E8F0;
    margin: 2.5rem 0;
}

/* ── Footer strip ─────────────────────────────────────────────────── */
.home-footer {
    text-align: center;
    color: #94A3B8;
    font-size: 0.8rem;
    font-family: 'DM Mono', monospace;
    margin-top: 3rem;
    letter-spacing: 0.05em;
}
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown('<div class="home-eyebrow">Plataforma de Análise · v2.0</div>', unsafe_allow_html=True)
st.markdown('<div class="home-title">Central de<br>Comparadores</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="home-subtitle">Ferramentas de cruzamento e validação de dados para '
    'operações logísticas e financeiras. Selecione uma ferramenta para começar.</div>',
    unsafe_allow_html=True
)

# ── Product Cards ─────────────────────────────────────────────────────────────
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('''
    <div class="product-card blue">
        <div class="card-icon-wrap blue">🔀</div>
        <div class="card-title">Comparador Genérico</div>
        <div class="card-desc">
            Cruzamento de dados universal. Mapeie colunas equivalentes 
            dinamicamente, configure chaves de merge personalizadas e 
            defina múltiplos pares de valores para validação em qualquer 
            planilha Excel, CSV ou TXT.
        </div>
        <div>
            <span class="card-tag blue">Excel · CSV · TXT</span>
            <span class="card-tag blue">Multi-chave</span>
            <span class="card-tag blue">Multi-arquivo</span>
        </div>
        <div class="card-nav-hint">
            Clique no botão abaixo para acessar
        </div>
    </div>
    ''', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔀 Acessar Comparador Genérico", type="primary", use_container_width=True):
        st.switch_page("Comparador_Generico")

with col2:
    st.markdown('''
    <div class="product-card green">
        <div class="card-icon-wrap green">🔍</div>
        <div class="card-title">Comparador de SKUs</div>
        <div class="card-desc">
            Validação otimizada de preços e SKUs entre a Base de Pedidos 
            e a Tabela Sellers. Interface simplificada para o fluxo 
            logístico e financeiro diário, com detecção automática 
            de colunas.
        </div>
        <div>
            <span class="card-tag green">SKU · Preços</span>
            <span class="card-tag green">Auto-detect</span>
            <span class="card-tag green">Export Excel</span>
        </div>
        <div class="card-nav-hint">
            Clique no botão abaixo para acessar
        </div>
    </div>
    ''', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔍 Acessar Comparador de SKUs", type="primary", use_container_width=True):
        st.switch_page("Comparador_Netshoes")

st.markdown('<hr class="divider-line">', unsafe_allow_html=True)

st.markdown(
    '<div class="home-footer">CENTRAL DE COMPARADORES</div>',
    unsafe_allow_html=True
)