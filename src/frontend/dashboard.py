"""
Streamlit Dashboard for Credit Card Fraud Detection
Real-time interactive fraud analysis and visualization (Modern UI)
"""

import streamlit as st
import requests
import json
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import time

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Fraud Detection Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM STYLING (MODERN DARK THEME)
# ============================================================================

st.markdown("""
    <style>
    /* Global background and text */
    .stApp {
        background-color: #0B0F19;
        color: #E2E8F0;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #1F2937;
    }
    
    /* Title Gradient Styling */
    h1 {
        background: linear-gradient(45deg, #38BDF8, #818CF8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        letter-spacing: -0.5px;
        margin-bottom: 0.5rem;
    }
    h2, h3 {
        color: #F8FAFC !important;
        font-weight: 600 !important;
    }

    /* Custom Buttons */
    div.stButton > button {
        background: linear-gradient(135deg, #4F46E5 0%, #3B82F6 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.4), 0 4px 6px -2px rgba(59, 130, 246, 0.2);
        color: white;
        border: none;
    }

    /* Native Metric Card Styling */
    div[data-testid="metric-container"] {
        background-color: #1E293B;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #334155;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }
    div[data-testid="metric-container"] > div {
        color: #94A3B8; /* Label color */
    }
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: #F1F5F9; /* Value color */
        font-weight: 700;
    }

    /* Custom Status Pills */
    .status-pill {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 0.9rem;
        letter-spacing: 0.5px;
    }
    .status-healthy {
        background-color: rgba(16, 185, 129, 0.15);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    .status-offline {
        background-color: rgba(239, 68, 68, 0.15);
        color: #F87171;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #1E293B;
        border-radius: 8px;
    }
    
    /* DataFrame styling */
    [data-testid="stDataFrame"] {
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid #334155;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# CONFIGURATION
# ============================================================================

API_BASE_URL = "http://localhost:8000"
API_PREDICT_ENDPOINT = f"{API_BASE_URL}/predict"
API_HEALTH_ENDPOINT = f"{API_BASE_URL}/health"

# Feature names (30 total)
FEATURE_NAMES = ["Time", "Amount"] + [f"V{i}" for i in range(1, 29)]

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if "transaction_data" not in st.session_state:
    st.session_state.transaction_data = None

if "prediction_result" not in st.session_state:
    st.session_state.prediction_result = None

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def generate_random_transaction():
    """Generate a random legitimate-like transaction"""
    transaction = {
        "Time": np.random.uniform(0, 86400),  # 0-24 hours in seconds
        "Amount": np.random.uniform(0.99, 1000),  # $0.99 - $1000
    }
    
    # Add V1-V28 with realistic distributions (mean=0, std=1)
    for i in range(1, 29):
        transaction[f"V{i}"] = np.random.normal(0, 1)
    
    return transaction

def check_api_status():
    """Check if FastAPI backend is running"""
    try:
        response = requests.get(API_HEALTH_ENDPOINT, timeout=2)
        if response.status_code == 200:
            data = response.json()
            return {
                "status": "healthy",
                "model_loaded": data.get("model_loaded", False),
                "threshold": data.get("threshold", 0.8)
            }
    except requests.exceptions.ConnectionError:
        return {"status": "offline", "model_loaded": False, "threshold": None}
    except Exception as e:
        return {"status": "error", "model_loaded": False, "error": str(e)}

def call_fraud_detection_api(transaction_data):
    """Send transaction to fraud detection API"""
    try:
        response = requests.post(
            API_PREDICT_ENDPOINT,
            json=transaction_data,
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"error": "Cannot connect to API. Is the backend running?"}
    except requests.exceptions.Timeout:
        return {"error": "API request timed out"}
    except Exception as e:
        return {"error": f"API Error: {str(e)}"}

def create_gauge_chart(anomaly_score, threshold):
    """Create a high-tech Plotly gauge chart"""
    fig = go.Figure(data=[go.Indicator(
        mode="gauge+number+delta",
        value=anomaly_score,
        domain={"x": [0, 1], "y": [0, 1]},
        title={"text": "Anomaly Score", "font": {"size": 20, "color": "#E2E8F0"}},
        delta={
            "reference": threshold,
            "suffix": " vs Limit",
            "increasing": {"color": "#EF4444"},
            "decreasing": {"color": "#10B981"}
        },
        gauge={
            "axis": {"range": [0, max(2.0, anomaly_score + 0.5)], "tickwidth": 1, "tickcolor": "#475569"},
            "bar": {"color": "rgba(0,0,0,0)"}, # Hide default bar, use steps
            "bgcolor": "#1E293B",
            "borderwidth": 0,
            "steps": [
                {"range": [0, threshold], "color": "rgba(16, 185, 129, 0.4)"}, # Safe Zone (Green)
                {"range": [threshold, threshold + 0.5], "color": "rgba(245, 158, 11, 0.5)"}, # Warning Zone (Yellow)
                {"range": [threshold + 0.5, 5], "color": "rgba(239, 68, 68, 0.5)"} # Danger Zone (Red)
            ],
            "threshold": {
                "line": {"color": "#EF4444", "width": 4},
                "thickness": 0.75,
                "value": threshold
            }
        },
        number={"font": {"size": 36, "color": "#F8FAFC"}}
    )])
    
    # Add actual value marker pointer
    fig.add_annotation(
        x=0.5, y=0.3,
        text=f"Value: {anomaly_score:.4f}",
        showarrow=False,
        font=dict(size=14, color="#94A3B8")
    )
    
    fig.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        font={"family": "sans-serif"}
    )
    return fig

def create_feature_distribution_chart(transaction_data):
    """Create a modern bar chart showing feature values"""
    v_features = {k: v for k, v in transaction_data.items() if k.startswith("V")}
    selected_features = {k: v for i, (k, v) in enumerate(v_features.items()) if i % 2 == 0}
    
    colors = ["#38BDF8" if val >= 0 else "#818CF8" for val in selected_features.values()]
    
    fig = go.Figure(data=[
        go.Bar(
            x=list(selected_features.keys()),
            y=list(selected_features.values()),
            marker=dict(color=colors, line=dict(width=0)),
            text=[f"{v:.1f}" for v in selected_features.values()],
            textposition="auto",
            textfont=dict(color="#F8FAFC")
        )
    ])
    
    fig.update_layout(
        title=dict(text="Transaction Principal Components (Sampled)", font=dict(color="#E2E8F0")),
        xaxis=dict(title="Feature", gridcolor="#334155", tickfont=dict(color="#94A3B8")),
        yaxis=dict(title="Value", gridcolor="#334155", tickfont=dict(color="#94A3B8")),
        height=350,
        margin=dict(l=40, r=40, t=60, b=40),
        hovermode="x unified",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig

# ============================================================================
# HEADER & API STATUS
# ============================================================================

col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("<h1>Fraud Detection Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94A3B8; font-size: 1.1rem; margin-bottom: 2rem;'>Real-Time Credit Card Transaction Analysis & Neural Network Inference</p>", unsafe_allow_html=True)

with col2:
    api_status = check_api_status()
    st.markdown("<br>", unsafe_allow_html=True)
    if api_status["status"] == "healthy":
        st.markdown("<div align='right'><span class='status-pill status-healthy'>🟢 Backend Connected</span></div>", unsafe_allow_html=True)
    else:
        st.markdown("<div align='right'><span class='status-pill status-offline'>🔴 Backend Offline</span></div>", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR CONTROLS
# ============================================================================

st.sidebar.markdown("<h2 style='text-align: center;'>⚡ Controls</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<br>", unsafe_allow_html=True)

if st.sidebar.button("🎲 Generate Random Data", width='stretch'):
    st.session_state.transaction_data = generate_random_transaction()
    st.session_state.prediction_result = None

st.sidebar.markdown("<hr style='border-color: #334155;'>", unsafe_allow_html=True)

if st.session_state.transaction_data is None:
    st.session_state.transaction_data = generate_random_transaction()

st.sidebar.markdown("### 💰 Transaction Settings")
amount = st.sidebar.number_input(
    "Amount ($)",
    min_value=0.0,
    max_value=50000.0,
    value=float(st.session_state.transaction_data.get("Amount", 100.0)),
    step=50.0
)
st.session_state.transaction_data["Amount"] = amount

time_seconds = st.sidebar.slider(
    "Time of Day (hrs)",
    min_value=0.0,
    max_value=24.0,
    value=float(st.session_state.transaction_data.get("Time", 43200) / 3600),
    step=0.5,
    format="%.1f"
)
st.session_state.transaction_data["Time"] = float(time_seconds * 3600)

st.sidebar.markdown("<hr style='border-color: #334155;'>", unsafe_allow_html=True)
st.sidebar.markdown("### 📊 Active Context")
st.sidebar.markdown(f"""
<div style='background: #1E293B; padding: 15px; border-radius: 8px; border: 1px solid #334155;'>
    <div style='color: #94A3B8; font-size: 0.9rem;'>Current Amount</div>
    <div style='color: #38BDF8; font-size: 1.5rem; font-weight: bold; margin-bottom: 10px;'>${st.session_state.transaction_data["Amount"]:,.2f}</div>
    <div style='color: #94A3B8; font-size: 0.9rem;'>Timestamp</div>
    <div style='color: #F8FAFC; font-size: 1.1rem; font-weight: bold;'>{int(time_seconds):02d}:{int((time_seconds%1)*60):02d}</div>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# MAIN CONTENT AREA
# ============================================================================

tab1, tab2, tab3 = st.tabs(["🎯 Analysis View", "🔬 Deep Dive", "ℹ️ System Info"])

with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # CTA Button row
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Execute Fraud Inference", width='stretch'):
            if api_status["status"] != "healthy":
                st.error("❌ API backend is offline. Start the uvicorn server.")
            else:
                with st.spinner("Analyzing autoencoder reconstruction loss..."):
                    time.sleep(0.6)  # UX feel
                    result = call_fraud_detection_api(st.session_state.transaction_data)
                    st.session_state.prediction_result = result
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.session_state.prediction_result is not None:
        result = st.session_state.prediction_result
        
        if "error" in result:
            st.error(f"⚠️ Error: {result['error']}")
        else:
            fraud_detected = result.get("fraud_detected", False)
            anomaly_score = result.get("anomaly_score", 0)
            threshold = result.get("threshold", 0.8)
            confidence = result.get("confidence", 0)
            
            # Outcome Banner
            if fraud_detected:
                st.markdown("""
                    <div style="background: linear-gradient(135deg, rgba(220, 38, 38, 0.2) 0%, rgba(153, 27, 27, 0.4) 100%);
                                border: 1px solid #DC2626; padding: 2rem; border-radius: 12px; text-align: center;">
                        <h2 style="color: #F87171 !important; margin: 0; font-size: 2.5rem;">🚨 ANOMALY DETECTED</h2>
                        <p style="color: #FECACA; margin-top: 0.5rem; font-size: 1.1rem;">Transaction blocked based on neural network reconstruction error.</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(6, 95, 70, 0.3) 100%);
                                border: 1px solid #059669; padding: 2rem; border-radius: 12px; text-align: center;">
                        <h2 style="color: #34D399 !important; margin: 0; font-size: 2.5rem;">✅ VERIFIED SAFE</h2>
                        <p style="color: #A7F3D0; margin-top: 0.5rem; font-size: 1.1rem;">Standard transaction pattern recognized. Approved.</p>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Metrics
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Anomaly Score (MSE)", f"{anomaly_score:.4f}", delta=f"{anomaly_score - threshold:.4f} gap", delta_color="inverse")
            m2.metric("System Threshold", f"{threshold:.2f}")
            m3.metric("Model Confidence", f"{confidence:.1%}")
            m4.metric("Network Decision", "REJECT" if fraud_detected else "APPROVE")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Visualizations Split
            g_col1, g_col2 = st.columns([1.2, 1])
            
            with g_col1:
                st.markdown("### Reconstruction Error Map")
                gauge_fig = create_gauge_chart(anomaly_score, threshold)
                st.plotly_chart(gauge_fig, width='stretch')
            
            with g_col2:
                st.markdown("### Inference Details")
                st.markdown(f"""
                <div style="background-color: #1E293B; padding: 1.5rem; border-radius: 12px; border: 1px solid #334155; height: 350px;">
                    <ul style="color: #E2E8F0; font-size: 1.1rem; line-height: 2;">
                        <li><b>Process ID:</b> <code>TXN-{int(time.time())}</code></li>
                        <li><b>Latency:</b> ~45ms</li>
                        <li><b>Input Vector:</b> 30 features</li>
                        <li><b>MSE Deviation:</b> {abs(anomaly_score - threshold):.5f}</li>
                        <li><b>Status:</b> {'<span style="color:#EF4444;">Flagged for Review</span>' if fraud_detected else '<span style="color:#10B981;">Cleared</span>'}</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

with tab2:
    st.markdown("## Data Vector Inspection")
    st.markdown("<p style='color:#94A3B8;'>Detailed breakdown of the latent features passed to the model.</p>", unsafe_allow_html=True)
    
    feature_chart = create_feature_distribution_chart(st.session_state.transaction_data)
    st.plotly_chart(feature_chart, width='stretch')
    
    st.markdown("### Raw Feature Tensor")
    features_table = {
        "Feature Name": FEATURE_NAMES,
        "Raw Value": [st.session_state.transaction_data.get(name, 0) for name in FEATURE_NAMES]
    }
    st.dataframe(features_table, width='stretch', height=400)

with tab3:
    st.markdown("## Architecture & Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background-color: #1E293B; padding: 2rem; border-radius: 12px; border: 1px solid #334155; height: 100%;">
            <h3 style="color: #38BDF8 !important; margin-top:0;">🛡️ Model Pipeline</h3>
            <p style="color: #94A3B8;">This dashboard visualizes inferences from a deep learning Autoencoder trained on historical financial data.</p>
            <ul style="color: #E2E8F0; margin-top: 1rem;">
                <li><b>Input Layer:</b> 30 nodes (Time, Amount + 28 PCA components)</li>
                <li><b>Encoder:</b> Compresses transaction to latent space</li>
                <li><b>Decoder:</b> Attempts to reconstruct original data</li>
                <li><b>Detection:</b> Fraudulent anomalies fail to reconstruct accurately, resulting in a high Mean Squared Error (MSE).</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div style="background-color: #1E293B; padding: 2rem; border-radius: 12px; border: 1px solid #334155; height: 100%;">
            <h3 style="color: #818CF8 !important; margin-top:0;">⚡ Backend Server</h3>
            <p style="color: #94A3B8;">Ensure your FastAPI service is routing traffic correctly.</p>
            <code style="display:block; padding: 1rem; background: #0B0F19; border-radius: 6px; color: #A7F3D0; margin-bottom: 1rem;">
                uvicorn src.inference.app:app --host 0.0.0.0 --port 8000
            </code>
            <p style="color: #94A3B8;"><b>Tech Stack:</b> Python, FastAPI, PyTorch/Scikit-Learn, Streamlit, Plotly</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; border-top: 1px solid #1E293B; padding-top: 2rem;">
    <p style="color: #64748B; font-size: 0.9rem; margin: 0;">
        Powered by Neural Autoencoder Reconstruction • Enterprise Fraud Detection Suite
    </p>
</div>
""", unsafe_allow_html=True)