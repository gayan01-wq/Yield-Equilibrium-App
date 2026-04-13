import streamlit as st
import pandas as pd

# --- 1. CONFIG & THEME ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 1.8rem !important; }
    .stMetric {background:#fff; border:1px solid #eee; padding:15px; border-radius:12px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);}
    .card {padding:12px; border-radius:10px; margin-bottom:10px; border-left:12px solid; font-weight:bold; color: #2c3e50;}
    .dominance-warn {color: #d35400; font-weight: bold; border: 2px solid #d35400; padding: 8px; border-radius: 5px; text-align: center; background: #fff5f0;}
    .pillar-box {background:#f8f9fa; padding:15px; border-radius:10px; border-top:4px solid #2c3e50; min-height: 180px;}
    </style>
""", unsafe_allow_html=True)

# --- 2. PASSWORD PROTECTION ---
def check_password():
    if "auth" not in st.session_state:
        st.session_state["auth"] = False
    if not st.session_state["auth"]:
        st.title("🏨 Yield Equilibrium Center")
        pwd = st.text_input("Access Key", type="password")
        if st.button("Unlock") or (pwd == "Gayan2026"): 
            if pwd == "Gayan2026":
                st.session_state["auth"] = True
                st.rerun()
            elif pwd != "": st.error("Invalid Key")
        return False
    return True

if check_password():
    with st.sidebar:
        st.title("👨‍💼 Architect")
        st.subheader("Gayan Nugawela")
        # --- TITLE UPDATE ---
        st.caption("Revenue management specialist- SME")
        st.divider()
        st.header("⚙️ Global Architecture")
        h_nm = st.text_input("Hotel Name", "Wyndham Garden Salalah")
        h_cp = st.number_input("Total Inventory", 1, 1000, 158)
        cu = st.selectbox("Currency", ["OMR", "AED", "SAR", "USD", "LKR"])
        
        st.divider()
        st.header("📊 Statutory & Costs")
        c_side1, c_side2 = st.columns(2)
        p01 = c_side1.number_input("P01 Fee", 0., 100., 6.90)
        # --- TAX DIVISOR FIX (4 Decimal Places) ---
        tx = c_side2.number_input("Tax Div", 1.0000, 2.5000, 1.2327, format="%.4f", step=0.0001)
        op_comm = st.slider("OTA Comm %", 0, 50, 18) / 100
        
        st.divider()
        st.header("🍽️ Meal Cost Allocation")
        mc_bb = st.number_input("BB Cost", 0.0, 500.0, 2.0)
        mc_hb = st.number_input("HB Cost", 0.0, 500.0, 8.0)
        mc_fb = st.number
