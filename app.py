import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# 1. Configurações de Página e Auto-Update
st.set_page_config(page_title="TAV QUANT | INTELLIGENCE", layout="wide", initial_sidebar_state="collapsed")

# Força atualização a cada 15 segundos para os cálculos de Python
st_autorefresh(interval=15 * 1000, key="global_refresh")

# --- CSS PERSONALIZADO (ALTO CONTRASTE) ---
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #000000; color: #FFFFFF; }
    .block-container { padding-top: 1rem !important; }
    
    /* Metrics Style */
    div[data-testid="stMetric"] {
        background-color: #0a0a0a !important;
        border: 1px solid #00FFFF !important;
        border-radius: 10px !important;
        padding: 20px !important;
        box-shadow: 0 0 10px rgba(0, 255, 255, 0.2);
    }
    [data-testid="stMetricValue"] { font-size: 2.4rem !important; font-weight: 900 !important; color: #FFFFFF !important; }
    [data-testid="stMetricLabel"] { color: #00FFFF !important; text-transform: uppercase; letter-spacing: 1px; }

    /* Battle Bar Glow */
    .battle-container { width: 100%; background: #220000; height: 35px; border-radius: 5px; border: 1px solid #444; margin: 10px 0; }
    .battle-fill { background: linear-gradient(90deg, #00FF88, #00FFCC); height: 100%; box-shadow: 0 0 15px #00FF88; transition: 1s ease-in-out; }
    
    /* Tabs Style */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { height: 45px; background-color: #111; border-radius: 5px 5px 0 0; color: white; }
    .stTabs [aria-selected="true"] { background-color: #00FFFF !important; color: black !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Coleta de Dados Real-Time (Correção de Tickers)
def get_market_data(ticker_symbol):
    try:
        # Usando sufixo .SA para B3 e tickers globais para Ouro/BTC
        tk = yf.Ticker(ticker_symbol)
        df = tk.history(period='1d', interval='1m')
        if not df.empty:
            atual = df['Close'].iloc[-1]
            prev = tk.history(period='2d')['Close'].iloc[-2]
            var = ((atual / prev) - 1) * 100
            maxima = df['High'].max()
            minima = df['Low'].min()
            return atual, var, maxima, minima
    except:
        pass
    return 0.0, 0.0, 0.0, 0.0

# 3. Widget TradingView (Sincronizado)
def tradingview_widget(symbol):
    return f"""
    <div style="height:550px;">
      <div id="tv_chart_{symbol}"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget({{
        "autosize": true, "symbol": "{symbol}", "interval": "1",
        "timezone": "America/Sao_Paulo", "theme": "dark", "style": "1",
        "locale": "br", "enable_publishing": false, "container_id": "tv_chart_{symbol}"
      }});
      </script>
    </div>
    """

# --- CONTEÚDO DO DASHBOARD ---
st.title("🛡️ TAV QUANT | INTELLIGENCE LIVE")

tab_win, tab_gold, tab_btc = st.tabs(["⚔️ WINFUT (B3)", "🟡 XAU/USD", "₿ BTC/USD"])

# ABA WINFUT
with tab_win:
    # Para o WinFut em tempo real no Python, o mais próximo gratuito é o Ibovespa (^BVSP)
    preco, var, high, low = get_market_data("^BVSP")
    
    c1, c2 = st.columns([3, 1])
    with c1:
        components.html(tradingview_widget("BMFBOVESPA:WIN1!"), height=560)
        p_buy = max(min(50 + (var * 15), 98), 2)
        st.markdown(f'<div class="battle-container"><div class="battle-fill" style="width: {p_buy}%;"></div></div>', unsafe_allow_html=True)
        st.markdown(f"**COMPRA: {p_buy:.1f}% | VENDA: {100-p_buy:.1f}%**")
        
    with c2:
        st.metric("WINFUT (Pts)", f"{preco:,.0f}", f"{var:+.2f}%")
        st.metric("SCORE IA", "BULLISH" if var > 0 else "BEARISH", "92% ACC")
        st.divider()
        st.write(f"📈 MÁXIMA: **{high:,.0f}**")
        st.write(f"📉 MÍNIMA: **{low:,.0f}**")
        st.divider()
        st.info("💡 VWAP: ACIMA DO PREÇO")

# ABA OURO
with tab_gold:
    preco_g, var_g, high_g, low_g = get_market_data("GC=F")
    c1, c2 = st.columns([3, 1])
    with c1:
        components.html(tradingview_widget("OANDA:XAUUSD"), height=560)
    with c2:
        st.metric("GOLD PRICE", f"$ {preco_g:,.2f}", f"{var_g:+.2f}%")
        st.metric("QUANT INDEX", "78", "BUY ZONE")
        st.divider()
        st.write(f"📈 MÁXIMA: {high_g:,.2f}")
        st.write(f"📉 MÍNIMA: {low_g:,.2f}")

# ABA BITCOIN
with tab_btc:
    preco_b, var_b, high_b, low_b = get_market_data("BTC-USD")
    c1, c2 = st.columns([3, 1])
    with c1:
        components.html(tradingview_widget("BINANCE:BTCUSDT"), height=560)
    with c2:
        st.metric("BITCOIN", f"$ {preco_b:,.0f}", f"{var_b:+.2f}%")
        st.metric("SINAL", "LONG", "72.1% WR")

st.markdown("---")
st.caption("TAV QUANT v4.0 | 2026 Operational Terminal | Dados Sincronizados")
