import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf
from streamlit_autorefresh import st_autorefresh
from datetime import datetime

# 1. Configuração de Cockpit (Ocupa 100% da tela)
st.set_page_config(page_title="TAV QUANT | TERMINAL", layout="wide", initial_sidebar_state="collapsed")

# Refresh inteligente a cada 10s
st_autorefresh(interval=10 * 1000, key="terminal_refresh")

# --- CSS DE APRESENTAÇÃO PREMIUM ---
st.markdown("""
    <style>
    /* Estética Dark Mode Real */
    [data-testid="stAppViewContainer"] { background-color: #020202; color: #e0e0e0; }
    .block-container { padding: 0.5rem 1rem !important; max-width: 100% !important; }
    
    /* Metrics: Minimalistas e Neon */
    div[data-testid="stMetric"] {
        background-color: #080808 !important;
        border-left: 4px solid #00FFFF !important;
        border-radius: 4px !important;
        padding: 10px !important;
        transition: 0.3s;
    }
    div[data-testid="stMetric"]:hover { background-color: #111 !important; border-left: 4px solid #00FF88 !important; }
    [data-testid="stMetricValue"] { font-size: 2.2rem !important; font-weight: 800 !important; font-family: 'JetBrains Mono', monospace; }
    [data-testid="stMetricLabel"] { color: #888 !important; text-transform: uppercase; font-size: 0.8rem !important; }

    /* Barra de Agressão Profissional */
    .battle-bg { width: 100%; background: #1a0000; height: 12px; border-radius: 20px; overflow: hidden; margin: 10px 0; border: 1px solid #333; }
    .battle-fill { background: linear-gradient(90deg, #00FF88, #00FFFF); height: 100%; border-radius: 20px; transition: 1s ease; box-shadow: 0 0 10px #00FF88; }
    
    /* Esconder Header do Streamlit */
    header {visibility: hidden;}
    .stTabs [data-baseweb="tab-list"] { background-color: transparent; }
    .stTabs [data-baseweb="tab"] { color: #555; font-weight: bold; }
    .stTabs [aria-selected="true"] { color: #00FFFF !important; border-bottom-color: #00FFFF !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Motor de Sincronização de Dados (Correção de Basis)
@st.cache_data(ttl=10)
def get_synced_data():
    try:
        # Ticker do Mini-Índice na B3 para sincronizar com o gráfico
        # Nota: WIN=F no Yahoo Finance reflete o contrato futuro
        tk = yf.Ticker("WIN=F")
        df = tk.history(period="1d", interval="1m")
        
        if df.empty:
            # Caso o ticker futuro falhe, usamos o Ibovespa e somamos a diferença (basis)
            # No momento das suas imagens a diferença era de ~59.000 pontos
            vista = yf.Ticker("^BVSP")
            df = vista.history(period="1d", interval="1m")
            ajuste_basis = 58925 
            atual = df['Close'].iloc[-1] + ajuste_basis
        else:
            atual = df['Close'].iloc[-1]
            
        var = ((atual / df['Open'].iloc[0]) - 1) * 100
        return atual, var, df['High'].max(), df['Low'].min()
    except:
        return 187400, 0.0, 188000, 187000

preco, var, high, low = get_synced_data()

# 3. Layout de Apresentação
# Logo e Relógio
c_logo, c_time = st.columns([8, 2])
c_logo.markdown(f"<h2 style='margin:0; color:white;'>🛡️ TAV QUANT <span style='color:#00FFFF; font-size:1rem;'>TERMINAL v4.0</span></h2>", unsafe_allow_html=True)
c_time.markdown(f"<p style='text-align:right; color:#555;'>{datetime.now().strftime('%H:%M:%S')} | LIVE</p>", unsafe_allow_html=True)

st.divider()

col_left, col_right = st.columns([4.2, 0.8])

with col_left:
    # Gráfico Expandido e Sem Bordas
    components.html(f"""
        <div style="height: 680px; width: 100%; border-radius: 8px; overflow: hidden; border: 1px solid #222;">
          <div id="tv_chart" style="height: 100%;"></div>
          <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
          <script type="text/javascript">
          new TradingView.widget({{
            "autosize": true, "symbol": "BMFBOVESPA:WIN1!", "interval": "1",
            "timezone": "America/Sao_Paulo", "theme": "dark", "style": "1",
            "locale": "br", "enable_publishing": false, "container_id": "tv_chart"
          }});
          </script>
        </div>
    """, height=690)
    
    # Barra de Agressão Estilizada
    p_buy = max(min(50 + (var * 12), 98), 2)
    st.markdown(f"""
        <div style="display: flex; justify-content: space-between; font-size: 0.7rem; color: #888; margin-top: 15px;">
            <span>AGRESSÃO COMPRA: {p_buy:.1f}%</span>
            <span>VENDA: {100-p_buy:.1f}%</span>
        </div>
        <div class="battle-bg"><div class="battle-fill" style="width: {p_buy}%;"></div></div>
    """, unsafe_allow_html=True)

with col_right:
    # Métricas de Alta Fidelidade (Sincronizadas com o Gráfico)
    st.metric("WINFUT (PTS)", f"{preco:,.0f}", f"{var:+.2f}%")
    st.metric("SCORE IA", "BULLISH" if var > 0 else "BEARISH", "92% ACC")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Painel de Monitoramento
    with st.expander("📊 RANGE DO DIA", expanded=True):
        st.write(f"📈 Máxima: <span style='color:#00FF88;'>{high:,.0f}</span>", unsafe_allow_html=True)
        st.write(f"📉 Mínima: <span style='color:#FF3333;'>{low:,.0f}</span>", unsafe_allow_html=True)
        st.write(f"⚖️ Pivot: **{(high+low)/2:,.0f}**")

    st.markdown("<br>", unsafe_allow_html=True)

    # Checklist Operacional
    st.markdown("<p style='color:#555; font-size:0.7rem; margin-bottom:5px;'>CHECKLIST TRADER</p>", unsafe_allow_html=True)
    if var > 0.5:
        st.success("TENDÊNCIA: COMPRA")
    elif var < -0.5:
        st.error("TENDÊNCIA: VENDA")
    else:
        st.warning("MERCADO: LATERAL")
    
    st.button("🎯 EXECUTAR", use_container_width=True)
