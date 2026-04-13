import streamlit as st

# --- 1. CONFIG ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium", initial_sidebar_state="expanded")

# --- 2. THEME & CSS ---
st.markdown("""
    <style>
    .main-title { font-size: 3rem !important; font-weight: 800; color: #2c3e50; text-align: center; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 2px; border-bottom: 5px solid #3498db; padding-bottom: 5px; }
    .framework-subtitle { text-align: center; color: #7f8c8d; font-style: italic; font-size: 1.1rem; margin-bottom: 30px; }
    [data-testid="stMetricValue"] { font-size: 1.8rem !important; }
    .stMetric {background:#fff; border:1px solid #eee; padding:15px; border-radius:12px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);}
    .card {padding:12px; border-radius:10px; margin-bottom:10px; border-left:12px solid; font-weight:bold; color: #2c3e50;}
    .coach-note {padding: 12px; border-radius: 8px; font-size: 0.95rem; margin-top: 10px; border: 2px solid #eee; background-color: #fdfefe; line-height: 1.4;}
    .pillar-box {background:#f8f9fa; padding:15px; border-radius:10px; border-top:4px solid #2c3e50; min-height: 180px;}
    .stNumberInput input { font-size: 1.1rem !important; font-weight: bold !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. AUTHENTICATION ---
if "auth" not in st.session_state:
    st.session_state["auth"] = False

if not st.session_state["auth"]:
    st.markdown("<h1 class='main-title'>Yield Equilibrium</h1>", unsafe_allow_html=True)
    with st.container():
        pwd = st.text_input("Access Key", type="password")
        if st.button("Unlock Dashboard"):
            if pwd == "Gayan2026":
                st.session_state["auth"] = True
                st.rerun()
            else:
                st.error("Invalid Key")
    st.stop() # Stops execution here if not authorized

# --- 4. SIDEBAR (Only shows if Auth is True) ---
with st.sidebar:
    st.title("👨‍💼 Architect")
    st.subheader("Gayan Nugawela")
    st.caption("Revenue management specialist- SME")
    st.divider()
    
    h_nm = st.text_input("Hotel Name", "Wyndham Garden Salalah")
    h_cp = st.number_input("Total Inventory", 1, 1000, 158)
    currencies = ["OMR", "AED", "SAR", "QAR", "BHD", "KWD", "EUR", "GBP", "USD", "LKR", "INR"]
    cu = st.selectbox("Currency", sorted(currencies))
    
    st.divider()
    st.header("📊 Statutory & Costs")
    c_side1, c_side2 = st.columns([1, 1.2]) 
    p01 = c_side1.number_input("P01 Fee", 0.0, 100.0, 6.90)
    tx = c_side2.number_input("Tax Div", 1.0, 2.5, 1.2327, format="%.4f", step=0.0001)
    op_comm = st.slider("OTA Comm %", 0, 50, 18) / 1
