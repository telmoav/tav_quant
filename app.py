import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# 1. Configuração de Layout Ultra-Wide
st.set_page_config(page_title="TAV QUANT | TERMINAL", layout="wide", initial_sidebar_state="collapsed")

# Atualização de dados a cada 15 segundos
st_autorefresh(interval=15 * 1000, key="global_sync")

# --- CSS PREMIUM: Expansão Total e Estética Dark ---
st.markdown("""
    <style>
    /* Expande o container para 100% da largura da tela */
    .block-container { padding: 0.5rem 1rem !important; max-width: 100% !important; }
    [data-testid="stAppViewContainer"] { background-color: #020202; }
    
    /* Metrics Neon Style */
    div[data-testid="stMetric"] {
        background-color: #080808 !important;
        border: 1px solid #00FFFF !important;
        border-radius: 5px !important;
        padding: 10px !important;
    }
    [data-testid="stMetricValue"] { font-size: 2.2rem !important; font-weight: 800 !important; color: #FFFFFF !important; }
    [data-testid="stMetricLabel"] { color: #00FFFF !important; text-transform: uppercase; }
    
    /* Esconder elementos padrão */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 2. Motor de Sincronização de Dados (Correção de Basis)
@st.cache_data(ttl=10)
def get_market_data(symbol):
    try:
        # Mapeamento para garantir que o Python leia o Futuro e não o À Vista
        mapping = {"WIN1!": "WIN=F", "WDO1!": "WDO=F", "IBOV": "^BVSP"}
        target = mapping.get(symbol, symbol)
        
        # Adiciona sufixo B3 se for ação brasileira e não tiver
        if target.isalpha() and len(target) <= 5 and not target.endswith(".SA"):
            target += ".SA"
            
        tk = yf.Ticker(target)
        df = tk.history(period="1d", interval="1m")
        
        if df.empty and target == "WIN=F":
            # Fallback dinâmico: se o ticker futuro falhar, usa o Ibovespa + Basis
            vista = yf.Ticker("^BVSP").history(period="1d", interval="1m")
            basis = 58925 # Diferença aproximada entre WIN e IBOV
            atual = vista['Close'].iloc[-1] + basis
            var = ((atual / (vista['Open'].iloc[0] + basis)) - 1) * 100
            return atual, var, vista['High'].max() + basis, vista['Low'].min() + basis

        atual = df['Close'].iloc[-1]
        var = ((atual / df['Open'].iloc[0]) - 1) * 100
        return atual, var, df['High'].max(), df['Low'].min()
    except:
        return 0.0, 0.0, 0.0, 0.0

# 3. Estrutura do Painel
st.markdown(f"<h2 style='margin:0; color:white;'>🛡️ TAV QUANT <span style='color:#00FFFF; font-size:1rem;'>MULTI-TERMINAL PRO</span></h2>", unsafe_allow_html=True)

col_main, col_side = st.columns([4.2, 0.8])

with col_main:
    # Gráfico com Busca Liberada ("allow_symbol_change": true)
    # Altura aumentada para 750px para expansão total
    components.html("""
        <div style="height: 750px; width: 100%;">
          <div id="tradingview_quant" style="height: 100%; width: 100%;"></div>
          <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
          <script type="text/javascript">
          new TradingView.widget({
            "autosize": true,
            "symbol": "BMFBOVESPA:WIN1!",
            "interval": "1",
            "timezone": "America/Sao_Paulo",
            "theme": "dark",
            "style": "1",
            "locale": "br",
            "toolbar_bg": "#f1f3f6",
            "enable_publishing": false,
            "allow_symbol_change": true,
            "save_image": false,
            "container_id": "tradingview_quant"
          });
          </script>
        </div>
    """, height=760)
    
    st.caption("💡 DICA: Clique no nome do ativo (topo esquerdo do gráfico) para pesquisar qualquer ativo (PETR4, BTCUSDT, etc).")

with col_side:
    # Seletor para sincronizar os cards laterais com o que você está operando
    asset = st.selectbox("SINCRONIZAR CARDS:", ["WIN1!", "WDO1!", "PETR4", "VALE3", "IBOV", "BTC-USD"])
    
    preco, var, high, low = get_market_data(asset)
    
    # Exibição Sincronizada
    st.metric(asset, f"{preco:,.0f}" if preco > 1000 else f"{preco:,.2f}", f"{var:+.2f}%")
    
    st.divider()
    st.markdown("### 📊 RANGE DIA")
    st.write(f"📈 MÁX: **{high:,.0f}**")
    st.write(f"📉 MÍN: **{low:,.0f}**")
    
    st.divider()
    st.subheader("🤖 IA SIGNAL")
    if var > 0.3:
        st.success("TENDÊNCIA: ALTA")
    elif var < -0.3:
        st.error("TENDÊNCIA: BAIXA")
    else:
        st.warning("MERCADO: LATERAL")
        
    if st.button("🎯 BOOT CAMP QUANT", use_container_width=True):
        st.toast("Iniciando varredura de fluxo...")
