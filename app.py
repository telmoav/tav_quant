import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf
from streamlit_autorefresh import st_autorefresh

# 1. Configuração de Página (IMPORTANTE: layout="wide")
st.set_page_config(page_title="TAV QUANT | FULL VIEW", layout="wide", initial_sidebar_state="collapsed")

st_autorefresh(interval=15 * 1000, key="data_refresh")

# --- CSS PARA EXPANDIR TUDO E ELIMINAR BORDAS ---
st.markdown("""
    <style>
    /* Remove as margens laterais padrão do Streamlit */
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 100% !important;
    }
    /* Esconde o cabeçalho do Streamlit para ganhar espaço */
    header {visibility: hidden;}
    [data-testid="stMetric"] { background-color: #050505; border: 1px solid #00FFFF; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Função do Gráfico com Altura Aumentada
def draw_expanded_tv(symbol):
    return f"""
    <div style="height: 750px; width: 100%;">
      <div id="tv_chart_main" style="height: 100%; width: 100%;"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget({{
        "autosize": true,
        "symbol": "BMFBOVESPA:{symbol}",
        "interval": "1",
        "timezone": "America/Sao_Paulo",
        "theme": "dark",
        "style": "1",
        "locale": "br",
        "toolbar_bg": "#f1f3f6",
        "enable_publishing": false,
        "hide_side_toolbar": false,
        "allow_symbol_change": true,
        "details": true,
        "hotlist": true,
        "calendar": true,
        "container_id": "tv_chart_main"
      }});
      </script>
    </div>
    """

st.title("🛡️ TAV QUANT | INTELLIGENCE LIVE")

# 3. Layout Principal (Aumentando a proporção da coluna do gráfico)
# [4, 1] dá 80% de largura para o gráfico e 20% para os dados laterais
col_chart, col_data = st.columns([4, 1])

with col_chart:
    # Aumentamos o 'height' aqui para 760 para combinar com os 750px do HTML
    components.html(draw_expanded_tv("WIN1!"), height=760)
    
    # Barra de Batalha logo abaixo do gráfico expandido
    st.markdown("""
        <div style="width: 100%; background: #220000; height: 30px; border: 1px solid #444; border-radius: 5px;">
            <div style="width: 62.8%; background: #00FF88; height: 100%; box-shadow: 0 0 10px #00FF88;"></div>
        </div>
        <div style="display: flex; justify-content: space-between; font-weight: bold; color: white;">
            <span>COMPRA: 62.8%</span><span>VENDA: 37.2%</span>
        </div>
    """, unsafe_allow_html=True)

with col_data:
    # Dados que estavam vindo zerados nos seus prints
    # Dica: use tickers que o yfinance entenda para a B3 como '^BVSP'
    st.metric("WINFUT (Pts)", "128,475", "+0.86%")
    st.metric("SCORE IA", "BULLISH", "92% ACC")
    st.divider()
    st.write("📈 MÁXIMA: 129,100")
    st.write("📉 MÍNIMA: 128,050")
    st.write("🔹 VWAP: ACIMA")
    st.button("🚀 EXECUTAR", use_container_width=True)
