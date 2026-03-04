import numpy as np
from streamlit_autorefresh import st_autorefresh

# 1. Configuração de Página
st.set_page_config(page_title="TAV QUANT | ULTRA VISION", layout="wide")
# 1. Configuração de Página (Forçar ocupação total da tela)
st.set_page_config(page_title="TAV QUANT | COCKPIT", layout="wide", initial_sidebar_state="collapsed")

# Atualização automática a cada 30 segundos
# Auto-update (30s)
st_autorefresh(interval=30 * 1000, key="datarefresh")

# --- CSS PARA ACENDER O PAINEL (MÁXIMO CONTRASTE) ---
# --- CSS PARA DISTRIBUIÇÃO E BRILHO ---
st.markdown("""
   <style>
    /* Fundo Total Black para destacar o que brilha */
   [data-testid="stAppViewContainer"] { background-color: #000000; color: #FFFFFF; }
   
    /* CARDS DE MÉTRICA: Fundo Grafite escuro com bordas Brancas */
    /* Remover espaços em branco excessivos no topo */
    .block-container { padding-top: 1rem !important; padding-bottom: 0rem !important; }
    
    /* Estilização das métricas para ficarem compactas e brilhantes */
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
        background-color: #111111 !important;
        border: 1px solid #00FFFF !important;
        border-radius: 5px !important;
        padding: 10px !important;
        text-align: center;
   }

    /* TEXTOS DE VARIAÇÃO (DELTA) */
    [data-testid="stMetricDelta"] { font-size: 1.2rem !important; font-weight: 700 !important; }
    [data-testid="stMetricLabel"] { color: #00FFFF !important; font-size: 0.9rem !important; font-weight: bold !important; }
    [data-testid="stMetricValue"] { color: #FFFFFF !important; font-size: 1.8rem !important; font-weight: 900 !important; }

    /* TITULOS GERAIS */
    h1, h2, h3 { color: #FFFFFF !important; font-weight: 900 !important; text-transform: uppercase; }

    /* BARRA DE BATALHA: Mais Alta e Vibrante */
    .battle-container { width: 100%; background: #440000; height: 50px; border-radius: 12px; border: 2px solid #555; margin: 20px 0; }
    .battle-fill { background: #00FF88; height: 100%; box-shadow: 0 0 30px #00FF88; border-radius: 10px 0 0 10px; transition: 1s; }
    /* Barra de Batalha Estilizada */
    .battle-container { width: 100%; background: #330000; height: 35px; border-radius: 5px; border: 1px solid #555; margin-top: 10px; }
    .battle-fill { background: #00FF88; height: 100%; box-shadow: 0 0 15px #00FF88; border-radius: 4px 0 0 4px; }
   
    /* TEXTOS DOS CRITÉRIOS */
    .stMarkdown p { color: #FFFFFF !important; font-size: 1.2rem !important; font-weight: 600 !important; }
    /* Esconder o menu do Streamlit para parecer um software nativo */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
   </style>
   """, unsafe_allow_html=True)

# 2. Coleta de Dados Segura
# 2. Coleta de Dados
@st.cache_data(ttl=30)
def get_live_data():
def get_data():
try:
        ticker = yf.Ticker("^BVSP")
        df = ticker.history(period='1d', interval='5m')
        tk = yf.Ticker("^BVSP")
        df = tk.history(period='1d', interval='5m')
if not df.empty:
atual = float(df['Close'].iloc[-1])
            hist = ticker.history(period='2d')
            prev = float(hist['Close'].iloc[-2]) if len(hist) > 1 else atual
            prev = float(tk.history(period='2d')['Close'].iloc[-2])
var = ((atual / prev) - 1) * 100
return df, atual, var
    except:
        pass
    except: pass
return pd.DataFrame(), 0.0, 0.0

df_ibov, valor_ibov, var_ibov = get_live_data()

# --- TOPO: MÉTRICAS ACESAS ---
st.title("🛡️ TAV QUANT | INTELLIGENCE SYSTEM")

c1, c2, c3, c4, c5 = st.columns(5)

# Formatação para evitar erro de tipo
val_display = f"{valor_ibov:,.0f}" if valor_ibov > 0 else "OFFLINE"
var_display = f"{var_ibov:+.2f}%" if var_ibov != 0 else "0.00%"
df, val, var = get_data()

c1.metric("IBOVESPA", val_display, var_display)
c2.metric("SINAL IA", "BULLISH" if var_ibov >= 0 else "BEARISH", "FORTE")
c3.metric("VOLATILIDADE", "18.4%", "NORMAL", delta_color="off")
c4.metric("PROB. SUCESSO", "92%", "ALTA", delta_color="off")
c5.metric("QUANT INDEX", "78", "BUY ZONE", delta_color="off")
# --- LAYOUT DE TRÊS COLUNAS (O COCKPIT) ---
# Coluna 1: Gauges e Checklist (Esquerda)
# Coluna 2: Preço e Batalha (Centro - Maior)
# Coluna 3: Métricas e Sinais (Direita)

# --- CORPO: GRÁFICO E BATALHA ---
st.divider()
col_left, col_mid, col_right = st.columns([1, 2, 1])
col1, col2, col3 = st.columns([1, 2, 1])

with col_mid:
    st.subheader("⚔️ DISPUTA DE AGRESSÃO (MOMENTUM)")
    
    # Cálculo visual da barra
    p_buy = 50 + (var_ibov * 10) if var_ibov != 0 else 50
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
        <div class="battle-container">
            <div class="battle-fill" style="width: {p_buy}%;"></div>
        </div>
        <div style="display: flex; justify-content: space-between; font-weight: 900; font-size: 1.5rem;">
            <span style="color: #00FF88; text-shadow: 2px 2px 4px #000;">BUY {p_buy:.1f}%</span>
            <span style="color: #FF3333; text-shadow: 2px 2px 4px #000;">SELL {100-p_buy:.1f}%</span>
        <div class="battle-container"><div class="battle-fill" style="width: {p_buy}%;"></div></div>
        <div style="display: flex; justify-content: space-between; font-weight: 900; font-size: 1.1rem; color: white;">
            <span>BUY {p_buy:.1f}%</span>
            <span>SELL {100-p_buy:.1f}%</span>
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
with col3:
    st.markdown("### ⚡ SINAIS")
    st.metric("VARIAÇÃO", f"{var:+.2f}%")
    st.metric("SINAL", "STRONG BUY" if var > 0.5 else "WAIT", delta=f"{p_buy:.0f} INDEX")
    st.metric("VOLATILIDADE", "1.24%", "BAIXA")
    
    st.markdown("---")
    if st.button("🚀 EXECUTAR ORDEM", use_container_width=True):
        st.toast("Enviando sinal para o Broker...")

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
# --- BARRA INFERIOR (TICKER TAPE SIMULADO) ---
st.markdown("---")
st.markdown("<p style='text-align: center; color: #555;'>TAV QUANT v2.0 | Conectado ao Yahoo Finance API | 2026</p>", unsafe_allow_html=True)
