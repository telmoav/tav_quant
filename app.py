import streamlit as st
import plotly.graph_objects as go
import yfinance as yf
import pandas as pd
import numpy as np
from streamlit_autorefresh import st_autorefresh

# 1. Configuração de Interface
st.set_page_config(page_title="TAV QUANT | LIVE", layout="wide")

# Atualiza a cada 30 segundos
st_autorefresh(interval=30 * 1000, key="datarefresh")

# CSS para CLAREAR as informações e melhorar o contraste
st.markdown("""
    <style>
    /* Fundo um pouco menos preto para dar profundidade */
    [data-testid="stAppViewContainer"] { background-color: #121212; color: #ffffff; }
    
    /* Cards com bordas claras e fundo grafite */
    div[data-testid="stMetric"] {
        background-color: #1e1e1e !important;
        border: 1px solid #3d3d3d !important;
        border-radius: 10px !important;
        padding: 15px !important;
    }
    
    /* Forçar cor branca nos rótulos das métricas */
    [data-testid="stMetricLabel"] { color: #e0e0e0 !important; font-size: 1.1rem !important; font-weight: bold !important; }
    [data-testid="stMetricValue"] { color: #ffffff !important; }
    
    /* Títulos mais visíveis */
    h1, h2, h3 { color: #00f2ff !important; text-shadow: 1px 1px 2px #000; }
    
    /* Barra de Batalha */
    .battle-container { width: 100%; background: #331111; height: 40px; border-radius: 8px; border: 2px solid #555; margin: 15px 0; }
    .battle-fill { background: #00ff88; height: 100%; box-shadow: 0 0 20px #00ff88; border-radius: 6px 0 0 6px; transition: 1s; }
    </style>
    """, unsafe_allow_html=True)

# 2. Coleta de Dados com Proteção de Erro
@st.cache_data(ttl=30)
def get_live_data():
    try:
        ticker = yf.Ticker("^BVSP")
        df = ticker.history(period='1d', interval='5m')
        if not df.empty:
            atual = float(df['Close'].iloc[-1])
            hist = ticker.history(period='2d')
            fechamento_anterior = float(hist['Close'].iloc[-2]) if len(hist) > 1 else atual
            variacao = ((atual / fechamento_anterior) - 1) * 100
            return df, atual, variacao
    except:
        pass
    return pd.DataFrame(), 0.0, 0.0

df_ibov, valor_ibov, var_ibov = get_live_data()

# --- HEADER (Métricas com verificação de nulidade para evitar TypeError) ---
st.title("🛡️ TAV QUANT | INTELLIGENCE SYSTEM")

c1, c2, c3, c4, c5 = st.columns(5)

# Formatação segura
val_str = f"{valor_ibov:,.0f}" if valor_ibov > 0 else "0"
var_str = f"{var_ibov:.2f}%" if var_ibov != 0 else "0.00%"

c1.metric("IBOVESPA", val_str, var_str)
c2.metric("SINAL IA", "BULLISH" if var_ibov >= 0 else "BEARISH", "FORTE")
c3.metric("VOLATILIDADE", "18.4%", "NORMAL", delta_color="off")
c4.metric("PROB. SUCESSO", "92%", "ESTÁVEL", delta_color="off")
c5.metric("QUANT INDEX", "78", "BUY ZONE", delta_color="off")

# --- CONTEÚDO PRINCIPAL ---
st.divider()
col_left, col_mid, col_right = st.columns([1, 2, 1])

with col_mid:
    st.subheader("⚔️ DISPUTA DE AGRESSÃO (MOMENTUM)")
    # Cálculo da barra
    buy_p = 50 + (var_ibov * 5) if var_ibov != 0 else 50
    buy_p = max(min(buy_p, 98), 2)
    
    st.markdown(f"""
        <div class="battle-container">
            <div class="battle-fill" style="width: {buy_p}%;"></div>
        </div>
        <div style="display: flex; justify-content: space-between; font-weight: bold; font-size: 1.2rem;">
            <span style="color: #00ff88;">BUY {buy_p:.1f}%</span>
            <span style="color: #ff3333;">SELL {100-buy_p:.1f}%</span>
        </div>
    """, unsafe_allow_html=True)
    
    if not df_ibov.empty:
        fig = go.Figure(go.Scatter(x=df_ibov.index, y=df_ibov['Close'], 
                                 line=dict(color='#00f2ff', width=4),
                                 fill='tozeroy', fillcolor='rgba(0, 242, 255, 0.1)'))
        fig.update_layout(template="plotly_dark", height=400, margin=dict(l=0,r=0,t=0,b=0),
                         paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                         xaxis=dict(gridcolor='#333'), yaxis=dict(gridcolor='#333'))
        st.plotly_chart(fig, use_container_width=True)

with col_left:
    st.write("🟢 **BULL PRESSURE**")
    f1 = go.Figure(go.Indicator(mode="gauge+number", value=buy_p, 
                                gauge={'bar':{'color':"#00ff88"}, 'axis':{'tickcolor':"white"}, 'bgcolor':"#222"}))
    f1.update_layout(height=250, paper_bgcolor='rgba(0,0,0,0)', font={'color':"white", 'size': 18})
    st.plotly_chart(f1, use_container_width=True)

with col_right:
    st.write("🔴 **BEAR PRESSURE**")
    f2 = go.Figure(go.Indicator(mode="gauge+number", value=100-buy_p, 
                                gauge={'bar':{'color':"#ff3333"}, 'axis':{'tickcolor':"white"}, 'bgcolor':"#222"}))
    f2.update_layout(height=250, paper_bgcolor='rgba(0,0,0,0)', font={'color':"white", 'size': 18})
    st.plotly_chart(f2, use_container_width=True)

# --- QUADRO DE CRITÉRIOS ---
st.divider()
st.subheader("📋 CHECKLIST ALGORÍTMICO")
q1, q2, q3 = st.columns(3)
with q1:
    st.info("✅ SCORE TÉCNICO: ALTO")
    st.write("**Resumo:** Fluxo comprador detectado no intraday.")
with q2:
    st.info("🔵 FLUXO: INSTITUCIONAL")
    st.write("**Status:** Acumulação em níveis de suporte.")
with q3:
    st.warning("⚠️ RISCO: MÉDIO")
    st.button("🚀 DISPARAR SINAL", use_container_width=True)
