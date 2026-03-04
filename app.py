import streamlit as st
import streamlit.components.v1 as components
import requests
from streamlit_autorefresh import st_autorefresh

# 1. Configuração do Cockpit
st.set_page_config(page_title="TAV QUANT | WINFUT REAL-TIME", layout="wide")

# Atualização forçada a cada 5 segundos para garantir o preço atualizado
st_autorefresh(interval=5000, key="winfut_refresh")

# TOKEN DA API (Substitua pela sua chave da Brapi ou HG Brasil)
# Para WINFUT tempo real, verifique se o seu plano suporta derivativos
API_TOKEN = "SEU_TOKEN_AQUI" 

st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #000000; color: #FFFFFF; }
    div[data-testid="stMetric"] {
        background-color: #0a0a0a !important;
        border: 1px solid #00FF88 !important;
        border-radius: 4px;
        padding: 20px !important;
    }
    [data-testid="stMetricValue"] { color: #00FF88 !important; font-size: 2.8rem !important; font-weight: 900 !important; }
    [data-testid="stMetricLabel"] { color: #FFFFFF !important; font-size: 1.2rem !important; }
    
    /* Barra de Agressão */
    .battle-container { width: 100%; background: #330000; height: 45px; border-radius: 5px; border: 1px solid #444; }
    .battle-fill { background: #00FF88; height: 100%; box-shadow: 0 0 20px #00FF88; transition: 0.5s; }
    </style>
    """, unsafe_allow_html=True)

# 2. Busca de Dados Diretos (Simulando API B3 via Vendor)
def get_winfut_data():
    try:
        # Nota: WIN$ ou WINFUT dependendo do provedor
        url = f"https://brapi.dev/api/quote/WIN$?token={API_TOKEN}"
        response = requests.get(url)
        data = response.json()
        res = data['results'][0]
        return {
            "price": res['regularMarketPrice'],
            "change": res['regularMarketChangePercent'],
            "high": res['regularMarketDayHigh'],
            "low": res['regularMarketDayLow']
        }
    except:
        # Fallback para teste visual caso a API falhe
        return {"price": 0, "change": 0, "high": 0, "low": 0}

dados = get_winfut_data()

# --- LAYOUT PRINCIPAL ---
st.title("⚔️ TAV QUANT | WINFUT SQUAD")

col_chart, col_side = st.columns([3, 1])

with col_chart:
    # TradingView configurado para WINFUT (Mini Índice Futuro)
    components.html(f"""
        <div style="height:620px;">
          <div id="tv_winfut"></div>
          <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
          <script type="text/javascript">
          new TradingView.widget({{
            "autosize": true,
            "symbol": "BMFBOVESPA:WIN1!",
            "interval": "1",
            "timezone": "America/Sao_Paulo",
            "theme": "dark",
            "style": "1",
            "locale": "br",
            "enable_publishing": false,
            "hide_side_toolbar": false,
            "allow_symbol_change": true,
            "container_id": "tv_winfut"
          }});
          </script>
        </div>
    """, height=630)
    
    # Barra de Agressão baseada na variação do candle atual
    p_buy = 50 + (dados['change'] * 10) if dados['change'] != 0 else 50
    p_buy = max(min(p_buy, 98), 2)
    
    st.markdown(f"""
        <div class="battle-container"><div class="battle-fill" style="width: {p_buy}%;"></div></div>
        <div style="display: flex; justify-content: space-between; font-weight: 900; font-size: 1.2rem; margin-top: 10px;">
            <span style="color: #00FF88;">COMPRA: {p_buy:.1f}%</span>
            <span style="color: #FF3333;">VENDA: {100-p_buy:.1f}%</span>
        </div>
    """, unsafe_allow_html=True)

with col_side:
    st.metric("WINFUT", f"{dados['price']:,.0f} pts", f"{dados['change']:+.2f}%")
    
    st.divider()
    st.subheader("🚀 PONTOS DO DIA")
    st.write(f"📈 Máxima: **{dados['high']:,.0f}**")
    st.write(f"📉 Mínima: **{dados['low']:,.0f}**")
    
    st.divider()
    st.subheader("📋 CHECKLIST TRADER")
    if dados['change'] > 0.5:
        st.success("✅ TENDÊNCIA: COMPRA")
    elif dados['change'] < -0.5:
        st.error("✅ TENDÊNCIA: VENDA")
    else:
        st.warning("⚖️ MERCADO: LATERAL")
        
    st.write("🔹 VWAP: **ACIMA**")
    st.write("🔹 AJUSTE: **{:.0f}**".format(dados['price'] * 0.998)) # Simulação de ajuste

    if st.button("🎯 DISPARAR ORDEM", use_container_width=True):
        st.toast("Enviando ordem de Mini-Índice...")
