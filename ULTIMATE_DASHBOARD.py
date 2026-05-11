import streamlit as st
import pandas as pd
import sqlite3
import pydeck as pdk
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ======================================================
# 🚀 MAX UPGRADE CONFIG
# ======================================================
st.set_page_config(
    page_title="AINTA SOC Ultimate", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

st_autorefresh(interval=5000, key="data_refresh")  # 5s live updates
st.title("🛡️ AINTA SOC - Ultimate Edition")
st.markdown("### Real-time AI Threat Intelligence | Hyderabad SOC")

# Sidebar controls
st.sidebar.header("⚙️ Controls")
auto_play = st.sidebar.checkbox("Auto-generate demo attacks", value=True)
risk_threshold = st.sidebar.slider("Risk Alert", 0, 200, 90)
time_range = st.sidebar.selectbox("Time view", ["Last 5min", "Last 1h", "All"], index=0)

# ======================================================
# 🔄 LIVE DATA ENGINE
# ======================================================
@st.cache_data(ttl=5)  # 5s cache
def load_data():
    conn = sqlite3.connect("database/alerts.db", timeout=10)
    query = "SELECT * FROM alerts ORDER BY timestamp DESC LIMIT 5000"
    df = pd.read_sql(query, conn)
    conn.close()
    
    if df.empty:
        return pd.DataFrame()
    
    # Ultimate cleaning - ensure columns exist
    df = df.reindex(columns=df.columns.tolist() + ['severity', 'packet_rate', 'timestamp'], fill_value=0)
    
    # Ultimate cleaning
    df = df.assign(
        severity=pd.to_numeric(df.severity, errors='coerce').fillna(0),
        packet_rate=pd.to_numeric(df.packet_rate, errors='coerce').fillna(0),
        timestamp=pd.to_datetime(df.timestamp, errors='coerce')
    ).dropna(subset=['timestamp']).reset_index(drop=True)
    
    # Add columns safely
    for col in ['attack_type', 'country']:
        df[col] = df.get(col, 'unknown')
    
    # Geo safe
    if 'latitude' in df.columns:
        df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce').fillna(0)
    else:
        df['latitude'] = 0

    if 'longitude' in df.columns:
        df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce').fillna(0)
    else:
        df['longitude'] = 0
    
    return df

data = load_data()

if data.empty:
    st.error("🚫 No data. Run `python run_system.py` to start monitoring!")
    if st.button("🧪 Quick Demo"):
        import subprocess
        subprocess.Popen(["python", "attacks/ddos_simulator.py"])
    st.stop()

# ======================================================
# 🎯 EXECUTIVE SUMMARY
# ======================================================
kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5 = st.columns(5)
kpi_col1.metric("🔥 Active Threats", len(data), delta="5min")
kpi_col2.metric("⚡ Peak Rate", f"{data['packet_rate'].max():.0f} pps")
kpi_col3.metric("🎯 Critical", len(data[data.severity > 7]))
kpi_col4.metric("🌍 Sources", data['src_ip'].nunique())
kpi_col5.metric("⏱️ Last Alert", data['timestamp'].max().strftime("%H:%M:%S"))

st.divider()

# ======================================================
# 🚨 TOP 5 THREATS (AI PRIORITIZED)
# ======================================================
st.subheader("🚨 Top Threats - AI Risk Score")

# Advanced risk scoring
def calculate_risk(row):
    score = row['severity'] * 2
    score += row['packet_rate'] * 0.02
    score += row['duration'] * 0.001 if 'duration' in row else 0
    return score

data['risk_score'] = data.apply(calculate_risk, axis=1)
top_threats = data.nlargest(5, 'risk_score')[['src_ip', 'attack_type', 'severity', 'packet_rate', 'risk_score', 'country']]

st.dataframe(top_threats.style.format({'risk_score': '{:.1f}', 'packet_rate': '{:.0f}'}))

if auto_play and st.button("💥 Generate Live Attack Demo"):
    import subprocess
    subprocess.Popen(["python", "attacks/ddos_simulator.py"])

# ======================================================
# 🌍 INTERACTIVE WORLD MAP
# ======================================================
st.subheader("🌍 Global Attack Map - Live")

data_map = data.query('latitude != 0 and longitude != 0').tail(100)

if not data_map.empty:
    # Hyderabad target
    target_lat, target_lon = 17.3850, 78.4867
    data_map = data_map.assign(target_lat=target_lat, target_lon=target_lon)
    
    # Risk-colored arcs
    arc_layer = pdk.Layer(
        'ArcLayer',
        data_map,
        get_source_position='[longitude, latitude]',
        get_target_position='[target_lon, target_lat]',
        get_width="severity * 2",
        get_source_color=[255 * (1 - data_map.severity/10), 0, 0],
        get_target_color=[0, 255 * (data_map.severity/10), 255],
        get_tilt=20,
    )
    
    map_view = pdk.ViewState(
        latitude=target_lat, 
        longitude=target_lon, 
        zoom=2.5,
        bearing=0,
        pitch=30
    )
    
    st.pydeck_chart(pdk.Deck(
        layers=[arc_layer],
        initial_view_state=map_view,
        height=500
    ))
    
    st.caption(f"🎯 Target: Hyderabad | 🛡️ {len(data_map)} active vectors")
else:
    col1, col2 = st.columns(2)
    col1.info("🗺️ Waiting for geo data...")
    col2.info("💡 Run demo attacks for live visualization")

st.divider()

# ======================================================
# 📊 ADVANCED ANALYTICS DASHBOARD
# ======================================================
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Attack Rate Timeline")
    
    # Bulletproof timeline (no resample crash)
    if 'timestamp' in data.columns:
        data['minute_bucket'] = data['timestamp'].dt.floor('1min')
        timeline_data = data.groupby('minute_bucket').size().reset_index()
        timeline_data = timeline_data.rename(columns={'minute_bucket': 'timestamp', 0: 'count'})
        
        fig = px.line(timeline_data, x='timestamp', y='count', 
                     title='Live Attack Rate')
        fig.update_traces(line=dict(color='#ff4444', width=3))
        fig.update_layout(showlegend=False, height=300)
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("⚡ Severity Distribution")
    
    severity_counts = data['severity'].value_counts().sort_index()
    fig = go.Figure(data=[
        go.Bar(x=severity_counts.index, y=severity_counts.values,
               marker_color=px.colors.sequential.Reds)
    ])
    fig.update_layout(height=300, showlegend=False, 
                     xaxis_title="Severity", yaxis_title="Count")
    st.plotly_chart(fig, use_container_width=True)

# Attack type pie
st.subheader("🎭 Attack Types")
attack_pie = data['attack_type'].value_counts()
fig = px.pie(values=attack_pie.values, names=attack_pie.index, 
             color_discrete_sequence=px.colors.qualitative.Set3)
st.plotly_chart(fig, use_container_width=True)

# ======================================================
# 🎯 AUTONOMOUS RESPONSE CENTER
# ======================================================
st.subheader("🤖 Autonomous Response")

response_col1, response_col2 = st.columns([3,1])

with response_col1:
    high_risk = data[data['risk_score'] > risk_threshold].tail(10)
    if not high_risk.empty:
        st.dataframe(high_risk[['src_ip', 'risk_score', 'severity', 'packet_rate']].style
                    .format({'risk_score': '{:.1f}'}))

with response_col2:
    if st.button("🚫 BLOCK ALL HIGH RISK", type="primary"):
        blocked = high_risk['src_ip'].tolist()
        with open("blacklist.txt", "a") as f:
            for ip in blocked:
                f.write(f"{ip}\n")
        st.success(f"✅ Blocked {len(blocked)} IPs")

# ======================================================
# 📡 LIVE FEED TERMINAL
# ======================================================
st.subheader("📡 Live Packet Feed")
live_feed = data[['timestamp', 'src_ip', 'attack_type', 'severity', 'packet_rate']].tail(20)

st.dataframe(live_feed.style.format({
    'timestamp': '{:%H:%M:%S}',
    'packet_rate': '{:.0f}',
    'severity': '{:.0f}'
}), height=300)

# Status footer
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)
col1.metric("🕐 Last Update", datetime.now().strftime("%H:%M:%S"))
col2.metric("💾 Alerts Stored", f"{len(data):,}")
col3.metric("🚀 Version", "Ultimate v2.0")
col4.metric("📍 SOC", "Hyderabad")

st.caption("""
🛡️ **AINTA Ultimate** - Maximum security upgrades  
🔄 Live 5s refresh | 🤖 AI response | 🌍 Interactive maps | 📊 Analytics  
💡 **Controls**: Sidebar | **Demo**: Auto-generate button  
📄 **Logs**: system.log | **Blacklist**: blacklist.txt
""")

