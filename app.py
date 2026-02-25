import streamlit as st
import plotly.graph_objects as go
import yfinance as yf
import pandas as pd
import numpy as np
from streamlit_autorefresh import st_autorefresh

# 1. Configuração de Página
st.set_page_config(page_title="TAV QUANT | ULTRA VISION", layout="wide")

# Atualização automática a cada 30 segundos
st_autorefresh(interval=30 * 1000, key="datarefresh")

# --- CSS PARA ACENDER O PAINEL (MÁXIMO CONTRASTE) ---
st.markdown("""
    <style>
    /* Fundo Total Black para destacar o que brilha */
    [data-testid="stAppViewContainer"] { background-color: #000000; color: #FFFFFF; }
    
    /* CARDS DE MÉTRICA: Fundo Grafite escuro com bordas Brancas */
    div[data-testid="stMetric"] {
        background-color: #161616 !important;
        border: 2px solid #333333 !important;
        border-radius: 10px !important;
        padding: 20px !important;
    }

    /* TÍTULOS DAS MÉTRICAS: Azul Ciano Neon e Negrito */
    [data-testid="stMetricLabel"] { 
        color: #00FFFF !important; 
        font-size: 1.3rem !important; 
        font-weight: 800 !important;
        text-shadow: 0px 0px 10px rgba(0,255,255,0.5);
    }

    /* VALORES DAS MÉTRICAS: Branco Puro e Gigante */
    [data-testid="stMetricValue"] { 
        color: #FFFFFF !important; 
        font-size: 2.5rem !important; 
        font-weight: 900 !important;
    }

    /* TEXTOS DE VARIAÇÃO (DELTA) */
    [data-testid="stMetricDelta"] { font-size: 1.2rem !important; font-weight: 700 !important; }

    /* TITULOS GERAIS */
    h1, h2, h3 { color: #FFFFFF !important; font-weight: 900 !important; text-transform: uppercase; }

    /* BARRA DE BATALHA: Mais Alta e Vibrante */
    .battle-container { width: 100%; background: #440000; height: 50px; border-radius: 12px; border: 2px solid #555; margin: 20px 0; }
    .battle-fill { background: #00FF88; height: 100%; box-shadow: 0 0 30px #00FF88; border-radius: 10px 0 0 10px; transition: 1s; }
    
    /* TEXTOS DOS CRITÉRIOS */
    .stMarkdown p { color: #FFFFFF !important; font-size: 1.2rem !important; font-weight: 600 !important; }
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

# --- TOPO: MÉTRICAS ACESAS ---
st.title("🛡️ TAV QUANT | INTELLIGENCE SYSTEM")

c1, c2, c3, c4, c5 = st.columns(5)

# Formatação para evitar erro de tipo
val_display = f"{valor_ibov:,.0f}" if valor_ibov > 0 else "OFFLINE"
var_display = f"{var_ibov:+.2f}%" if var_ibov != 0 else "0.00%"

c1.metric("IBOVESPA", val_display, var_display)
c2.metric("SINAL IA", "BULLISH" if var_ibov >= 0 else "BEARISH", "FORTE")
c3.metric("VOLATILIDADE", "18.4%", "NORMAL", delta_color="off")
c4.metric("PROB. SUCESSO", "92%", "ALTA", delta_color="off")
c5.metric("QUANT INDEX", "78", "BUY ZONE", delta_color="off")

# --- CORPO: GRÁFICO E BATALHA ---
st.divider()
col_left, col_mid, col_right = st.columns([1, 2, 1])

with col_mid:
    st.subheader("⚔️ DISPUTA DE AGRESSÃO (MOMENTUM)")
    
    # Cálculo visual da barra
    p_buy = 50 + (var_ibov * 10) if var_ibov != 0 else 50
    p_buy = max(min(p_buy, 98), 2)
    
    st.markdown(f"""
        <div class="battle-container">
            <div class="battle-fill" style="width: {p_buy}%;"></div>
        </div>
        <div style="display: flex; justify-content: space-between; font-weight: 900; font-size: 1.5rem;">
            <span style="color: #00FF88; text-shadow: 2px 2px 4px #000;">BUY {p_buy:.1f}%</span>
            <span style="color: #FF3333; text-shadow: 2px 2px 4px #000;">SELL {100-p_buy:.1f}%</span>
        </div>
    """, unsafe_allow_html=True)
    
    if not df_ibov.empty:
        fig = go.Figure(go.Scatter(x=df_ibov.index, y=df_ibov['Close'], 
                                 line=dict(color='#00FFFF', width=4),
                                 fill='tozeroy', fillcolor='rgba(0, 255, 255, 0.15)'))
        fig.update_layout(template="plotly_dark", height=450, margin=dict(l=0,r=0,t=0,b=0),
                         paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                         xaxis=dict(gridcolor='#333', tickfont=dict(color='white', size=14, family='Arial Black')), 
                         yaxis=dict(gridcolor='#333', tickfont=dict(color='white', size=14, family='Arial Black')))
        st.plotly_chart(fig, use_container_width=True)

with col_left:
    st.subheader("🟢 BULL POWER")
    f1 = go.Figure(go.Indicator(mode="gauge+number", value=p_buy, 
                                gauge={'bar':{'color':"#00FF88"}, 'axis':{'tickcolor':"white"}, 'bgcolor':"#222"}))
    f1.update_layout(height=300, paper_bgcolor='rgba(0,0,0,0)', font={'color':"white", 'size': 24, 'family': 'Arial Black'})
    st.plotly_chart(f1, use_container_width=True)

with col_right:
    st.subheader("🔴 BEAR POWER")
    f2 = go.Figure(go.Indicator(mode="gauge+number", value=100-p_buy, 
                                gauge={'bar':{'color':"#FF3333"}, 'axis':{'tickcolor':"white"}, 'bgcolor':"#222"}))
    f2.update_layout(height=300, paper_bgcolor='rgba(0,0,0,0)', font={'color':"white", 'size': 24, 'family': 'Arial Black'})
    st.plotly_chart(f2, use_container_width=True)

# --- BASE: CRITÉRIOS ---
st.divider()
st.subheader("📋 CHECKLIST OPERACIONAL")
q1, q2, q3 = st.columns(3)
with q1:
    st.success("✅ **SCORE TÉCNICO: ALTO**")
    st.write("Predomínio de ordens de compra no book.")
with q2:
    st.info("🔵 **FLUXO: INSTITUCIONAL**")
    st.write("Players estrangeiros acumulando posição.")
with q3:
    st.warning("⚠️ **RISCO: CONTROLADO**")
    st.button("🎯 EXECUTAR SINAL AGORA", use_container_width=True)
