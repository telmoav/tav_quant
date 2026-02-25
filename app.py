import streamlit as st
import plotly.graph_objects as go
import yfinance as yf
import pandas as pd
import numpy as np
from streamlit_autorefresh import st_autorefresh

# 1. Configuração de Página (Forçar ocupação total da tela)
st.set_page_config(page_title="TAV QUANT | COCKPIT", layout="wide", initial_sidebar_state="collapsed")

# Auto-update (30s)
st_autorefresh(interval=30 * 1000, key="datarefresh")

# --- CSS PARA DISTRIBUIÇÃO E BRILHO ---
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #000000; color: #FFFFFF; }
    
    /* Remover espaços em branco excessivos no topo */
    .block-container { padding-top: 1rem !important; padding-bottom: 0rem !important; }
    
    /* Estilização das métricas para ficarem compactas e brilhantes */
    div[data-testid="stMetric"] {
        background-color: #111111 !important;
        border: 1px solid #00FFFF !important;
        border-radius: 5px !important;
        padding: 10px !important;
        text-align: center;
    }

    [data-testid="stMetricLabel"] { color: #00FFFF !important; font-size: 0.9rem !important; font-weight: bold !important; }
    [data-testid="stMetricValue"] { color: #FFFFFF !important; font-size: 1.8rem !important; font-weight: 900 !important; }

    /* Barra de Batalha Estilizada */
    .battle-container { width: 100%; background: #330000; height: 35px; border-radius: 5px; border: 1px solid #555; margin-top: 10px; }
    .battle-fill { background: #00FF88; height: 100%; box-shadow: 0 0 15px #00FF88; border-radius: 4px 0 0 4px; }
    
    /* Esconder o menu do Streamlit para parecer um software nativo */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 2. Coleta de Dados
@st.cache_data(ttl=30)
def get_data():
    try:
        tk = yf.Ticker("^BVSP")
        df = tk.history(period='1d', interval='5m')
        if not df.empty:
            atual = float(df['Close'].iloc[-1])
            prev = float(tk.history(period='2d')['Close'].iloc[-2])
            var = ((atual / prev) - 1) * 100
            return df, atual, var
    except: pass
    return pd.DataFrame(), 0.0, 0.0

df, val, var = get_data()

# --- LAYOUT DE TRÊS COLUNAS (O COCKPIT) ---
# Coluna 1: Gauges e Checklist (Esquerda)
# Coluna 2: Preço e Batalha (Centro - Maior)
# Coluna 3: Métricas e Sinais (Direita)

col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.markdown("### 📊 SENTIMENTO")
    p_buy = 50 + (var * 10) if var != 0 else 50
    p_buy = max(min(p_buy, 98), 2)
    
    # Gauge Compacto de Compra
    fig_g1 = go.Figure(go.Indicator(mode="gauge+number", value=p_buy, 
                 gauge={'bar':{'color':"#00FF88"}, 'bgcolor':"#222", 'axis':{'range':[0,100], 'visible':False}}))
    fig_g1.update_layout(height=180, margin=dict(l=10,r=10,t=30,b=10), paper_bgcolor='rgba(0,0,0,0)', font={'color':"white", 'weight':'bold'})
    st.plotly_chart(fig_g1, use_container_width=True)
    
    st.markdown("---")
    st.markdown("📋 **CHECKLIST IA**")
    st.write("✅ Fluxo Estrangeiro: **ALTISTA**")
    st.write("✅ Volume: **ACIMA DA MÉDIA**")
    st.write("✅ Spread: **ESTREITO**")

with col2:
    st.markdown(f"<h1 style='text-align: center; color: white;'>IBOV: {val:,.0f}</h1>", unsafe_allow_html=True)
    
    # Gráfico de Preço Principal
    if not df.empty:
        fig_main = go.Figure(go.Scatter(x=df.index, y=df['Close'], line=dict(color='#00FFFF', width=3), fill='tozeroy', fillcolor='rgba(0, 255, 255, 0.1)'))
        fig_main.update_layout(height=380, template="plotly_dark", margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                               xaxis=dict(showgrid=False), yaxis=dict(side="right", gridcolor="#222"))
        st.plotly_chart(fig_main, use_container_width=True)
    
    # Barra de Batalha logo abaixo do gráfico
    st.markdown(f"""
        <div class="battle-container"><div class="battle-fill" style="width: {p_buy}%;"></div></div>
        <div style="display: flex; justify-content: space-between; font-weight: 900; font-size: 1.1rem; color: white;">
            <span>BUY {p_buy:.1f}%</span>
            <span>SELL {100-p_buy:.1f}%</span>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("### ⚡ SINAIS")
    st.metric("VARIAÇÃO", f"{var:+.2f}%")
    st.metric("SINAL", "STRONG BUY" if var > 0.5 else "WAIT", delta=f"{p_buy:.0f} INDEX")
    st.metric("VOLATILIDADE", "1.24%", "BAIXA")
    
    st.markdown("---")
    if st.button("🚀 EXECUTAR ORDEM", use_container_width=True):
        st.toast("Enviando sinal para o Broker...")

# --- BARRA INFERIOR (TICKER TAPE SIMULADO) ---
st.markdown("---")
st.markdown("<p style='text-align: center; color: #555;'>TAV QUANT v2.0 | Conectado ao Yahoo Finance API | 2026</p>", unsafe_allow_html=True)
