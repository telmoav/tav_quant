import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# 1. Configuração de Interface
st.set_page_config(page_title="TAV QUANT | B3 EDITION", layout="wide")

# Refresh de dados a cada 30 segundos
st_autorefresh(interval=30 * 1000, key="b3_refresh")

st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #000000; color: #FFFFFF; }
    div[data-testid="stMetric"] {
        background-color: #111111 !important;
        border: 1px solid #00FF88 !important;
        border-radius: 5px;
    }
    [data-testid="stMetricLabel"] { color: #00FF88 !important; font-weight: bold; }
    [data-testid="stMetricValue"] { color: #FFFFFF !important; font-weight: 900; }
    
    .battle-container { width: 100%; background: #330000; height: 35px; border-radius: 5px; border: 1px solid #444; }
    .battle-fill { background: #00FF88; height: 100%; box-shadow: 0 0 15px #00FF88; transition: 1s; }
    </style>
    """, unsafe_allow_html=True)

# 2. Motor de Dados B3 (.SA)
@st.cache_data(ttl=30)
def get_b3_data(ticker):
    try:
        # Adiciona o sufixo da B3 se não tiver
        full_ticker = f"{ticker}.SA" if not ticker.endswith(".SA") else ticker
        tk = yf.Ticker(full_ticker)
        df = tk.history(period='1d', interval='1m')
        if not df.empty:
            atual = float(df['Close'].iloc[-1])
            prev = tk.history(period='2d')['Close'].iloc[-2]
            var = ((atual / prev) - 1) * 100
            return atual, var
    except: pass
    return 0.0, 0.0

def draw_b3_chart(symbol):
    # Força o Widget a buscar no feed da BMFBOVESPA
    return f"""
    <div style="height:600px;">
      <div id="tv_b3_{symbol}" style="height:100%;"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget({{
        "autosize": true,
        "symbol": "BMFBOVESPA:{symbol}",
        "interval": "5",
        "timezone": "America/Sao_Paulo",
        "theme": "dark",
        "style": "1",
        "locale": "br",
        "toolbar_bg": "#f1f3f6",
        "enable_publishing": false,
        "hide_side_toolbar": false,
        "allow_symbol_change": true,
        "container_id": "tv_b3_{symbol}"
      }});
      </script>
    </div>
    """

st.title("🛡️ TAV QUANT | B3 OPERATIONAL")

# Seleção de Ativos da B3
b3_asset = st.selectbox("SELECIONE O ATIVO B3", ["IBOV", "WIN1!", "WDO1!", "PETR4", "VALE3", "ITUB4"], index=0)

col_chart, col_side = st.columns([3, 1])

# Mapeamento para o Yahoo Finance (Dados das métricas)
yf_mapper = {"IBOV": "^BVSP", "PETR4": "PETR4.SA", "VALE3": "VALE3.SA", "ITUB4": "ITUB4.SA", "WIN1!": "^BVSP", "WDO1!": "USDBRL=X"}

with col_chart:
    # Gráfico do TradingView com feed BMFBOVESPA
    components.html(draw_b3_chart(b3_asset), height=610)
    
    # Lógica de Agressão baseada no preço real B3
    price, var = get_b3_data(yf_mapper[b3_asset])
    p_buy = 50 + (var * 20) if var != 0 else 50
    p_buy = max(min(p_buy, 98), 2)
    
    st.markdown(f"""
        <div class="battle-container"><div class="battle-fill" style="width: {p_buy}%;"></div></div>
        <div style="display: flex; justify-content: space-between; font-weight: 900; color: white; padding: 5px;">
            <span>AGRESSÃO COMPRA: {p_buy:.1f}%</span>
            <span>AGRESSÃO VENDA: {100-p_buy:.1f}%</span>
        </div>
    """, unsafe_allow_html=True)

with col_side:
    st.metric(f"PREÇO {b3_asset}", f"R$ {price:,.2f}" if b3_asset != "IBOV" else f"{price:,.0f} pts", f"{var:+.2f}%")
    
    st.divider()
    st.subheader("📋 FILTROS B3")
    st.write(f"🔹 **Papel:** {b3_asset}")
    st.write(f"🔹 **Tendência:** {'ALTA' if var > 0 else 'BAIXA'}")
    st.write(f"🔹 **Volatilidade:** Alta")
    
    st.divider()
    if st.button("🚀 DISPARAR ORDEM B3", use_container_width=True):
        st.toast(f"Enviando ordem de {b3_asset} para a mesa...")

st.info("Nota: Os dados das métricas possuem delay de 15min (padrão Yahoo Finance Free). Para tempo real zero, é necessário API paga da B3.")
