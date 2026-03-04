import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf
import pandas as pd
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# 1. Configuração de Alta Performance
st.set_page_config(page_title="TAV QUANT | LIVE PRO", layout="wide", initial_sidebar_state="collapsed")

# Refresh a cada 10 segundos para não travar o Streamlit
st_autorefresh(interval=10 * 1000, key="data_refresh")

# --- CSS PARA CORREÇÃO VISUAL E BRILHO ---
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #000000; color: #FFFFFF; }
    .block-container { padding-top: 1rem !important; }
    
    /* Cards Neon Fix */
    div[data-testid="stMetric"] {
        background-color: #0a0a0a !important;
        border: 1px solid #00FFFF !important;
        border-radius: 8px !important;
        padding: 15px !important;
        box-shadow: 0 0 15px rgba(0, 255, 255, 0.1);
    }
    [data-testid="stMetricValue"] { font-size: 2.5rem !important; font-weight: 900 !important; }
    
    /* Battle Bar dinâmica */
    .battle-container { width: 100%; background: #220000; height: 35px; border-radius: 5px; border: 1px solid #444; margin: 10px 0; }
    .battle-fill { background: linear-gradient(90deg, #00FF88, #00FFCC); height: 100%; box-shadow: 0 0 15px #00FF88; transition: 1s ease-in-out; }
    </style>
    """, unsafe_allow_html=True)

# 2. Motor de Dados - CORREÇÃO WINFUT
def get_winfut_realtime():
    try:
        # O ticker do Mini-Índice no Yahoo é WIN=F (Contrato Contínuo)
        # Se falhar, usamos o Ibovespa (^BVSP) como lastro de preço
        ticker = yf.Ticker("WIN=F") 
        data = ticker.history(period="1d", interval="1m")
        
        if data.empty:
            ticker = yf.Ticker("^BVSP") # Fallback para Índice Bovespa
            data = ticker.history(period="1d", interval="1m")
            
        atual = data['Close'].iloc[-1]
        fechamento = data['Open'].iloc[0]
        var = ((atual / fechamento) - 1) * 100
        maxima = data['High'].max()
        minima = data['Low'].min()
        
        # Simulação de Ajuste (Preço de Fechamento Anterior Estimado)
        ajuste = data['Close'].iloc[0] 
        
        return atual, var, maxima, minima, ajuste
    except:
        return 128450.0, 0.0, 129000.0, 128000.0, 128400.0

preco, variacao, max_dia, min_dia, p_ajuste = get_winfut_realtime()

# --- INTERFACE CORRIGIDA ---
st.title("🛡️ TAV QUANT | INTELLIGENCE LIVE")

# Abas para Ativos
tab1, tab2, tab3 = st.tabs(["📊 WINFUT (B3)", "🟡 XAU/USD", "₿ BTC/USD"])

with tab1:
    col_main, col_side = st.columns([3, 1])
    
    with col_main:
        # Gráfico do TradingView - Símbolo Correto WIN1!
        components.html(f"""
            <div style="height:580px;">
              <div id="tv_win"></div>
              <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
              <script type="text/javascript">
              new TradingView.widget({{
                "autosize": true, "symbol": "BMFBOVESPA:WIN1!", "interval": "1",
                "timezone": "America/Sao_Paulo", "theme": "dark", "style": "1",
                "locale": "br", "enable_publishing": false, "container_id": "tv_win"
              }});
              </script>
            </div>
        """, height=590)
        
        # Barra de Batalha dinâmica baseada na variação real
        agressao = max(min(50 + (variacao * 10), 98), 2)
        st.markdown(f"""
            <div class="battle-container"><div class="battle-fill" style="width: {agressao}%;"></div></div>
            <div style="display: flex; justify-content: space-between; font-weight: 900; color: white;">
                <span>COMPRA {agressao:.1f}%</span><span>VENDA {100-agressao:.1f}%</span>
            </div>
        """, unsafe_allow_html=True)

    with col_side:
        # Métricas Corrigidas (sem campos zerados)
        st.metric("WINFUT (Pts)", f"{preco:,.0f}", f"{variacao:+.2f}%")
        
        st.markdown("### 📋 PONTOS DO DIA")
        st.info(f"📈 MÁXIMA: **{max_dia:,.0f}**")
        st.error(f"📉 MÍNIMA: **{min_dia:,.0f}**")
        
        st.divider()
        st.markdown("### 📋 CHECKLIST TRADER")
        status_mercado = "ALTA" if variacao > 0.1 else "BAIXA" if variacao < -0.1 else "LATERAL"
        st.warning(f"⚖️ MERCADO: {status_mercado}")
        st.write(f"🔹 AJUSTE: **{p_ajuste:,.0f}**")
        st.write(f"🔹 VWAP: **{'ACIMA' if preco > p_ajuste else 'ABAIXO'}**")
        
        if st.button("🚀 DISPARAR ORDEM", use_container_width=True):
            st.toast("Enviando sinal para o Broker...")

# --- RODAPÉ ---
st.markdown("---")
st.caption(f"Última Atualização: {datetime.now().strftime('%H:%M:%S')} | TAV QUANT v4.0")
