import streamlit as st

# --- 1. CONFIG & STYLING (Hardened for Stability) ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium")

st.markdown("""
    <style>
    .main-title { font-size: 3rem !important; font-weight: 900; color: #1e3799; text-align: center; margin-bottom: 0px; }
    .sub-header { font-size: 1.2rem; text-align: center; color: #4a69bd; font-weight: 600; margin-bottom: 20px; }
    .card { padding: 20px; border-radius: 12px; margin-bottom: 15px; border-left: 10px solid; background-color: #fcfcfc; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .status-box { padding: 20px; border-radius: 15px; text-align: center; font-size: 1.5rem; font-weight: bold; margin: 10px 0; border: 1px solid rgba(0,0,0,0.1); }
    [data-testid="stSidebar"] { background-color: #f1f4f9; border-right: 2px solid #3498db; }
    </style>
""", unsafe_allow_html=True)

# --- 2. SIMPLE AUTHENTICATION ---
if "unlocked" not in st.session_state:
    st.session_state["unlocked"] = False

if not st.session_state["unlocked"]:
    st.markdown("<h1 class='main-title'>EQUILIBRIUM ENGINE</h1>", unsafe_allow_html=True)
    st.write("### Strategic Revenue Management Dashboard")
    access_code = st.text_input("Enter Access Key", type="password")
    if st.button("Unlock Strategy"):
        if access_code == "Gayan2026":
            st.session_state["unlocked"] = True
            st.rerun()
        else:
            st.error("Access Denied")
    st.stop()

# --- 3. SIDEBAR (Gayan's Architect Panel) ---
with st.sidebar:
    st.markdown(f"<h2 style='color:#1e3799; margin-bottom:0;'>Gayan Nugawela</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#3498db; font-weight:bold;'>Strategic Revenue Architect</p>", unsafe_allow_html=True)
    st.divider()
    
    hotel_name = st.text_input("Property Identity", "Wyndham Garden Salalah")
    h_total = st.number_input("Total Inventory", value=237)
    cu = st.selectbox("Currency", ["OMR", "AED", "SAR", "QAR", "USD", "EUR", "GBP", "LKR", "INR"])
    
    st.divider()
    st.write("### 📊 Financials")
    p01 = st.number_input("P01 Fixed Fee", value=6.90)
    tx_div = st.number_input("Tax Divisor", value=1.2327, format="%.4f")
    ota_comm = st.slider("OTA Comm %", 0, 50, 18) / 100
    
    st.write("### 🍽️ Per Pax Allocation")
    m_bb = st.number_input("Breakfast (BB)", value=2.0
