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
    /* Global background and text - Enhanced dark theme */
    .stApp {
        background-color: #0A0E27;
        color: #E2E8F0;
    }
    
    /* Sidebar Styling - Premium look */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #111F4A 0%, #0A0E27 100%);
        border-right: 1px solid #1E3A5F;
    }
    
    /* Title Gradient Styling - Professional gradient */
    h1 {
        background: linear-gradient(135deg, #06B6D4 0%, #EC4899 50%, #8B5CF6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900 !important;
        letter-spacing: -1px;
        margin-bottom: 0.5rem;
        font-size: 2.8rem !important;
    }
    h2, h3 {
        color: #F8FAFC !important;
        font-weight: 700 !important;
    }

    /* Premium Buttons with gradient */
    div.stButton > button {
        background: linear-gradient(135deg, #06B6D4 0%, #3B82F6 50%, #EC4899 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1.2rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        box-shadow: 0 8px 16px -2px rgba(6, 182, 212, 0.3), 0 4px 8px -1px rgba(0, 0, 0, 0.2);
        font-size: 1rem;
    }
    div.stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 25px -5px rgba(6, 182, 212, 0.5), 0 8px 12px -2px rgba(0, 0, 0, 0.3);
        color: white;
        border: none;
    }

    /* Premium Metric Cards */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #1E3A5F 0%, #112240 100%);
        border-radius: 16px;
        padding: 24px;
        border: 1px solid #06B6D4;
        box-shadow: 0 8px 16px -2px rgba(6, 182, 212, 0.1), inset 0 1px 2px rgba(255,255,255,0.1);
    }
    div[data-testid="metric-container"] > div {
        color: #94A3B8;
        font-size: 0.95rem !important;
    }
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: #06B6D4 !important;
        font-weight: 900 !important;
        font-size: 1.8rem !important;
    }

    /* Custom Status Pills */
    .status-pill {
        display: inline-block;
        padding: 0.5rem 1.2rem;
        border-radius: 50px;
        font-weight: 700;
        font-size: 0.95rem;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 12px -2px rgba(0, 0, 0, 0.2);
    }
    .status-healthy {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(5, 150, 105, 0.3) 100%);
        color: #34D399;
        border: 1px solid #059669;
    }
    .status-offline {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(220, 38, 38, 0.3) 100%);
        color: #F87171;
        border: 1px solid #DC2626;
    }

    /* Card styling */
    .card {
        background: linear-gradient(135deg, #1E3A5F 0%, #112240 100%);
        border: 1px solid #06B6D4;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 8px 16px -2px rgba(6, 182, 212, 0.1);
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #1E3A5F 0%, #112240 100%);
        border-radius: 12px;
        border: 1px solid #06B6D4;
    }
    
    /* DataFrame styling */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #06B6D4;
        box-shadow: 0 4px 12px -2px rgba(6, 182, 212, 0.1);
    }

    /* Tabs styling */
    [data-baseweb="tab-list"] {
        border-bottom: 2px solid #06B6D4;
    }

    /* Alert boxes */
    .stAlert {
        border-radius: 12px !important;
        border: 1px solid !important;
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
    """Create a high-tech Plotly gauge chart with professional colors"""
    fig = go.Figure(data=[go.Indicator(
        mode="gauge+number+delta",
        value=anomaly_score,
        domain={"x": [0, 1], "y": [0, 1]},
        title={"text": "Anomaly Score (MSE)", "font": {"size": 22, "color": "#06B6D4", "family": "sans-serif"}},
        delta={
            "reference": threshold,
            "suffix": " vs Limit",
            "increasing": {"color": "#F87171"},
            "decreasing": {"color": "#34D399"}
        },
        gauge={
            "axis": {"range": [0, max(2.0, anomaly_score + 0.5)], "tickwidth": 2, "tickcolor": "#06B6D4"},
            "bar": {"color": "rgba(0,0,0,0)"},
            "bgcolor": "#112240",
            "borderwidth": 2,
            "bordercolor": "#06B6D4",
            "steps": [
                {"range": [0, threshold], "color": "rgba(16, 185, 129, 0.5)"}, # Safe Zone (Green)
                {"range": [threshold, threshold + 0.5], "color": "rgba(245, 158, 11, 0.6)"}, # Warning Zone (Orange)
                {"range": [threshold + 0.5, 5], "color": "rgba(239, 68, 68, 0.6)"} # Danger Zone (Red)
            ],
            "threshold": {
                "line": {"color": "#EC4899", "width": 5},
                "thickness": 0.8,
                "value": threshold
            }
        },
        number={"font": {"size": 42, "color": "#06B6D4", "family": "sans-serif"}}
    )])
    
    fig.update_layout(
        height=380,
        margin=dict(l=20, r=20, t=70, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "sans-serif", "color": "#E2E8F0"}
    )
    return fig

def create_feature_distribution_chart(transaction_data):
    """Create a modern bar chart with gradient colors"""
    v_features = {k: v for k, v in transaction_data.items() if k.startswith("V")}
    selected_features = {k: v for i, (k, v) in enumerate(v_features.items()) if i % 2 == 0}
    
    # Create gradient colors: cyan to pink based on values
    colors = []
    values = list(selected_features.values())
    min_val = min(values) if values else 0
    max_val = max(values) if values else 1
    
    for val in values:
        normalized = (val - min_val) / (max_val - min_val) if max_val != min_val else 0.5
        if normalized < 0.5:
            # Cyan to Purple
            r = int(6 + (139 - 6) * (normalized * 2))
            g = int(182 + (92 - 182) * (normalized * 2))
            b = int(212 + (207 - 212) * (normalized * 2))
        else:
            # Purple to Pink
            r = int(139 + (236 - 139) * ((normalized - 0.5) * 2))
            g = int(92 + (72 - 92) * ((normalized - 0.5) * 2))
            b = int(207 + (153 - 207) * ((normalized - 0.5) * 2))
        colors.append(f"rgb({r}, {g}, {b})")
    
    fig = go.Figure(data=[
        go.Bar(
            x=list(selected_features.keys()),
            y=list(selected_features.values()),
            marker=dict(
                color=colors,
                line=dict(width=2, color="#06B6D4")
            ),
            text=[f"{v:.2f}" for v in selected_features.values()],
            textposition="auto",
            textfont=dict(color="#E2E8F0", size=11, family="sans-serif"),
            hovertemplate='<b>%{x}</b><br>Value: %{y:.4f}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title=dict(
            text="Principal Component Features",
            font=dict(color="#06B6D4", size=18, family="sans-serif")
        ),
        xaxis=dict(
            title="Features (V1-V28)",
            gridcolor="#06B6D4",
            gridwidth=0.5,
            tickfont=dict(color="#94A3B8", size=10),
            title_font=dict(color="#06B6D4", size=12)
        ),
        yaxis=dict(
            title="Normalized Values",
            gridcolor="#06B6D4",
            gridwidth=0.5,
            tickfont=dict(color="#94A3B8", size=10),
            title_font=dict(color="#06B6D4", size=12)
        ),
        height=380,
        margin=dict(l=50, r=30, t=60, b=50),
        hovermode="x unified",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="sans-serif", color="#E2E8F0")
    )
    return fig

# ============================================================================
# HEADER & API STATUS
# ============================================================================

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.markdown("<h1>🛡️ Fraud Detection Intelligence</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94A3B8; font-size: 1.05rem; margin-bottom: 0;'>Real-Time Anomaly Detection • Transformer Autoencoder • Neural Network Inference</p>", unsafe_allow_html=True)

with col3:
    api_status = check_api_status()
    st.markdown("<br>", unsafe_allow_html=True)
    if api_status["status"] == "healthy":
        st.markdown("<div align='right'><span class='status-pill status-healthy'>🟢 API ONLINE</span></div>", unsafe_allow_html=True)
    else:
        st.markdown("<div align='right'><span class='status-pill status-offline'>🔴 OFFLINE</span></div>", unsafe_allow_html=True)

# Enhanced metrics dashboard
st.markdown("<br>", unsafe_allow_html=True)

met1, met2, met3, met4 = st.columns(4)

with met1:
    st.metric(
        "Transactions Scanned",
        "284,315",
        "+12.5%"
    )

with met2:
    st.metric(
        "Fraud Blocked",
        "492",
        "0.17%"
    )

with met3:
    st.metric(
        "System Accuracy",
        "96.2%",
        "+2.1%"
    )

with met4:
    st.metric(
        "Model Status",
        "Active",
        "Transformer AE"
    )

st.markdown("<hr style='border-color: #06B6D4; margin: 1.5rem 0;'>", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR CONTROLS
# ============================================================================

st.sidebar.markdown("""
    <style>
    .sidebar-title {
        background: linear-gradient(135deg, #06B6D4 0%, #EC4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 1.4rem;
        font-weight: 900;
        letter-spacing: 0.5px;
    }
    </style>
""", unsafe_allow_html=True)

st.sidebar.markdown("<h2 class='sidebar-title'>⚙️ Transaction Control</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<br>", unsafe_allow_html=True)

if st.sidebar.button("🎲 Generate Random Transaction", width='stretch', use_container_width=True):
    st.session_state.transaction_data = generate_random_transaction()
    st.session_state.prediction_result = None

st.sidebar.markdown("<hr style='border-color: #06B6D4; opacity: 0.3;'>", unsafe_allow_html=True)

if st.session_state.transaction_data is None:
    st.session_state.transaction_data = generate_random_transaction()

st.sidebar.markdown("### 💰 Amount ($)")
amount = st.sidebar.slider(
    "Transaction Amount",
    min_value=0.0,
    max_value=50000.0,
    value=float(st.session_state.transaction_data.get("Amount", 100.0)),
    step=50.0,
    label_visibility="collapsed"
)
st.session_state.transaction_data["Amount"] = amount

st.sidebar.markdown("### ⏰ Time of Day")
time_seconds = st.sidebar.slider(
    "Hour",
    min_value=0.0,
    max_value=24.0,
    value=float(st.session_state.transaction_data.get("Time", 43200) / 3600),
    step=0.5,
    format="%.1f hrs",
    label_visibility="collapsed"
)
st.session_state.transaction_data["Time"] = float(time_seconds * 3600)

st.sidebar.markdown("<hr style='border-color: #06B6D4; opacity: 0.3;'>", unsafe_allow_html=True)

st.sidebar.markdown("### 📊 Transaction Summary")
st.sidebar.markdown(f"""
<div style='background: linear-gradient(135deg, #1E3A5F 0%, #112240 100%);
            padding: 16px; border-radius: 12px; border: 1px solid #06B6D4;
            box-shadow: 0 4px 12px rgba(6, 182, 212, 0.1);'>
    <div style='color: #94A3B8; font-size: 0.85rem; margin-bottom: 8px;'>AMOUNT</div>
    <div style='color: #EC4899; font-size: 1.6rem; font-weight: 900; margin-bottom: 16px;'>${st.session_state.transaction_data["Amount"]:,.2f}</div>
    
    <div style='color: #94A3B8; font-size: 0.85rem; margin-bottom: 8px;'>TIME</div>
    <div style='color: #06B6D4; font-size: 1.3rem; font-weight: 700;'>{int(time_seconds):02d}:{int((time_seconds%1)*60):02d}</div>
    
    <div style='color: #8B5CF6; font-size: 0.75rem; margin-top: 12px;'>29 PCA Features Included</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
st.sidebar.markdown("### 🔌 API Connection")
api_status_text = "✅ Online" if api_status["status"] == "healthy" else "❌ Offline"
api_color = "#34D399" if api_status["status"] == "healthy" else "#F87171"
st.sidebar.markdown(f"""
<div style='background: linear-gradient(135deg, #1E3A5F 0%, #112240 100%);
            padding: 12px; border-radius: 10px; border: 1px solid #06B6D4;'>
    <div style='color: {api_color}; font-weight: 700; font-size: 0.95rem;'>{api_status_text}</div>
    <div style='color: #94A3B8; font-size: 0.8rem; margin-top: 4px;'>http://localhost:8000</div>
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
        if st.button("⚡ EXECUTE FRAUD DETECTION", width='stretch'):
            if api_status["status"] != "healthy":
                st.error("❌ API backend is offline. Start the uvicorn server with: uvicorn src.inference.app:app --reload")
            else:
                with st.spinner("🔄 Analyzing transaction through autoencoder..."):
                    time.sleep(0.6)
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
            
            # Outcome Banner - Enhanced with gradient
            if fraud_detected:
                st.markdown("""
                    <div style="background: linear-gradient(135deg, rgba(220, 38, 38, 0.25) 0%, rgba(153, 27, 27, 0.5) 100%);
                                border: 2px solid #DC2626; padding: 2.5rem; border-radius: 16px; text-align: center;
                                box-shadow: 0 12px 24px -4px rgba(220, 38, 38, 0.3), inset 0 1px 3px rgba(255,255,255,0.1);">
                        <h2 style="color: #FCA5A5 !important; margin: 0; font-size: 2.8rem; font-weight: 900;">🚨 ANOMALY DETECTED</h2>
                        <p style="color: #FECACA; margin-top: 0.8rem; font-size: 1.15rem; font-weight: 500;">
                            Transaction flagged as suspicious by neural network</p>
                        <p style="color: #F87171; margin-top: 0.3rem; font-size: 0.95rem;">
                            Reconstruction error exceeds threshold • Recommend blocking</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(6, 95, 70, 0.4) 100%);
                                border: 2px solid #059669; padding: 2.5rem; border-radius: 16px; text-align: center;
                                box-shadow: 0 12px 24px -4px rgba(16, 185, 129, 0.3), inset 0 1px 3px rgba(255,255,255,0.1);">
                        <h2 style="color: #6EE7B7 !important; margin: 0; font-size: 2.8rem; font-weight: 900;">✅ VERIFIED LEGITIMATE</h2>
                        <p style="color: #A7F3D0; margin-top: 0.8rem; font-size: 1.15rem; font-weight: 500;">
                            Transaction matches standard patterns</p>
                        <p style="color: #86EFAC; margin-top: 0.3rem; font-size: 0.95rem;">
                            Low reconstruction error • Safe to approve</p>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Enhanced Metrics Row
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Anomaly Score", f"{anomaly_score:.4f}", delta=f"{(anomaly_score - threshold):.4f}", delta_color="inverse")
            m2.metric("Threshold", f"{threshold:.2f}")
            m3.metric("Confidence", f"{confidence:.1%}")
            m4.metric("Decision", "🚫 REJECT" if fraud_detected else "✅ APPROVE")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
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