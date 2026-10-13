
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

# =========================
# CONFIGURAÇÃO DA PÁGINA
# =========================
st.set_page_config(
    page_title="IHM Industrial | Motor M3",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================
# CSS
# =========================
st.html("""
<style>
:root {
    --bg: #0b0f14;
    --panel: #111821;
    --panel-2: #151e28;
    --border: #243140;
    --text: #eef3f7;
    --muted: #8ea0b3;
    --blue: #2f7df6;
    --green: #2ecc71;
    --yellow: #f1c40f;
    --red: #ff5d5d;
    --gray: #7f8c8d;
}

html, body, [class*="css"] {
    font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

.stApp {
    background:
        linear-gradient(rgba(255,255,255,.018) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,.018) 1px, transparent 1px),
        radial-gradient(circle at 15% 0%, rgba(47,125,246,.10), transparent 30%),
        radial-gradient(circle at 85% 20%, rgba(46,204,113,.045), transparent 28%),
        linear-gradient(145deg, #090d12 0%, #0d131a 45%, #0a0f15 100%);
    background-size:
        32px 32px,
        32px 32px,
        auto,
        auto,
        auto;
    color: var(--text);
}

.stApp::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 6px;
    z-index: 9999;
    background:
        repeating-linear-gradient(
            135deg,
            #f2c94c 0 18px,
            #f2c94c 18px 22px,
            #121820 22px 40px
        );
    opacity: .85;
}

.block-container::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    background:
        linear-gradient(115deg, transparent 0%, rgba(255,255,255,.012) 38%, transparent 62%),
        repeating-linear-gradient(
            0deg,
            rgba(255,255,255,.008) 0px,
            rgba(255,255,255,.008) 1px,
            transparent 1px,
            transparent 4px
        );
    mix-blend-mode: screen;
    opacity: .45;
}

.block-container {
    max-width: 1600px;
    padding-top: 1.1rem;
    padding-bottom: 2rem;
}

[data-testid="stSidebar"] {
    background:
        linear-gradient(180deg, rgba(18,25,34,.98), rgba(10,15,21,.99)),
        #0f151d;
    border-right: 1px solid #2b3948;
    box-shadow: 12px 0 30px rgba(0,0,0,.22);
}

[data-testid="stSidebar"] .block-container {
    padding-top: 1.2rem;
}

h1, h2, h3 {
    letter-spacing: -0.02em;
}

.header-wrap {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 1rem;
    margin-bottom: .5rem;
}

.title {
    font-size: clamp(1.8rem, 3vw, 3.2rem);
    font-weight: 800;
    line-height: 1.02;
    margin: 0;
}

.subtitle {
    color: var(--muted);
    margin-top: .55rem;
    font-size: .98rem;
}

.top-badges {
    display: flex;
    gap: .5rem;
    flex-wrap: wrap;
    justify-content: flex-end;
}

.badge {
    padding: .38rem .62rem;
    border-radius: 999px;
    border: 1px solid var(--border);
    background: #101720;
    color: var(--text);
    font-size: .78rem;
    white-space: nowrap;
}

.card {
    background: linear-gradient(180deg, rgba(21,30,40,.98), rgba(16,23,32,.98));
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 1rem 1.05rem;
    box-shadow: 0 10px 35px rgba(0,0,0,.18);
    height: 100%;
}

.card-title {
    color: var(--muted);
    font-size: .82rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .08em;
    margin-bottom: .4rem;
}

.metric-value {
    font-size: 2rem;
    font-weight: 800;
    line-height: 1;
    margin: .15rem 0 .55rem 0;
}

.metric-unit {
    font-size: .95rem;
    color: var(--muted);
    font-weight: 600;
}

.status-pill {
    display: inline-flex;
    align-items: center;
    gap: .4rem;
    padding: .35rem .62rem;
    border-radius: 999px;
    font-size: .78rem;
    font-weight: 700;
    border: 1px solid currentColor;
}

.motor-card {
    border: 1px solid #2f7df6;
    background:
        linear-gradient(135deg, rgba(47,125,246,.18), rgba(47,125,246,.05)),
        linear-gradient(180deg, rgba(21,30,40,.98), rgba(16,23,32,.98));
    border-radius: 22px;
    padding: 1.25rem;
    box-shadow: 0 16px 40px rgba(47,125,246,.12);
}

.motor-name {
    font-size: 1.45rem;
    font-weight: 800;
    margin-bottom: .3rem;
}

.motor-sub {
    color: var(--muted);
    margin-bottom: 1rem;
}

.health-wrap {
    background: #0f151d;
    border: 1px solid var(--border);
    border-radius: 999px;
    height: 14px;
    overflow: hidden;
}

.health-bar {
    height: 100%;
    border-radius: 999px;
}

.section-title {
    font-size: 1.2rem;
    font-weight: 800;
    margin: .65rem 0 .8rem 0;
}

.ai-box {
    border-radius: 18px;
    padding: 1.05rem;
    border: 1px solid var(--border);
    background: linear-gradient(180deg, rgba(17,24,33,.98), rgba(14,20,28,.98));
}

.small {
    color: var(--muted);
    font-size: .84rem;
}

.rule {
    height: 1px;
    background: var(--border);
    margin: 1.1rem 0;
}

.alert-item {
    border: 1px solid var(--border);
    border-left-width: 4px;
    border-radius: 12px;
    padding: .78rem .85rem;
    margin-bottom: .55rem;
    background: #0f151d;
}

.log-row {
    display: grid;
    grid-template-columns: 72px 1fr;
    gap: .6rem;
    padding: .55rem 0;
    border-bottom: 1px solid rgba(36,49,64,.7);
}

.sidebar-title {
    font-size: 1.12rem;
    font-weight: 800;
    margin-bottom: .15rem;
}

.sidebar-sub {
    color: var(--muted);
    font-size: .84rem;
    margin-bottom: .9rem;
}

div[data-testid="stMetric"] {
    background: #111821;
    border: 1px solid var(--border);
    padding: .8rem;
    border-radius: 14px;
}

.stSlider [data-baseweb="slider"] {
    margin-top: .2rem;
}

footer {visibility: hidden;}
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
</style>
""")

# =========================
# FUNÇÕES
# =========================
def html(content):
    """Renderiza HTML/CSS sem o parser Markdown interferir no conteúdo."""
    st.html(content)

def classify_temp(v):
    if v < 70:
        return "NORMAL", "#2ecc71"
    if v < 80:
        return "ATENÇÃO", "#f1c40f"
    return "CRÍTICO", "#ff5d5d"

def classify_vib(v):
    if v < 4.5:
        return "NORMAL", "#2ecc71"
    if v < 7.1:
        return "ATENÇÃO", "#f1c40f"
    return "CRÍTICO", "#ff5d5d"

def classify_rpm(v):
    if 1450 <= v <= 1850:
        return "NORMAL", "#2ecc71"
    if 1200 <= v <= 2100:
        return "ATENÇÃO", "#f1c40f"
    return "CRÍTICO", "#ff5d5d"

def classify_hours(v):
    if v < 800:
        return "NORMAL", "#2ecc71"
    if v < 1200:
        return "ATENÇÃO", "#f1c40f"
    return "CRÍTICO", "#ff5d5d"

def system_state(states):
    if "CRÍTICO" in states:
        return "CRÍTICO", "#ff5d5d", "✕"
    if "ATENÇÃO" in states:
        return "ATENÇÃO", "#f1c40f", "⚠"
    return "NORMAL", "#2ecc71", "●"

def calc_health(temp, vib, rpm, hours):
    penalties = 0
    penalties += max(0, temp - 60) * 0.65
    penalties += max(0, vib - 2.5) * 4.5
    penalties += abs(rpm - 1700) / 40
    penalties += max(0, hours - 500) / 45
    return int(np.clip(round(100 - penalties), 25, 100))

def trend_text(series):
    d = series[-1] - series[-5]
    if d > 0.8:
        return "↑ Subindo"
    if d < -0.8:
        return "↓ Caindo"
    return "→ Estável"

def metric_card(icon, label, value, unit, status, color, trend, limits):
    symbol = "●" if status == "NORMAL" else "⚠" if status == "ATENÇÃO" else "✕"
    html(f"""<div class="card">
        <div class="card-title">{icon} {label}</div>
        <div class="metric-value">{value} <span class="metric-unit">{unit}</span></div>
        <div class="status-pill" style="color:{color};">{symbol} {status}</div>
        <div style="margin-top:.65rem;font-size:.88rem;">{trend}</div>
        <div class="small" style="margin-top:.45rem;">{limits}</div>
    </div>""")

def make_history(temp, vib, rpm, hours, n=36):
    rng = np.random.default_rng(12)
    times = [datetime.now() - timedelta(minutes=5*(n-i-1)) for i in range(n)]
    temp_series = np.linspace(temp-3, temp, n) + rng.normal(0, 0.55, n)
    vib_series = np.linspace(max(0.4, vib-0.7), vib, n) + rng.normal(0, 0.16, n)
    rpm_series = np.linspace(rpm-35, rpm, n) + rng.normal(0, 14, n)
    hours_series = np.linspace(max(0, hours-6), hours, n)
    return times, temp_series, vib_series, rpm_series, hours_series

def line_chart(x, y, title, unit, attention=None, critical=None):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=y, mode="lines",
        line=dict(width=3),
        hovertemplate=f"%{{y:.2f}} {unit}<extra></extra>"
    ))
    if attention is not None:
        fig.add_hline(y=attention, line_dash="dash", annotation_text="Atenção")
    if critical is not None:
        fig.add_hline(y=critical, line_dash="dash", annotation_text="Crítico")
    fig.update_layout(
        title=title,
        margin=dict(l=10, r=10, t=42, b=10),
        height=290,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#dce6ee"),
        xaxis=dict(showgrid=False),
        yaxis=dict(gridcolor="rgba(255,255,255,.08)", zeroline=False),
        hovermode="x unified",
    )
    return fig

