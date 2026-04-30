import streamlit as st
import pandas as pd
import sqlite3
import pydeck as pdk
import numpy as np
from streamlit_autorefresh import st_autorefresh

# ---------------- CONFIG ----------------
st.set_page_config(page_title="AINTA SOC", layout="wide")
st_autorefresh(interval=4000, key="refresh")

st.title("🛡️ AINTA – AI Enhanced Network Threat Analyzer")

# ---------------- LOAD ----------------
conn = sqlite3.connect("database/alerts.db", check_same_thread=False)

try:
    data = pd.read_sql("SELECT * FROM alerts ORDER BY timestamp DESC LIMIT 2000", conn)
except Exception as e:
    st.error(f"DB Error: {e}")
    st.stop()

if data.empty:
    st.error("🚫 No data from monitoring engine")
    st.stop()

# ---------------- CLEAN ----------------
required_cols = ["src_ip", "severity", "packet_rate", "timestamp"]

for col in required_cols:
    if col not in data.columns:
        data[col] = 0

data["severity"] = pd.to_numeric(data["severity"], errors="coerce").fillna(0)
data["packet_rate"] = pd.to_numeric(data["packet_rate"], errors="coerce").fillna(0)
data["timestamp"] = pd.to_datetime(data["timestamp"], errors="coerce")

data = data.dropna(subset=["timestamp"])

for col in ["attack_type", "country", "latitude", "longitude"]:
    if col not in data.columns:
        data[col] = "unknown" if col in ["attack_type", "country"] else 0

# ======================================================
# 🧠 ENGINE
# ======================================================

# Dedup
data["bucket"] = data["timestamp"].dt.floor("10s")
data = data.drop_duplicates(subset=["src_ip", "bucket"])

# Incident aggregation
incidents = (
    data.groupby("src_ip")
    .agg(
        events=("src_ip", "count"),
        max_severity=("severity", "max"),
        avg_rate=("packet_rate", "mean"),
        first_seen=("timestamp", "min"),
        last_seen=("timestamp", "max")
    )
)

# Duration
incidents["duration"] = (incidents["last_seen"] - incidents["first_seen"]).dt.total_seconds()

# Momentum
recent = data[data["timestamp"] > (data["timestamp"].max() - pd.Timedelta(minutes=2))]
momentum = recent.groupby("src_ip").size()
incidents["momentum"] = incidents.index.map(momentum).fillna(0)

# Threat History (NEW)
history = (
    data.groupby("src_ip")
    .agg(
        total_events=("src_ip","count"),
        avg_severity=("severity","mean")
    )
)
incidents = incidents.join(history)

# Threat Intel (SIMULATED)
def enrich(ip):
    if str(ip).startswith("172."):
        return ("internal", 10)
    elif str(ip).startswith("35.") or str(ip).startswith("104."):
        return ("cloud", 60)
    return ("unknown", 30)

intel = pd.DataFrame([
    {"src_ip": ip, "reputation": enrich(ip)[0], "intel_score": enrich(ip)[1]}
    for ip in incidents.index
]).set_index("src_ip")

incidents = incidents.join(intel)

# Risk
incidents["risk"] = (
    incidents["max_severity"] * 0.4 +
    incidents["events"] * 4 +
    incidents["avg_rate"] * 0.01 +
    incidents["duration"] * 0.01 +
    incidents["momentum"] * 5 +
    incidents["intel_score"]
)

# Behavior
incidents["behavior"] = np.where(
    incidents["events"] > 10, "Persistent",
    np.where(incidents["momentum"] > 3, "Burst", "Low")
)

# Decision
def decide(row):
    if row["risk"] > 150:
        return "BLOCK"
    if row["risk"] > 90:
        return "MONITOR"
    return "IGNORE"

incidents["action"] = incidents.apply(decide, axis=1)

# Priority
def classify(r):
    if r > 150:
        return "CRITICAL"
    if r > 100:
        return "HIGH"
    if r > 60:
        return "MEDIUM"
    return "LOW"

incidents["priority"] = incidents["risk"].apply(classify)

