import streamlit as st

# --- 1. CONFIG & BEAUTIFICATION ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium")

st.markdown("""
    <style>
    .main-title { font-size: 3rem !important; font-weight: 800; color: #2c3e50; text-align: center; border-bottom: 5px solid #3498db; padding-bottom: 10px; margin-bottom: 20px; }
    .card { padding: 15px; border-radius: 12px; margin-bottom: 15px; border-left: 10px solid; font-weight: bold; background-color: #fcfcfc; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .status-box { padding: 20px; border-radius: 15px; text-align: center; font-size: 1.5rem; font-weight: bold; margin: 10px 0; border: 1px solid rgba(0,0,0,0.1); }
    .stNumberInput label { font-weight: bold !important; color: #2c3e50 !important; }
    </style>
""", unsafe_allow_html=True)

# --- 2. AUTHENTICATION ---
if "auth" not in st.session_state:
    st.session_state["auth"] = False

if not st.session_state["auth"]:
    st.markdown("<h1 class='main-title'>Yield Equilibrium</h1>", unsafe_allow_html=True)
    st.subheader("Strategic Decision Support System")
    pwd = st.text_input("Access Key", type="password")
    if st.button("Unlock Dashboard"):
        if pwd == "Gayan2026":
            st.session_state["auth"] = True
            st.rerun()
        else:
            st.error("Invalid Key")
    st.stop()

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("Architect")
    st.write("**Gayan Nugawela**")
    st.caption("Revenue management specialist- SME")
    st.divider()
    
    h_total = st.number_input("Total Inventory Baseline", 1, 5000, 237)
    cu = st.selectbox("Currency", ["OMR", "AED", "SAR", "QAR", "USD", "EUR", "LKR"])
    
    st.divider()
    st.write("### Statutory & Costs")
    p01 = st.number_input("P01 Fixed Fee", 0.0, 100.0, 6.90)
    tx = st.number_input("Tax Divisor", 1.0, 2.5, 1.2327, format="%.4f")
    comm_pct = st.slider("OTA Commission %", 0, 50, 18) / 100
    
    st.divider()
    st.write("### Unit Meal Costs")
    m_bb = st.number_input("BB", 0.0, 500.0, 2.0)
    m_hb = st.number_input("HB", 0.0, 500.0, 8.0)
    m_fb = st.number_input("FB", 0.0, 500.0, 14.0)
    m_ai = st.number_input("AI", 0.0, 500.0, 27.0)
    m_map = {"RO": 0.0, "