# =========================
# SIDEBAR / SIMULAÇÃO
# =========================
with st.sidebar:
    html('<div class="sidebar-title">🎛️ Painel de Simulação</div>')
    html('<div class="sidebar-sub">Ajuste os sensores para testar estados, alertas e diagnóstico.</div>')

    temp = st.slider("🌡️ Temperatura da Carcaça (°C)", 20.0, 100.0, 64.5, 0.5)
    vib = st.slider("〰️ Vibração Global RMS (mm/s)", 0.0, 12.0, 3.5, 0.1)
    hours = st.slider("⏱️ Horas Acumuladas de Operação", 0, 1600, 570, 10)
    rpm = st.slider("⚡ Velocidade de Rotação (RPM)", 500, 3000, 1700, 50)

    st.markdown("---")
    st.caption("Faixas de referência")
    st.caption("Temperatura: normal < 70 °C | crítico ≥ 80 °C")
    st.caption("Vibração: normal < 4,5 mm/s | crítico ≥ 7,1 mm/s")
    st.caption("RPM nominal: 1450–1850 RPM")

# =========================
# ESTADOS
# =========================
temp_state, temp_color = classify_temp(temp)
vib_state, vib_color = classify_vib(vib)
rpm_state, rpm_color = classify_rpm(rpm)
hours_state, hours_color = classify_hours(hours)

