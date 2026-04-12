import streamlit as st
import pandas as pd

# --- PASSWORD PROTECTION ---
def check_password():
    if "auth" not in st.session_state:
        st.session_state["auth"] = False
    if not st.session_state["auth"]:
        st.title("🏨 Yield Equilibrium Center")
        pwd = st.text_input("Access Key", type="password")
        if st.button("Unlock") or (pwd == "Gayan2026"): 
            st.session_state["auth"] = True
            st.rerun()
        return False
    return True

if check_password():
    # --- UNIVERSAL PREMIUM STYLING ---
    st.set_page_config(layout="wide", page_title="Yield Equilibrium SME")
    
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }
        [data-testid="stSidebar"] {
            background-color: #0e1117 !important;
            color: white;
        }
        .stMetric {
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            padding: 15px;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }
        .card {
            padding: 12px;
            border-radius: 12px;
            margin-bottom: 10px;
            border-left: 10px solid;
            font-weight: bold;
            background: rgba(255, 255, 255, 0.6);
            box-shadow: 2px 2px 5px rgba(0,0,0,0.03);
        }
        h1, h2, h3 { color: #1e3a8a; }
        </style>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown("<h2 style='color:white;'>👨‍💼 Architect</h2>", unsafe_allow_html=True)
        st.markdown("<h3 style='color:#60a5fa; margin-bottom:0;'>Gayan Nugawela</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color:white; font-size:14px;'>MBA | CRME | CHRM | RevOps</p>", unsafe_allow_html=True)
        st.caption("Revenue Management Expert & SME")
        st.divider()
        
        st.title("⚙️ Global Settings")
        h_nm = st.text_input("Hotel Entity", "Global Portfolio Audit")
        h_cp = st.number_input("Total Inventory", 1, 1000, 158)
        
        st.markdown("### 🍽️ Meals (Net)")
        b = st.number_input("BB", 0.0, 500.0, 2.0)
        l = st.number_input("LN", 0.0, 500.0, 6.0)
        d = st.number_input("DN", 0.0, 500.0, 6.0)
        s = st.number_input("SAI", 0.0, 500.0, 8.0)
        a = st.number_input("AI", 0.0, 500.0, 15.0)
        m = {"RO":0, "BB":b, "HB":b+d, "FB":b+l+d, "SAI":b+l+d+s, "AI":b+l+d+s+a}
        
        p01 = st.number_input("P01 Fee", 0.0, 100.0, 6.9)
        tx = st.number_input("Tax Divisor", 1.0, 2.0, 1.2327, format="%.4f")
        op = st.slider("OTA Commission %", 0, 50, 18) / 100
        cu = st.selectbox("Currency", ["OMR", "AED", "SAR", "THB", "EUR", "GBP", "USD"])

    st.title("🏨 Yield Equilibrium Center")
    st.markdown("---")

    def run(rms, adr, nts, mix, cp, fl, ev_rev=0, total_tr_cost=0):
        t_rms = sum(rms)
        if t_rms <= 0:
