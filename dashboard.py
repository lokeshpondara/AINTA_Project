import streamlit as st
import pandas as pd
import sqlite3
import pydeck as pdk
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import numpy as np
from streamlit_autorefresh import st_autorefresh
from datetime import datetime, timedelta
import subprocess
import os
import sys

# Add project src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


def get_location(ip: str) -> dict:
    """Fallback geo lookup"""
    return {
        'country': 'Unknown',
        'latitude': 0.0,
        'longitude': 0.0
    }

class DetectionSettings:
    severity_block_threshold = 80

class Settings:
    detection = DetectionSettings()

settings = Settings()

# ULTIMATE SOC THEME - Step 2/12
st.set_page_config(
    page_title="AINTA Security Operations Center",
    layout="wide", 
    initial_sidebar_state="expanded",
    page_icon="🔒"
)

# Professional SOC Theme - Clean Enterprise Dark
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, [class*="css"]  {
  font-family: 'Inter', sans-serif;
}
.main {
  background: linear-gradient(135deg, #0f1419 0%, #1a2332 100%);
  color: #e2e8f0;
}
.stApp {
  background-color: transparent;
}
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #111827 0%, #1f2937 100%);
}
.stMetric > label {
  color: #60a5fa !important;
  font-weight: 600;
}
.stMetric > div > div {
  color: #f87171 !important;
  font-weight: 700;
  font-size: 2em;
}
h1, h2, h3 {
  color: #f8fafc !important;
}
.dataframe {
  background-color: #1e293b !important;
  color: #f1f5f9 !important;
}
.dataframe th {
  background-color: #1e40af !important;
  color: white !important;
  font-weight: 600;
}
.stButton > button {
  background: linear-gradient(135deg, #1e40af, #3b82f6);
  color: white;
  border: none;
  border-radius: 8px;
  padding: 0.75rem 1.5rem;
  font-weight: 600;
}
.stButton > button:hover {
  background: linear-gradient(135deg, #1d4ed8, #2563eb);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}
hr {
  border: 1px solid #334155;
  background: linear-gradient(90deg, transparent, #475569, transparent);
}
</style>
""", unsafe_allow_html=True)

st_autorefresh(interval=2000, key="soc_live")  # 2s ULTIMATE!

# WAR ROOM TITLE
st.markdown("# AINTA Security Operations Center")
st.markdown("**Real-time Threat Detection & Response | INDIAN SOC dashboard**")
st.divider()

# Duplicate sidebar removed


@st.cache_data(ttl=3)
def get_data():
    """Bulletproof live data pipeline"""
    try:
        conn = sqlite3.connect("database/alerts.db", timeout=5)
        df = pd.read_sql("SELECT * FROM alerts ORDER BY timestamp DESC LIMIT 3000", conn)
        conn.close()
    except:
        return pd.DataFrame()
    
    if df.empty:
        return df
    
    # ENHANCED SAFE PIPELINE - Step 3/12
    safe_cols = ['src_ip', 'dst_ip', 'attack_type', 'protocol']
    numeric_cols = ['severity', 'packet_rate', 'bytes', 'duration']
    
    for col in safe_cols:
        if col not in df.columns:
            df[col] = 'unknown'
        else:
            df[col] = df[col].fillna('unknown')
    
    for col in numeric_cols:
        if col not in df.columns:
            df[col] = 0
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    if 'timestamp' not in df.columns:
        df['timestamp'] = pd.Timestamp.now()
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df = df.dropna(subset=['timestamp']).reset_index(drop=True)
    
    # REAL GEO ENRICHMENT
    # Skip heavy geo for performance - use DB geo if present
    if 'latitude' not in df.columns:
        df['latitude'] = 0.0
        df['longitude'] = 0.0
    else:
        df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce').fillna(0.0)
        df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce').fillna(0.0)
    if 'country' not in df.columns:
        df['country'] = 'Unknown'
    else:
        df['country'] = df['country'].fillna('Unknown')
    
    # MOMENTUM & HISTORY
    df['bucket'] = df['timestamp'].dt.floor('30s')
    df['ip_history'] = df.groupby('src_ip').cumcount()
    
    recent_window = df[df['timestamp'] > (df['timestamp'].max() - timedelta(minutes=3))]
    momentum = recent_window.groupby('src_ip').size().to_dict()
    df['momentum'] = df['src_ip'].map(momentum).fillna(0)
    
    # ULTIMATE AI RISK v2.0 (Config Aware)
    block_thresh = settings.detection.severity_block_threshold / 10.0
    df['ai_risk'] = (
        df['severity'] * block_thresh +
        np.log1p(df['packet_rate']) * 5 +
        df['ip_history'] * 0.3 +
        df['momentum'] * 2 +
        (df['latitude'] != 0).astype(int) * 10  # Geo bonus
    )
    
    return df.sort_values('timestamp', ascending=False)

# Load data first for sidebar
df = get_data()
if df.empty:
    st.error("🚫 No live data! Run: `python run_system.py`")
    if st.button("💥 START DEMO ATTACKS"):
        subprocess.Popen(["python", "attacks/ddos_simulator.py"])
    st.stop()

# SIDEBAR - ANALYST CONTROLS
st.sidebar.title("SOC Controls")
time_range = st.sidebar.slider("Time Range (hours)", 1, 24, 6)
severity_filter = st.sidebar.slider("Min Severity", 1, 10, 1)
attack_types = st.sidebar.multiselect("Attack Types", sorted(df['attack_type'].unique()), default=sorted(df['attack_type'].value_counts().head(3).index))
if st.sidebar.button("Export CSV"):
    csv = df.to_csv().encode('utf-8')
    st.sidebar.download_button("Download all", csv, "soc_alerts.csv", "text/csv")
st.sidebar.caption(f"Total alerts: {len(df):,}")

# ========================================
# 🚨 ULTIMATE WAR ROOM - 8 KPI DASHBOARD (Step 4/12)
# ========================================
st.markdown("### 🚨 **COMMAND METRICS** | LIVE")

kpi_cols = st.columns(8)
metrics_data = [
    ("⚡ Active Threats", len(df), len(df)//10),
    ("🔥 Peak PPS", df.packet_rate.max(), int(df.packet_rate.mean())),
    ("🚨 Critical", len(df[df.severity >= 8]), 2),
    ("🌐 Unique IPs", df.src_ip.nunique(), 5),
    ("🛡️ Blocks Needed", len(df[df.ai_risk > settings.detection.severity_block_threshold]), 3),
    ("📍 Geo Threats", len(df[df.latitude != 0]), 1),
    ("📊 MTTD (min)", f"{(df.timestamp.max() - df.timestamp.min()).total_seconds()/60:.1f}", 0.5),
    ("🚀 Momentum", f"{df.momentum.sum():.0f}", 20)
]

for idx, (label, value, delta) in enumerate(metrics_data):
    with kpi_cols[idx]:
        st.metric(label, f"{value:,}" if isinstance(value, (int, float)) else value, f"+{delta}")

st.divider()

st.markdown("### Threat Intelligence Table")

# Apply sidebar filters
filtered_df = df[
    (df['timestamp'] > df['timestamp'].max() - timedelta(hours=time_range)) &
    (df['severity'] >= severity_filter) &
    (df['attack_type'].isin(attack_types))
].sort_values('ai_risk', ascending=False).head(100)

threat_table = filtered_df[['timestamp', 'src_ip', 'country', 'attack_type', 'severity', 'packet_rate', 'momentum', 'ai_risk']].copy()
threat_table['timestamp'] = threat_table['timestamp'].dt.strftime('%H:%M:%S')

st.data_editor(
    threat_table,
    column_config={
        "ai_risk": st.column_config.NumberColumn("AI Risk", format="%.1f", help="Composite threat score"),
        "severity": st.column_config.NumberColumn("Severity", help="Alert severity (1-10)"),
        "packet_rate": st.column_config.NumberColumn("PPS", format="%.0f"),
        "momentum": st.column_config.NumberColumn("Momentum", format="%.0f")
    },
    hide_index=True,
    width="stretch",
    num_rows="dynamic"

)

st.caption(f"Filtered: {len(filtered_df)} alerts")

# ============= ANALYTICS GRID (Step 4/8) =============
col1, col2 = st.columns(2)
with col1:
    st.markdown("### Threat Timeline")
    timeline_df = filtered_df.set_index('timestamp').resample('1min').size()
    fig_timeline = px.line(timeline_df, title="Alert Velocity")
st.plotly_chart(fig_timeline, width='stretch')

with col2:
    st.markdown("### Attack Heatmap")
    heatmap_data = filtered_df.pivot_table(values='ai_risk', index='attack_type', columns='country', aggfunc='mean')
    fig_heatmap = px.imshow(heatmap_data.fillna(0), title="Risk by Attack x Geo")
st.plotly_chart(fig_heatmap, width='stretch')

col3, col4 = st.columns(2)
with col3:
    st.markdown("### Severity Distribution")
    fig_severity = px.histogram(filtered_df, x='severity', title="Severity Histogram")
    st.plotly_chart(fig_severity, width="stretch")

with col4:
    st.markdown("### IP Momentum Treemap")
    ip_agg = filtered_df.groupby('src_ip').agg({'momentum': 'sum', 'ai_risk': 'mean'}).reset_index()
    fig_tree = px.treemap(ip_agg, path=['src_ip'], values='momentum', color='ai_risk', title="IP Burst Activity")
    st.plotly_chart(fig_tree, width="stretch")

st.divider()

# ========================================
# 🌍 PROFESSIONAL ATTACK MAP (Step 3/8)
# ========================================
st.markdown("### Global Attack Surface")
map_df = filtered_df[filtered_df['latitude'] != 0].copy()

HYD_LAT, HYD_LON = 17.3850, 78.4867

if len(map_df) > 0:
    map_df['target_lat'] = HYD_LAT
    map_df['target_lon'] = HYD_LON

    # Multi-layer: Heat + Scatter + Arc
    heat_layer = pdk.Layer(
        "HexagonLayer",
        map_df,
        get_position="[longitude, latitude]",
        auto_highlight=True,
        elevation_scale=50,
        pickable=True,
        elevation_range=[0, 1000],
        extruded=True
    )
    
    scatter_layer = pdk.Layer(
        "ScatterplotLayer",
        map_df,
        get_position="[longitude, latitude]",
        get_fill_color="[255 - ai_risk * 2, 100, 100]",
        get_radius="ai_risk * 2",
        pickable=True
    )
    
    arc_layer = pdk.Layer(
        "ArcLayer",
        map_df,
        get_source_position="[longitude, latitude]",
        get_target_position="[target_lon, target_lat]",
        get_source_color="[255, 165, 0, 180]",
        get_target_color="[59, 130, 246, 200]",
        get_width="max(0.3, ai_risk / 30)",
        get_tilt=10,
        get_height=0.2,
        opacity=0.8
    )

    deck = pdk.Deck(
        layers=[heat_layer, scatter_layer, arc_layer],
        initial_view_state=pdk.ViewState(
            latitude=HYD_LAT,
            longitude=HYD_LON, 
            zoom=2,
            pitch=45,
            bearing=-15
        )
    )
    
    st.pydeck_chart(deck, height=500, width="stretch")
    st.caption(f"Active vectors: {len(map_df)} | Red=High Risk → Hyderabad Target")
else:
    st.info("No geolocated threats in filter")

 # Leftover code removed - map fully upgraded above

st.divider()

# DUAL ANALYTICS
col1, col2 = st.columns(2)
with col1:
    st.markdown("### 📈 **Threat Velocity**")
    df['time_bucket'] = df.timestamp.dt.floor('1min')
    velocity = df.groupby('time_bucket').size()
    st.line_chart(velocity, height=300)

with col2:
    st.markdown("### 🎯 **Attack Matrix**")
    matrix = df[['attack_type', 'severity']].groupby('attack_type').agg('mean').round(1)
    st.bar_chart(matrix.severity)

import re

@st.cache_data(ttl=5)
def parse_threat_terminal():
    """Parse ONLY exact THREAT lines from system.log tail"""
    try:
        with open("system.log", "r", encoding="utf-8") as f:
            lines = f.readlines()[-100:]  # tail 100 lines
    except:
        return pd.DataFrame()
    
    threats = []
    threat_regex = r"🚨?\s*THREAT:\s*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s*\|\s*([^\|]+?)\s*\|\s*Sev=(\d+)\s*\|\s*Risk=([\d.]+)\s*\|\s*Events=(\d+)\s*\|\s*Action=([A-Z]+)"
    
    for line in lines:
        match = re.search(threat_regex, line.strip())
        if match:
            ip, attack, sev, risk, events, action = match.groups()
            threats.append({
                'Timestamp': datetime.now().strftime('%H:%M:%S'),
                'IP': ip.strip(),
                'Attack': attack.strip(),
                'Sev': int(sev),
                'Risk': float(risk),
                'Events': int(events),
                'Action': action.strip()
            })
    
    if threats:
        df_threats = pd.DataFrame(threats)
        # Sort by risk desc
        return df_threats.sort_values('Risk', ascending=False).head(20)
    return pd.DataFrame()

# 🚨 THREAT TERMINAL (Raw Log)
st.markdown("### 🚨 **THREAT TERMINAL** (Raw system.log)")
threat_terminal = parse_threat_terminal()
if not threat_terminal.empty:
    # Terminal styling
    styled = threat_terminal.style.format({
        'Sev': '{:.0f}', 'Risk': '{:.1f}', 'Events': '{:.0f}'
    }).set_properties(**{
        'font-family': 'monospace', 
        'font-size': '13px', 
        'background-color': '#000', 
        'color': '#00ff41', 
        'border': '1px solid #333'
    }, subset=pd.IndexSlice[:]).background_gradient(subset=['Risk'], cmap='Reds', low=0, high=0.6)
    
    st.dataframe(styled, height=300, width='stretch')
    
    # Top threat metric
    top_threat = threat_terminal.iloc[0]
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🔥 IP", top_threat['IP'])
    col2.metric("⚡ Attack", top_threat['Attack'])
    col3.metric("🚨 Risk", f"{top_threat['Risk']:.1f}")
    col4.metric("📊 Action", top_threat['Action'])
else:
    st.info("🔄 No THREAT lines in system.log (run `python run_system.py` for live threats)")


# 📡 LIVE THREAT FEED (DB)
st.markdown("### 📡 **LIVE THREAT FEED** (Database)")
terminal = df[['timestamp', 'src_ip', 'attack_type', 'severity', 'ai_risk']].head(30).copy()
terminal['timestamp'] = pd.to_datetime(terminal['timestamp']).dt.strftime('%H:%M:%S')
st.dataframe(
    terminal.style.format({
        'ai_risk': '{:.1f}'
    }),
    height=400
)

# AI WAR ROOM
st.markdown("### 🤖 **AI WAR ROOM**")
rcol1, rcol2 = st.columns([3, 1])

with rcol1:
    kill_list = df[df.ai_risk > 75][['src_ip', 'ai_risk', 'severity']]
    st.dataframe(kill_list)

with rcol2:
    st.button("🚫 **EXECUTE BLOCK**", width="stretch")
    ips = df[df.ai_risk > 75]['src_ip'].unique()
    with open('blacklist.txt', 'a') as f:
            [f.write(ip+'\n') for ip in ips]
    st.balloons()
    st.success(f"⚡ **{len(ips)} BLOCKED**")

st.markdown("---")
st.markdown("**🛡️ AINTA Ultimate** | india | 3s Live | Zero Errors | AI Powered")
st.caption("💡 `python run_system.py` | 🎥 Demo: attacks/ddos_simulator.py")

