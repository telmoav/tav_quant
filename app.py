import streamlit as st
import plotly.graph_objects as go
import yfinance as yf
import pandas as pd

# Configuração de alta densidade (Estilo Terminal)
st.set_page_config(page_title="TAV QUANT TERMINAL", layout="wide")

# CSS para o visual Neon/Dark das suas imagens
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #080808; color: white; }
    .metric-card { background: #111; border: 1px solid #333; border-radius: 4px; padding: 10px; text-align: center; }
    .battle-container { width: 100%; background: #441111; height: 30px; border-radius: 4px; border: 1px solid #555; position: relative; }
    .battle-fill { background: #00ff88; height: 100%; box-shadow: 0 0 15px #00ff88; border-radius: 4px 0 0 4px; transition: 0.5s; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER: INDICADORES TÉCNICOS ---
st.title("🤖 TAV QUANT | INTELLIGENCE")
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("IBOVESPA", "191.200", "0.91%")
c2.metric("DÓLAR", "5.15", "-1.01%", delta_color="inverse")
c3.metric("VOLATILIDADE", "18.4%", "NORMAL")
c4.metric("PROB. SUCESSO", "91.67%", "ALTA")
c5.metric("QUANT INDEX", "78", "BUY")

# --- CORPO: BATALHA E FLUXO ---
st.divider()
col_left, col_mid, col_right = st.columns([1, 2, 1])

with col_mid:
    st.markdown("### ⚔️ DISPUTA DE AGRESSÃO (BUY vs SELL)")
    buy_power = 67 # Simulado
    st.markdown(f"""
        <div class="battle-container">
            <div class="battle-fill" style="width: {buy_power}%;"></div>
        </div>
        <div style="display: flex; justify-content: space-between; font-weight: bold;">
            <span style="color: #00ff88;">COMPRA {buy_power}%</span>
            <span style="color: #ff3333;">VENDA {100-buy_power}%</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Gráfico de Tendência Real (Últimos 30 dias)
    data = yf.download('^BVSP', period='30d')['Close']
    fig = go.Figure(go.Scatter(x=data.index, y=data, fill='tozeroy', line_color='#00f2ff'))
    fig.update_layout(template="plotly_dark", height=300, margin=dict(l=0,r=0,t=20,b=0), paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

with col_left:
    st.write("📈 **SENTIMENTO BULL**")
    fig_bull = go.Figure(go.Indicator(mode="gauge+number", value=85, gauge={'bar':{'color':"#00ff88"}, 'bgcolor':"#222"}))
    fig_bull.update_layout(height=200, paper_bgcolor='rgba(0,0,0,0)', font={'color':"#00ff88"})
    st.plotly_chart(fig_bull, use_container_width=True)
    st.info("🌎 Estrangeiros: +853M")

with col_right:
    st.write("📉 **SENTIMENTO BEAR**")
    fig_bear = go.Figure(go.Indicator(mode="gauge+number", value=15, gauge={'bar':{'color':"#ff3333"}, 'bgcolor':"#222"}))
    fig_bear.update_layout(height=200, paper_bgcolor='rgba(0,0,0,0)', font={'color':"#ff3333"})
    st.plotly_chart(fig_bear, use_container_width=True)
    st.error("🏦 Institucional: -163M")

# --- FOOTER: QUADRO DE CRITÉRIOS ---
st.divider()
st.subheader("📋 QUADRO DE CRITÉRIOS ATUAIS")
q1, q2, q3 = st.columns(3)
with q1:
    st.markdown("✅ **Mínimo Compra:** 7 / **Atual:** 12")
    st.markdown("📏 **Distância Abertura:** 785 pts")
with q2:
    st.markdown("🔵 **Tendência:** Predomínio Comprador")
    st.markdown("📊 **Fibo Hoje:** 53.67%")
with q3:
    st.markdown("⚠️ **Range 10d:** 1930 pts")
    st.button("🎯 EXECUTAR SINAL", use_container_width=True)
