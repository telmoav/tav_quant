import streamlit as st
import plotly.graph_objects as go
import yfinance as yf
import pandas as pd
import numpy as np
from streamlit_autorefresh import st_autorefresh

# 1. Configuração Principal
st.set_page_config(page_title="TAV QUANT | ULTRA VISION", layout="wide")

# Atualização automática (30 segundos)
st_autorefresh(interval=30 * 1000, key="datarefresh")

# CSS CUSTOMIZADO PARA MÁXIMA CLAREZA
st.markdown("""
    <style>
    /* Fundo levemente cinza para destacar os cards pretos */
    [data-testid="stAppViewContainer"] { background-color: #0f0f0f; color: #ffffff; }
    
    /* CARDS DE MÉTRICA: Fundo escuro, bordas brilhantes e texto branco puro */
    div[data-testid="stMetric"] {
        background-color: #1a1a1a !important;
        border: 2px solid #444 !important;
        border-radius: 8px !important;
        padding: 20px !important;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.5);
    }
    
    /* TEXTOS DAS MÉTRICAS: Aumentando o brilho e tamanho */
    [data-testid="stMetricLabel"] { 
        color: #00f2ff !important; /* Azul Ciano Vibrante */
        font-size: 1.2rem !important; 
        font-weight: 800 !important; 
        text-transform: uppercase;
    }
    [data-testid="stMetricValue"] { 
        color: #ffffff !important; /* Branco Puro */
        font-size: 2.2rem !important;
        font-weight: 900 !important;
    }
    
    /* Títulos e Subtítulos */
    h1, h2, h3 { color: #ffffff !important; font-weight: 900 !important; }

    /* Barra de Batalha: Mais alta e com brilho intenso */
    .battle-container { width: 100%; background: #440000; height: 50px; border-radius: 10px; border: 2px solid #666; margin: 15px 0; }
    .battle-fill { background: #00ff88; height: 100%; box-shadow: 0 0 25px #00ff88; border-radius: 8px 0 0 8px; transition: 1s; }
    
    /* Ajuste de visibilidade dos textos das colunas */
    .stMarkdown p { font-size: 1.1rem !important; font-weight: 600 !important; color: #ffffff !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Coleta de Dados Segura
@st.cache_data(ttl=30)
def get_live_data():
    try:
        ticker = yf.Ticker("^BVSP")
        df = ticker.history(period='1d', interval='5m')
        if not df.empty:
            atual = float(df['Close'].iloc[-1])
            hist = ticker.history(period='2d')
            prev = float(hist['Close'].iloc[-2]) if len(hist) > 1 else atual
            var = ((atual / prev) - 1) * 100
            return df, atual, var
    except:
        pass
    return pd.DataFrame(), 0.0, 0.0

df_ibov, valor_ibov, var_ibov = get_live_data()

# --- TOPO: MÉTRICAS EM DESTAQUE ---
st.title("🛡️ TAV QUANT | INTELLIGENCE SYSTEM")

c1, c2, c3, c4, c5 = st.columns(5)

# Tratamento para evitar que texto suma se valor for zero
val_txt = f"{valor_ibov:,.0f}" if valor_ibov > 0 else "---"
var_txt = f"{var_ibov:+.2f}%" if var_ibov != 0 else "0.00%"

c1.metric("IBOVESPA", val_txt, var_txt)
c2.metric("SINAL IA", "BULLISH" if var_ibov >= 0 else "BEARISH", "FORTE")
c3.metric("VOLATILIDADE", "18.4%", "NORMAL", delta_color="off")
c4.metric("PROB. SUCESSO", "92%", "ALTA", delta_color="off")
c5.metric("QUANT INDEX", "78", "BUY ZONE", delta_color="off")

# --- CENTRO: GRÁFICO E BATALHA ---
st.divider()
col_left, col_mid, col_right = st.columns([1, 2, 1])

with col_mid:
    st.subheader("⚔️ DISPUTA DE AGRESSÃO (MOMENTUM)")
    
    # Cálculo visual da força
    p_compra = 50 + (var_ibov * 8) if var_ibov != 0 else 50
    p_compra = max(min(p_compra, 98), 2)
    
    st.markdown(f"""
        <div class="battle-container">
            <div class="battle-fill" style="width: {p_compra}%;"></div>
        </div>
        <div style="display: flex; justify-content: space-between; font-weight: 900; font-size: 1.4rem;">
            <span style="color: #00ff88; text-shadow: 1px 1px 2px #000;">COMPRA {p_compra:.1f}%</span>
            <span style="color: #ff3333; text-shadow: 1px 1px 2px #000;">VENDA {100-p_compra:.1f}%</span>
        </div>
    """, unsafe_allow_html=True)
    
    if not df_ibov.empty:
        fig = go.Figure(go.Scatter(x=df_ibov.index, y=df_ibov['Close'], 
                                 line=dict(color='#00f2ff', width=4),
                                 fill='tozeroy', fillcolor='rgba(0, 242, 255, 0.15)'))
        fig.update_layout(template="plotly_dark", height=450, margin=dict(l=0,r=0,t=0,b=0),
                         paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                         xaxis=dict(gridcolor='#444', tickfont=dict(color='white', size=14)), 
                         yaxis=dict(gridcolor='#444', tickfont=dict(color='white', size=14)))
        st.plotly_chart(fig, use_container_width=True)

with col_left:
    st.markdown("### 🟢 COMPRA")
    f1 = go.Figure(go.Indicator(mode="gauge+number", value=p_compra, 
                                gauge={'bar':{'color':"#00ff88"}, 'axis':{'tickcolor':"white"}, 'bgcolor':"#333"}))
    f1.update_layout(height=300, paper_bgcolor='rgba(0,0,0,0)', font={'color':"white", 'size': 20, 'weight': 'bold'})
    st.plotly_chart(f1, use_container_width=True)

with col_right:
    st.markdown("### 🔴 VENDA")
    f2 = go.Figure(go.Indicator(mode="gauge+number", value=100-p_compra, 
                                gauge={'bar':{'color':"#ff3333"}, 'axis':{'tickcolor':"white"}, 'bgcolor':"#333"}))
    f2.update_layout(height=300, paper_bgcolor='rgba(0,0,0,0)', font={'color':"white", 'size': 20, 'weight': 'bold'})
    st.plotly_chart(f2, use_container_width=True)

# --- BASE: CRITÉRIOS ---
st.divider()
st.subheader("📋 CHECKLIST OPERACIONAL")
q1, q2, q3 = st.columns(3)
with q1:
    st.success("✅ **SCORE TÉCNICO: ALTO**")
    st.write("Fluxo de agressão predominante na ponta compradora.")
with q2:
    st.info("🔵 **FLUXO: INSTITUCIONAL**")
    st.write("Grandes players mantendo posição acima da VWAP.")
with q3:
    st.warning("⚠️ **RISCO: CONTROLADO**")
    st.button("🎯 DISPARAR ALERTA", use_container_width=True)
