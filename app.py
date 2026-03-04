import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf
from streamlit_autorefresh import st_autorefresh

# 1. Configuração de Tela Cheia
st.set_page_config(page_title="TAV QUANT | MULTI-ASSET", layout="wide", initial_sidebar_state="collapsed")

# Auto-refresh para manter os cálculos de suporte ativos
st_autorefresh(interval=20 * 1000, key="multi_asset_refresh")

# --- CSS PARA EXPANSÃO TOTAL ---
st.markdown("""
    <style>
    .block-container { padding: 0.5rem 1rem !important; max-width: 100% !important; }
    header {visibility: hidden;}
    div[data-testid="stMetric"] { background-color: #080808; border-left: 4px solid #00FFFF; border-radius: 4px; }
    [data-testid="stMetricValue"] { font-size: 2.2rem !important; font-weight: 800 !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Lógica de Captura (Dinâmica)
@st.cache_data(ttl=15)
def get_dynamic_data(symbol):
    try:
        # Tenta mapear o símbolo para o Yahoo Finance
        mapper = {"WIN1!": "WIN=F", "WDO1!": "WDO=F", "IBOV": "^BVSP"}
        yf_symbol = mapper.get(symbol, symbol)
        if not yf_symbol.endswith(".SA") and yf_symbol.isalpha():
            yf_symbol += ".SA" # Auto-add para ações B3
            
        tk = yf.Ticker(yf_symbol)
        df = tk.history(period="1d", interval="1m")
        if not df.empty:
            atual = df['Close'].iloc[-1]
            var = ((atual / df['Open'].iloc[0]) - 1) * 100
            return atual, var, df['High'].max(), df['Low'].min()
    except:
        pass
    return 0.0, 0.0, 0.0, 0.0

# 3. Widget TradingView com BUSCA LIBERADA
def draw_unlocked_chart():
    return """
    <div style="height: 720px; width: 100%;">
      <div id="tv_unlocked" style="height: 100%; width: 100%;"></div>
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
        "allow_symbol_change": true,  /* LIBERA A TROCA DE ATIVO */
        "show_popup_button": true,
        "popup_width": "1000",
        "popup_height": "650",
        "withdateranges": true,
        "container_id": "tv_unlocked"
      });
      </script>
    </div>
    """

st.markdown(f"<h3 style='margin:0;'>🛡️ TAV QUANT <span style='color:#00FFFF;'>MULTI-TERMINAL</span></h3>", unsafe_allow_html=True)

col_left, col_right = st.columns([4.2, 0.8])

with col_left:
    # Gráfico onde você pode digitar qualquer ativo agora
    components.html(draw_unlocked_chart(), height=730)
    
    st.info("💡 DICA: Clique no nome do ativo no canto superior esquerdo do gráfico para digitar um novo (ex: PETR4, WDO1!, BTCUSDT).")

with col_right:
    # Como o ativo no gráfico é independente, mantemos um seletor aqui 
    # apenas para as métricas do Python acompanharem sua análise
    asset_ref = st.selectbox("SINCRONIZAR MÉTRICAS:", ["WIN1!", "WDO1!", "PETR4", "VALE3", "IBOV"])
    
    preco, var, high, low = get_dynamic_data(asset_ref)
    
    st.metric(asset_ref, f"{preco:,.0f}" if preco > 200 else f"{preco:,.2f}", f"{var:+.2f}%")
    
    st.divider()
    st.write(f"📈 Máx: {high:,.0f}")
    st.write(f"📉 Mín: {low:,.0f}")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("🚀 BOOT CAMP QUANT", use_container_width=True):
        st.success("Algoritmo de análise ativado para este ativo!")