overall, overall_color, overall_icon = system_state(
    [temp_state, vib_state, rpm_state, hours_state]
)

health = calc_health(temp, vib, rpm, hours)

# diagnóstico tipo árvore de decisão
if vib >= 7.1:
    diagnosis = "FALHA POTENCIAL"
    confidence = 97
    reason = "Vibração em faixa crítica, com forte indicação de anomalia mecânica."
    recommendation = "Inspecionar rolamentos, alinhamento do eixo e fixações antes de manter operação contínua."
elif temp >= 80:
    diagnosis = "FALHA POTENCIAL"
    confidence = 95
    reason = "Temperatura da carcaça acima da faixa crítica."
    recommendation = "Verificar ventilação, carga, corrente do motor e condições térmicas."
elif vib >= 4.5 or temp >= 70 or rpm_state == "ATENÇÃO" or hours_state == "ATENÇÃO":
    diagnosis = "ATENÇÃO"
    confidence = 89
    reason = "Uma ou mais variáveis estão próximas ou acima da faixa recomendada."
    recommendation = "Manter monitoramento reforçado e programar inspeção preventiva."
else:
    diagnosis = "NORMAL"
    confidence = 94
    reason = "Temperatura, vibração e rotação permanecem dentro das faixas operacionais."
    recommendation = "Manter operação e rotina normal de monitoramento."

times, temp_hist, vib_hist, rpm_hist, hours_hist = make_history(temp, vib, rpm, hours)

# influência ilustrativa
raw_imp = np.array([
    1.2 + max(0, vib - 2),
    1.0 + max(0, temp - 55)/8,
    0.8 + abs(rpm-1700)/300,
    0.7 + hours/1200
], dtype=float)
imp = raw_imp / raw_imp.sum() * 100