# Alert fatigue
incidents["fatigue"] = np.where(
    incidents["events"] > 20, "Overloaded",
    np.where(incidents["events"] > 10, "Repeated", "Normal")
)

# ======================================================
# 🎯 QUEUE
# ======================================================
queue = incidents.sort_values(by="risk", ascending=False).head(10)

# ======================================================
# 🚨 TOP ALERT
# ======================================================
if not queue.empty:
    top = queue.iloc[0]

    st.error(
        f"🚨 {top.name} | Risk={round(top['risk'],1)} | "
        f"Momentum={top['momentum']} | Action={top['action']}"
    )

# ======================================================
# 📊 KPI
# ======================================================
c1,c2,c3,c4 = st.columns(4)

c1.metric("Incidents", len(incidents))
c2.metric("Critical", (incidents["priority"]=="CRITICAL").sum())
c3.metric("Auto Block", (incidents["action"]=="BLOCK").sum())
c4.metric("Attackers", len(incidents))

st.divider()

# ======================================================
# 🎯 AI QUEUE
# ======================================================
st.subheader("🎯 AI Decision Queue")
st.dataframe(queue)

# ======================================================
# 🌍 FLOW MAP (ADVANCED)
# ======================================================
st.subheader("🌍 Attack Flow Map")

geo = data.dropna(subset=["latitude","longitude"])
geo = geo[(geo["latitude"]!=0)&(geo["longitude"]!=0)]

if not geo.empty:
    # Auto location from IP API
    import requests
    try:
        resp = requests.get('http://ip-api.com/json/?fields=lat,lon,status')
        loc = resp.json()
        if loc['status'] == 'success':
            target_lat = loc['lat']
            target_lon = loc['lon']
        else:
            target_lat = 19.0760
            target_lon = 72.8777
    except Exception:
        print("Location API unavailable")
        target_lat = 19.0760
        target_lon = 72.8777
    geo["target_lat"] = target_lat
    geo["target_lon"] = target_lon

    arc = pdk.Layer(
        "ArcLayer",
        geo,
        get_source_position='[longitude, latitude]',
        get_target_position='[target_lon, target_lat]',
        get_width=2,
        get_source_color=[255, 0, 0],
        get_target_color=[0, 255, 255],
    )

    st.pydeck_chart(pdk.Deck(
        layers=[arc],
        initial_view_state=pdk.ViewState(latitude=20, longitude=0, zoom=1)
    ))

# ======================================================
# 📈 MOMENTUM
# ======================================================
st.subheader("📈 Attack Momentum")

timeline = (
    data.set_index("timestamp")
    .resample("1min")
    .size()
)

st.line_chart(timeline)

# ======================================================
# 🔥 BEHAVIOR
# ======================================================
st.subheader("🔥 Behavior Profiling")

st.dataframe(
    incidents[["events","momentum","behavior","risk","action","fatigue"]]
    .sort_values(by="risk", ascending=False)
.head(10)
)

# ======================================================
# 🧩 STORYLINE (ELITE FEATURE)
# ======================================================
st.subheader("🧩 Attack Storyline")

for ip in queue.index[:3]:
    st.write(f"### {ip}")

    ip_data = data[data["src_ip"] == ip].sort_values("timestamp")

    st.dataframe(
        ip_data[["timestamp","attack_type","packet_rate","severity"]].head(10)
    )

# ======================================================
# 🚨 RESPONSE
# ======================================================
st.subheader("🚨 Autonomous Response")

auto_block = queue[queue["action"]=="BLOCK"]

for ip, row in auto_block.iterrows():

    col1, col2 = st.columns([4,1])

    col1.write(f"🚫 {ip} | Risk={round(row['risk'],1)}")

    if col2.button("CONFIRM BLOCK", key=f"block_{ip}"):
        with open("blacklist.txt","a") as f:
            f.write(str (ip) +"\n")
        st.success(f"{ip} blocked")

# ======================================================
# 📡 RAW DATA
# ======================================================
st.subheader("📡 Raw Feed")

st.dataframe(
        data.sort_values(by="timestamp", ascending=False).head(100)
    )
