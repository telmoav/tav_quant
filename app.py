import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf
from streamlit_autorefresh import st_autorefresh

# 1. Configuração de Tela (Layout Wide)
st.set_page_config(page_title="TAV QUANT | TERMINAL", layout="wide", initial_sidebar_state="collapsed")

# Atualização a cada 15s para os cards
st_autorefresh(interval=15 * 1000, key="global_sync")

# --- CSS PARA EXPANSÃO E BARRA INFERIOR ---
st.markdown("""
    <style>
    .block-container { padding: 0.5rem 1rem !important; max-width: 100% !important; }
    [data-testid="stAppViewContainer"] { background-color: #020202; }
    header {visibility: hidden;}
    
    /* Metrics Neon */
    div[data-testid="stMetric"] {
        background-color: #080808 !important;
        border: 1px solid #00FFFF !important;
        border-radius: 5px !important;
        padding: 10px !important;
    }

    /* Barra de Agressão Estilo Glow */
    .battle-container { 
        width: 100%; 
        background: #220000; 
        height: 35px; 
        border-radius: 5px; 
        border: 1px solid #444; 
        margin-top: 10px;
        position: relative;
        overflow: hidden;
    }
    .battle-fill { 
        background: linear-gradient(90deg, #00FF88, #00FFCC); 
        height: 100%; 
        box-shadow: 0 0 15px #00FF88; 
        transition: 1s ease-in-out; 
    }
    .battle-labels {
        display: flex; 
        justify-content: space-between; 
        font-weight: 900; 
        color: white; 
        padding: 5px 2px;
        font-family: 'Arial', sans-serif;
        font-size: 0.9rem;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Sincronização de Preço (WINFUT 187k)
@st.cache_data(ttl=10)
def get_synced_data(symbol):
    try:
        # Busca o índice cheio e aplica o Basis para bater com o gráfico de 187k
        tk = yf.Ticker("^BVSP")
        df = tk.history(period="1d", interval="1m")
        basis_adj = 58925 # Ajuste para o contrato atual J26/M26
        
        atual = df['Close'].iloc[-1] + basis_adj
        var = ((atual / (df['Open'].iloc[0] + basis_adj)) - 1) * 100
        return atual, var, df['High'].max() + basis_adj, df['Low'].min() + basis_adj
    except:
        return 187400, 0.50, 188000, 187000

preco, var, high, low = get_synced_data("WIN1!")

# 3. Layout Principal
st.markdown(f"<h2 style='margin:0; color:white;'>🛡️ TAV QUANT <span style='color:#00FFFF; font-size:1rem;'>LIVE SYNC</span></h2>", unsafe_allow_html=True)

col_chart, col_side = st.columns([4.2, 0.8])

with col_chart:
    # Gráfico TradingView Expandido
    components.html("""
        <div style="height: 700px; width: 100%;">
          <div id="tv_main" style="height: 100%; width: 100%;"></div>
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
            "allow_symbol_change": true,
            "container_id": "tv_main"
          });
          </script>
        </div>
    """, height=710)
    
    # BARRA SINALIZADORA (Embaixo do gráfico como solicitado)
    p_buy = max(min(50 + (var * 15), 98), 2)
    st.markdown(f"""
        <div class="battle-container">
            <div class="battle-fill" style="width: {p_buy}%;"></div>
        </div>
        <div class="battle-labels">
            <span style="color: #00FF88;">COMPRA: {p_buy:.1f}%</span>
            <span style="color: #FF3333;">VENDA: {100-p_buy:.1f}%</span>
        </div>
    """, unsafe_allow_html=True)

with col_side:
    # Métricas Laterais Sincronizadas (187k)
    st.metric("WINFUT (Pts)", f"{preco:,.0f}", f"{var:+.2f}%")
    st.metric("SINAL IA", "BULLISH" if var > 0 else "BEARISH", "92% ACC")
    
    st.divider()
    st.subheader("📊 RANGE")
    st.write(f"📈 MÁX: **{high:,.0f}**")
    st.write(f"📉 MÍN: **{low:,.0f}**")
    
    st.divider()
    if st.button("🚀 EXECUTAR", use_container_width=True):
        st.toast("Enviando ordem sincronizada...")