# =========================
# CABEÇALHO
# =========================
now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
html(f"""<div class="header-wrap">
    <div>
        <div class="title">🏭 IHM — Monitoramento Inteligente</div>
        <div class="subtitle">Planta de Testes Supervisórios | SENAI • Motor Elétrico M3</div>
    </div>
    <div class="top-badges">
        <div class="badge">🟢 Sistema ONLINE</div>
        <div class="badge">📡 Sensores 4/4</div>
        <div class="badge">🤖 IA ATIVA</div>
        <div class="badge">🕒 {now}</div>
    </div>
</div>""")
html('<div class="rule"></div>')

# =========================
# BLOCO PRINCIPAL
# =========================
left, right = st.columns([1.15, 1.85], gap="large")

with left:
    html('<div class="section-title">⚙️ Estado Geral do Ativo</div>')
    html(f"""<div class="motor-card">
        <div class="motor-name">⚙️ MOTOR ELÉTRICO M3</div>
        <div class="motor-sub">Ativo principal monitorado em tempo real</div>
        <div class="status-pill" style="color:{overall_color}; font-size:.9rem; margin-bottom:1rem;">
            {overall_icon} OPERAÇÃO {overall}
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:.85rem;margin-top:.5rem;">
            <div><div class="small">Temperatura</div><b>{temp:.1f} °C</b></div>
            <div><div class="small">Vibração RMS</div><b>{vib:.1f} mm/s</b></div>
            <div><div class="small">Rotação</div><b>{rpm} RPM</b></div>
            <div><div class="small">Operação</div><b>{hours} h</b></div>
        </div>
        <div style="margin-top:1.1rem;display:flex;justify-content:space-between;">
            <b>Saúde do equipamento</b><b>{health}%</b>
        </div>
        <div class="health-wrap" style="margin-top:.45rem;">
            <div class="health-bar" style="width:{health}%;background:{overall_color};"></div>
        </div>
    </div>""")

with right:
    html('<div class="section-title">📊 Leituras Atuais dos Sensores</div>')
    c1, c2 = st.columns(2)
    with c1:
        metric_card("🌡️", "Temperatura da Carcaça", f"{temp:.1f}", "°C", temp_state, temp_color,
                    trend_text(temp_hist), "Normal < 70 °C • Crítico ≥ 80 °C")
    with c2:
        metric_card("〰️", "Vibração Global RMS", f"{vib:.1f}", "mm/s", vib_state, vib_color,
                    trend_text(vib_hist), "Normal < 4,5 • Crítico ≥ 7,1 mm/s")

    st.write("")
    c3, c4 = st.columns(2)
    with c3:
        metric_card("⏱️", "Horas de Operação", f"{hours}", "h", hours_state, hours_color,
                    "→ Acumulativo", "Atenção ≥ 800 h • Crítico ≥ 1200 h")
    with c4:
        metric_card("⚡", "Velocidade de Rotação", f"{rpm}", "RPM", rpm_state, rpm_color,
                    trend_text(rpm_hist), "Faixa nominal: 1450–1850 RPM")

# =========================
# IA
# =========================
html('<div class="section-title">🤖 Diagnóstico Inteligente</div>')

ai1, ai2 = st.columns([1.5, 1], gap="large")

with ai1:
    diag_color = "#2ecc71" if diagnosis == "NORMAL" else "#f1c40f" if diagnosis == "ATENÇÃO" else "#ff5d5d"
    html(f"""<div class="ai-box">
        <div class="card-title">Árvore de Decisão • Resultado Atual</div>
        <div style="display:flex;justify-content:space-between;gap:1rem;align-items:center;">
            <div>
                <div style="font-size:1.8rem;font-weight:800;color:{diag_color};">{diagnosis}</div>
                <div class="small">Confiança estimada: {confidence}%</div>
            </div>
            <div class="status-pill" style="color:{diag_color};">{overall_icon} {overall}</div>
        </div>
        <div class="rule"></div>
        <b>Motivo da decisão</b>
        <div class="small" style="margin-top:.35rem;">{reason}</div>
        <div style="margin-top:.9rem;"><b>Recomendação</b></div>
        <div class="small" style="margin-top:.35rem;">{recommendation}</div>
    </div>""")

