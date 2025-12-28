import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

import alerts
from anomaly_detector import detect_anomalies

# Initialize session state for real-time monitoring
if 'traffic_data' not in st.session_state:
    st.session_state.traffic_data = pd.DataFrame()
if 'last_alert_ids' not in st.session_state:
    st.session_state.last_alert_ids = set()
if 'monitoring_active' not in st.session_state:
    st.session_state.monitoring_active = False

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Smart Home Intrusion Detector",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 Smart Home Network Intrusion Detection System")
st.write("AI-based detection of anomalous smart home network traffic.")

st.divider()

# ---------------- Email Settings UI ----------------
with st.sidebar.expander("Email Settings (optional)", expanded=False):
    st.caption("Configure SMTP to receive email alerts for MEDIUM/HIGH risks.")
    with st.form(key="smtp_form"):
        smtp_host = st.text_input("SMTP Host", value=st.session_state.get('smtp_config', {}).get('SMTP_HOST') if 'smtp_config' in st.session_state else "")
        smtp_port = st.text_input("SMTP Port", value=st.session_state.get('smtp_config', {}).get('SMTP_PORT') if 'smtp_config' in st.session_state else "587")
        smtp_user = st.text_input("SMTP User", value=st.session_state.get('smtp_config', {}).get('SMTP_USER') if 'smtp_config' in st.session_state else "")
        smtp_password = st.text_input("SMTP Password", type="password", value=st.session_state.get('smtp_config', {}).get('SMTP_PASSWORD') if 'smtp_config' in st.session_state else "")
        alert_to = st.text_input("Alert To (comma-separated)", value=st.session_state.get('smtp_config', {}).get('ALERT_TO') if 'smtp_config' in st.session_state else "")
        col1, col2 = st.columns([1,1])
        with col1:
            save = st.form_submit_button("Save")
        with col2:
            clear = st.form_submit_button("Clear")

    if save:
        st.session_state['smtp_config'] = {
            'SMTP_HOST': smtp_host,
            'SMTP_PORT': smtp_port,
            'SMTP_USER': smtp_user,
            'SMTP_PASSWORD': smtp_password,
            'ALERT_TO': alert_to
        }
        st.sidebar.success("SMTP settings saved to session.")
    if clear:
        if 'smtp_config' in st.session_state:
            del st.session_state['smtp_config']
        st.sidebar.info("SMTP settings cleared from session.")

if 'smtp_config' in st.session_state:
    cfg = st.session_state['smtp_config']
    st.sidebar.markdown(f"**SMTP:** {cfg.get('SMTP_HOST','')} — **To:** {cfg.get('ALERT_TO','')}")

# Button to test SMTP connection
if st.sidebar.button('Test SMTP connection'):
    ok, msg = alerts.test_smtp_connection()
    if ok:
        st.sidebar.success(msg)
    else:
        st.sidebar.error(msg)

# ---------------- Data Simulation ----------------
st.subheader("📡 Simulated Network Traffic")

def generate_data():
    np.random.seed(42)
    devices = ["Camera", "Smart Lock", "Thermostat", "Light", "Speaker"]

    n = 120
    packets = np.random.normal(300, 60, n).astype(int)
    devices_col = np.random.choice(devices, n)

    # Timestamps: one per minute ending now
    timestamps = pd.date_range(end=pd.Timestamp.now(), periods=n, freq='T')

    # Inject anomalies
    for i in np.random.choice(range(n), 10, replace=False):
        packets[i] = np.random.randint(800, 1200)

    return pd.DataFrame({
        "Device": devices_col,
        "Packets": packets,
        "Timestamp": timestamps
    })


