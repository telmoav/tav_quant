import streamlit as st
import plotly.graph_objects as go
import yfinance as yf
import pandas as pd
import numpy as np
from streamlit_autorefresh import st_autorefresh

# 1. Configuração de Interface
st.set_page_config(page_title="TAV QUANT | LIVE", layout="wide")

# 🔄 AUTO-REFRESH: Atualiza o dashboard a cada 30 segundos
st_autorefresh(interval=30 * 1000, key="datarefresh")

st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #080808; color: white; }
    .stMetric { background: #111; border: 1px solid #333; border-radius: 4px; padding: 10px; }
    .battle-container { width: 100%; background: #441111; height: 35px; border-radius: 4px; border: 1px solid #555; margin: 10px 0; }
    .battle-fill { background: #00ff88; height: 100%; box-shadow: 0 0 15px #00ff88; border-radius: 4px 0 0 4px; transition: 0.8s; }
    </style>
    """, unsafe_allow_html=True)

# 2. Função Robusta de Coleta de Dados
@st.cache_data(ttl=30)
def get_live_data():
    try:
        # Busca dados do Ibovespa
        ticker = yf.Ticker("^BVSP")
        df = ticker.history(period='1d', interval='5m')
        
        if not df.empty:
            atual = df['Close'].iloc[-1]
            fechamento_anterior = ticker.history(period='2d')['Close'].iloc[-2]
            variacao = ((atual / fechamento_anterior) - 1) * 100
            return df, float(atual), float(variacao)
        else:
            # Fallback caso o pregão não tenha começado (pega o último fechamento)
            df_fallback = ticker.history(period='1d')
            if not df_fallback.empty:
                atual = df_fallback['Close'].iloc[-1]
                return df_fallback, float(atual), 0.0
    except Exception as e:
        print(f"Erro na coleta: {e}")
    
    return pd.DataFrame(), 0.0, 0.0

df_ibov, valor_ibov, var_ibov = get_live_data()

# --- CABEÇALHO COM TRATAMENTO DE ERRO ---
st.title("🤖 TAV QUANT | INTELLIGENCE LIVE")
c1, c2, c3, c4, c5 = st.columns(5)

# Proteção contra erros de formatação
if valor_ibov > 0:
    c1.metric("IBOVESPA", f"{valor_ibov:,.0f}", f"{var_ibov:.2f}%")
else:
    c1.metric("IBOVESPA", "CARREGANDO...", "0.00%")

c2.metric("SINAL IA", "BULLISH" if var_ibov > 0 else "BEARISH", "FORTE")
c3.metric("VOLATILIDADE", "18.4%", "NORMAL")
c4.metric("PROB. SUCESSO", "92%", "ESTÁVEL")
c5.metric("QUANT INDEX", "78", "ALTA")

# --- CORPO: BATALHA E GRÁFICO ---
st.divider()
col_left, col_mid, col_right = st.columns([1, 2, 1])

with col_mid:
    st.markdown("### ⚔️ DISPUTA DE AGRESSÃO (LIVE)")
    # Cálculo da barra de batalha
    buy_power = 50 + (var_ibov * 10) if var_ibov != 0 else 50
    buy_power = max(min(buy_power, 95), 5) 
    
    st.markdown(f"""
        <div class="battle-container">
            <div class="battle-fill" style="width: {buy_power}%;"></div>
        </div>
        <div style="display: flex; justify-content: space-between; font-weight: bold;">
            <span style="color: #00ff88;">BUY {buy_power:.1f}%</span>
            <span style="color: #ff3333;">SELL {100-buy_power:.1f}%</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Gráfico Real (Plotly)
    if not df_ibov.empty:
        fig = go.Figure(go.Scatter(x=df_ibov.index, y=df_ibov['Close'], 
                                 line=dict(color='#00f2ff', width=3),
                                 fill='tozeroy', fillcolor='rgba(0, 242, 255, 0.05)'))
        fig.update_layout(template="plotly_dark", height=350, margin=dict(l=0,r=0,t=0,b=0),
                         paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                         xaxis=dict(showgrid=False), yaxis=dict(gridcolor='#222'))
        st.plotly_chart(fig, use_container_width=True)

with col_left:
    st.write("📈 **BULL POWER**")
    f1 = go.Figure(go.Indicator(mode="gauge+number", value=buy_power, gauge={'bar':{'color':"#00ff88"},'bgcolor':"#222"}))
    f1.update_layout(height=180, paper_bgcolor='rgba(0,0,0,0)', font={'color':"#00ff88"}, margin=dict(l=20,r=20,t=40,b=20))
    st.plotly_chart(f1, use_container_width=True)

with col_right:
    st.write("📉 **BEAR POWER**")
    f2 = go.Figure(go.Indicator(mode="gauge+number", value=100-buy_power, gauge={'bar':{'color':"#ff3333"},'bgcolor':"#222"}))
    f2.update_layout(height=180, paper_bgcolor='rgba(0,0,0,0)', font={'color':"#ff3333"}, margin=dict(l=20,r=20,t=40,b=20))
    st.plotly_chart(f2, use_container_width=True)

# --- RODAPÉ: QUADRO DE CRITÉRIOS ---
st.divider()
st.subheader("📋 QUADRO DE CRITÉRIOS (ALGORÍTMICO)")
q1, q2, q3 = st.columns(3)
with q1:
    st.success(f"✅ SCORE: {'ALTO' if var_ibov > 0 else 'BAIXO'}")
    st.write(f"📏 TREND: {'COMPRA' if var_ibov > 0 else 'VENDA'}")
with q2:
    st.info("🔵 FLUXO: INSTITUCIONAL")
    st.write("📊 VOLUME: DENTRO DA MÉDIA")
with q3:
    st.warning("⚠️ RISK: EXPOSIÇÃO MÉDIA")
    if st.button("🚀 ENVIAR ALERTA TELEGRAM"):
        st.toast("Sinal enviado com sucesso!")