with ai2:
    imp_df = pd.DataFrame({
        "Variável": ["Vibração", "Temperatura", "RPM", "Horas"],
        "Influência (%)": imp
    }).sort_values("Influência (%)", ascending=True)

    fig_imp = go.Figure(go.Bar(
        x=imp_df["Influência (%)"],
        y=imp_df["Variável"],
        orientation="h",
        text=[f"{v:.0f}%" for v in imp_df["Influência (%)"]],
        textposition="auto"
    ))
    fig_imp.update_layout(
        title="Por que a IA tomou essa decisão?",
        margin=dict(l=10, r=10, t=44, b=10),
        height=260,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#dce6ee"),
        xaxis=dict(showgrid=False, visible=False),
        yaxis=dict(showgrid=False),
    )
    st.plotly_chart(fig_imp, width='stretch', config={"displayModeBar": False})

# =========================
# ALERTAS E EVENTOS
# =========================
html('<div class="section-title">🚨 Alertas e Eventos</div>')
a1, a2 = st.columns([1, 1.4], gap="large")

with a1:
    alerts = []
    if temp_state != "NORMAL":
        alerts.append(("Temperatura", temp_state, temp_color, f"{temp:.1f} °C"))
    if vib_state != "NORMAL":
        alerts.append(("Vibração", vib_state, vib_color, f"{vib:.1f} mm/s"))
    if rpm_state != "NORMAL":
        alerts.append(("Rotação", rpm_state, rpm_color, f"{rpm} RPM"))
    if hours_state != "NORMAL":
        alerts.append(("Horas de operação", hours_state, hours_color, f"{hours} h"))

    alert_html = '<div class="card"><div class="card-title">Alertas Ativos</div>'
    if not alerts:
        alert_html += (
            '<div class="alert-item" style="border-left-color:#2ecc71;">'
            '✅ <b>Nenhum alerta ativo.</b><br>'
            '<span class="small">Todos os parâmetros estão dentro da faixa normal.</span>'
            '</div>'
        )
    else:
        for name, state, color, value in alerts:
            alert_html += (
                f'<div class="alert-item" style="border-left-color:{color};">'
                f'<b>{state}: {name}</b><br>'
                f'<span class="small">Valor atual: {value}</span>'
                '</div>'
            )
    alert_html += '</div>'
    html(alert_html)

with a2:
    events = []
    hh = datetime.now()
    events.append((hh.strftime("%H:%M"), f"Diagnóstico atualizado: {diagnosis}."))
    if vib_state != "NORMAL":
        events.append(((hh - timedelta(minutes=2)).strftime("%H:%M"), f"Vibração entrou em estado {vib_state.lower()}."))
    if temp_state != "NORMAL":
        events.append(((hh - timedelta(minutes=4)).strftime("%H:%M"), f"Temperatura entrou em estado {temp_state.lower()}."))
    events.append(((hh - timedelta(minutes=6)).strftime("%H:%M"), "Pacote de sensores recebido com sucesso."))
    events.append(((hh - timedelta(minutes=10)).strftime("%H:%M"), "Motor M3 em monitoramento contínuo."))

    log_html = '<div class="card"><div class="card-title">Log de Eventos</div>'
    for tm, msg in events:
        log_html += f'<div class="log-row"><b>{tm}</b><span class="small">{msg}</span></div>'
    log_html += '</div>'
    html(log_html)

# =========================
# HISTÓRICO
# =========================
html('<div class="section-title">📈 Histórico e Tendências</div>')

g1, g2 = st.columns(2)
with g1:
    st.plotly_chart(
        line_chart(times, temp_hist, "Temperatura da Carcaça", "°C", 70, 80),
        width='stretch',
        config={"displayModeBar": False}
    )
with g2:
    st.plotly_chart(
        line_chart(times, vib_hist, "Vibração Global RMS", "mm/s", 4.5, 7.1),
        width='stretch',
        config={"displayModeBar": False}
    )

g3, g4 = st.columns(2)
with g3:
    st.plotly_chart(
        line_chart(times, rpm_hist, "Velocidade de Rotação", "RPM", 1450, 2100),
        width='stretch',
        config={"displayModeBar": False}
    )
with g4:
    fig_h = line_chart(times, hours_hist, "Horas Acumuladas", "h", 800, 1200)
    st.plotly_chart(fig_h, width='stretch', config={"displayModeBar": False})

st.caption("Protótipo de IHM para fins educacionais • Monitoramento preditivo • SENAI")