def add_incoming_traffic(num_packets=10):
    """Simulate new incoming traffic and detect anomalies in real-time."""
    devices = ["Camera", "Smart Lock", "Thermostat", "Light", "Speaker"]
    
    # Generate new traffic
    new_packets = np.random.normal(300, 60, num_packets).astype(int)
    new_devices = np.random.choice(devices, num_packets)
    new_timestamps = pd.date_range(start=st.session_state.traffic_data['Timestamp'].max() + timedelta(minutes=1), periods=num_packets, freq='T')
    
    # Randomly inject attack traffic
    attack_indices = np.random.choice(range(num_packets), max(1, num_packets // 5), replace=False)
    for i in attack_indices:
        new_packets[i] = np.random.randint(800, 1500)
    
    new_data = pd.DataFrame({
        "Device": new_devices,
        "Packets": new_packets,
        "Timestamp": new_timestamps
    })
    
    # Append to existing traffic
    st.session_state.traffic_data = pd.concat([st.session_state.traffic_data, new_data], ignore_index=True)
    
    # Detect anomalies on full dataset
    results = detect_anomalies(st.session_state.traffic_data)
    
    # Send alerts for newly detected HIGH/MEDIUM anomalies
    for idx, row in results.iterrows():
        if row["Risk"] != "LOW":
            # Create a unique ID for this alert to avoid duplicates
            alert_id = hash((row["Device"], row["Timestamp"], row["Risk"]))
            
            if alert_id not in st.session_state.last_alert_ids:
                alerts.send_alert(
                    device=row["Device"],
                    packets=row["Packets"],
                    risk=row["Risk"],
                    risk_score=row.get('RiskScore', None),
                    explanation=row.get('Explanation', ''),
                    shap_explanation=row.get('SHAP_Explanation', '')
                )
                st.session_state.last_alert_ids.add(alert_id)
    
    return results

df = generate_data()
# Simulation controls
simulate_attack = st.sidebar.checkbox("Enable attack simulation", value=False)
if simulate_attack:
    # Inject a stronger burst of anomalies to simulate attack
    for i in np.random.choice(range(len(df)), 15, replace=False):
        df.loc[i, 'Packets'] = df.loc[i, 'Packets'] + np.random.randint(500, 1500)
    st.warning("Attack simulation enabled — anomalous traffic injected.")

st.dataframe(df, use_container_width=True)

st.divider()

# Real-time monitoring interface
st.subheader("📡 Real-Time Network Traffic Monitoring")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🔄 Initialize System"):
        st.session_state.traffic_data = generate_data()
        st.session_state.last_alert_ids = set()
        st.success("System initialized with baseline traffic data.")
with col2:
    if st.button("📥 Simulate Incoming Traffic"):
        if len(st.session_state.traffic_data) == 0:
            st.session_state.traffic_data = generate_data()
        results = add_incoming_traffic(num_packets=15)
        st.success("✅ New traffic packet processed. Alerts sent for anomalies.")
with col3:
    if st.button("🚨 Simulate Attack"):
        if len(st.session_state.traffic_data) == 0:
            st.session_state.traffic_data = generate_data()
        # Inject strong attack traffic
        devices = ["Camera", "Smart Lock", "Thermostat", "Light", "Speaker"]
        attack_packets = np.random.randint(1200, 2000, 20)
        attack_devices = np.random.choice(devices, 20)
        attack_timestamps = pd.date_range(start=st.session_state.traffic_data['Timestamp'].max() + timedelta(minutes=1), periods=20, freq='T')
        
        attack_data = pd.DataFrame({
            "Device": attack_devices,
            "Packets": attack_packets,
            "Timestamp": attack_timestamps
        })
        st.session_state.traffic_data = pd.concat([st.session_state.traffic_data, attack_data], ignore_index=True)
        
        # Detect and alert
        results = detect_anomalies(st.session_state.traffic_data)
        for idx, row in results.iterrows():
            if row["Risk"] != "LOW":
                alert_id = hash((row["Device"], row["Timestamp"], row["Risk"]))
                if alert_id not in st.session_state.last_alert_ids:
                    alerts.send_alert(
                        device=row["Device"],
                        packets=row["Packets"],
                        risk=row["Risk"],
                        risk_score=row.get('RiskScore', None),
                        explanation=row.get('Explanation', ''),
                        shap_explanation=row.get('SHAP_Explanation', '')
                    )
                    st.session_state.last_alert_ids.add(alert_id)
        st.warning("🚨 Attack simulated — HIGH packet traffic injected and alerts triggered!")

# Display current traffic data
if len(st.session_state.traffic_data) > 0:
    st.write(f"**Total packets monitored:** {len(st.session_state.traffic_data)}")
    st.dataframe(st.session_state.traffic_data.tail(20), use_container_width=True)
else:
    st.info("Click 'Initialize System' to start monitoring.")

st.divider()

# ---------------- Detection (Demo Mode) ----------------
st.subheader("🧠 Anomaly Detection (Demo with Initial Data)")

results = detect_anomalies(df)
# Display results with SHAP explanations (if available)
display_cols = ['Device','Packets','Timestamp','Risk','RiskScore','Explanation','CyberContext']
if 'SHAP_Explanation' in results.columns:
    display_cols.append('SHAP_Explanation')
st.dataframe(results[display_cols].fillna(''), use_container_width=True)

# Simple risk distribution
st.bar_chart(results['Risk'].value_counts())

st.divider()

# ---------------- Alerts ----------------
st.subheader("🚨 Alerts")

# Alerts from demo data (initial load only)
for _, row in results.iterrows():
    if row["Risk"] != "LOW":
        alert_id = hash((row["Device"], row["Timestamp"], row["Risk"]))
        if alert_id not in st.session_state.last_alert_ids:
            alerts.send_alert(
                device=row["Device"],
                packets=row["Packets"],
                risk=row["Risk"],
                risk_score=row.get('RiskScore', None),
                explanation=row.get('Explanation', ''),
                shap_explanation=row.get('SHAP_Explanation', '')
            )
            st.session_state.last_alert_ids.add(alert_id)

st.divider()

# Alert Dashboard (real-time, updated as you interact)
alerts.show_alert_dashboard()

st.divider()

st.success("✅ Smart Home Intrusion Detector — Real-Time Monitoring Active")
