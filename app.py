import streamlit as st
import pandas as pd

# --- CONFIG & THEME ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium", initial_sidebar_state="expanded")

# Custom CSS for UI Stability
st.markdown("""
    <style>
    .stMetric {background:#fff; border:1px solid #eee; padding:15px; border-radius:12px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);}
    .card {padding:10px; border-radius:8px; margin-bottom:8px; border-left:10px solid; font-weight:bold; font-size: 1.1em;}
    .pillar-box {background:#f8f9fa; padding:15px; border-radius:10px; border-top:4px solid #2c3e50; min-height: 200px;}
    .density-warn {color: #e67e22; font-weight: bold; border: 1px solid #e67e22; padding: 5px; border-radius: 5px; display: block; margin-top: 5px;}
    .wealth-box {background: #fcfcfc; border: 1px solid #ddd; padding: 10px; border-radius: 8px; margin-top: 10px;}
    </style>
""", unsafe_allow_html=True)

# --- PASSWORD PROTECTION ---
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
        st.caption("MBA | CRME | CHRM | RevOps")
        st.divider()
        
        st.title("⚙️ Global Settings")
        h_nm = st.text_input("Hotel", "Wyndham Garden Salalah")
        h_cp = st.number_input("Total Inventory", 1, 1000, 158)
        
        st.header("🍽️ Meals (Net)")
        b = st.number_input("BB", 0., 500., 2.0)
        l = st.number_input("LN", 0., 500., 6.0)
        d_cost = st.number_input("DN", 0., 500., 6.0)
        s_cost = st.number_input("SAI", 0., 500., 8.0)
        a_cost = st.number_input("AI", 0., 500., 15.0)
        
        m = {
            "RO": 0.0, "BB": b, "HB": b + d_cost, 
            "FB": b + l + d_cost, "SAI": b + l + d_cost + s_cost, 
            "AI": b + l + d_cost + s_cost + a_cost
        }
        
        p01 = st.number_input("P01 Fee", 0., 100., 6.9)
        tx = st.number_input("Tax Div", 1.0, 2.5, 1.2327, format="%.4f")
        op = st.slider("OTA Comm %", 0, 50, 18) / 100
        cu = st.selectbox("Currency", ["OMR", "AED", "SAR", "USD", "LKR", "GBP", "EUR"])
        
        st.divider()
        st.subheader("📈 Yield Multipliers")
        risk_premium = 0.15 # 15% displacement risk

    # --- CORE ENGINE WITH DENSITY LOGIC ---
    def run(rms, adr, nts, mix, cp, fl, ev_rev=0, total_tr_cost=0):
        t_rms = sum(rms)
        if t_rms <= 0: return None
        
        pax = (rms[0]*1 + rms[1]*2 + rms[2]*3)
        inv_impact = (t_rms / h_cp) * 100
        
        # 20% DENSITY LOGIC
        effective_hurdle =
