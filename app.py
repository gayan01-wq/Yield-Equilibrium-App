import streamlit as st
import pandas as pd

def check_password():
    if "auth" not in st.session_state:
        st.session_state["auth"] = False
    if not st.session_state["auth"]:
        st.title("🏨 Yield Equilibrium Center")
        p = st.text_input("Access Key", type="password")
        if st.button("Unlock") or (p == "Gayan2026"): 
            st.session_state["auth"] = True
            st.rerun()
        return False
    return True

if check_password():
    st.set_page_config(layout="wide", page_title="Yield Equilibrium SME")
    
    st.markdown("""
        <style>
        .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
        [data-testid="stSidebar"] { background-color: #0e1117 !important; }
        [data-testid="stSidebar"] * { color: #ffffff !important; }
        .stMetric { background: #ffffff; border-radius: 12px; padding: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .card { padding: 10px; border-radius: 8px; margin-bottom: 8px; border-left: 10px solid; 
                background: #ffffff; color: #1e3a8a; font-weight: bold; }
        .status-pill { padding: 5px 12px; border-radius: 20px; color: #ffffff !important; 
                       font-weight: bold; text-shadow: 1px 1px 2px rgba(0,0,0,0.5); display: inline-block; }
        </style>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown("<h2 style='color:#60a5fa;'>Architect</h2>", unsafe_allow_html=True)
        st.markdown("### Gayan Nugawela")
        st.markdown("<small>MBA | CRME | CHRM | RevOps</small>", unsafe_allow_html=True)
        st.divider()
        h_inv = st.number_input("Total Inventory", 1, 1000, 237)
        st.markdown("#### 🍽️ Meals (Net)")
        b, l, d = st.number_input("BB",0.,500.,2.), st.number_input("LN",0.,500.,6.), st.number_input("DN",0.,500.,6.)
        s, a = st.number_input("SAI",0.,500.,8.), st.number_input("AI",0.,500.,15.)
        m_map = {"RO":0, "BB":b, "HB":b+d, "FB":b+l+d, "SAI":b+l+d+s, "AI":b+l+d+s+a}
        p01, tx = st.number_input("P01 Fee",0.,100.,6.9), st.number_input("Tax Divisor",1.,2.,1.2327)
        op = st.slider("OTA Comm %", 0, 50, 18) / 100
        cu = st.selectbox("Currency", ["OMR", "AED", "SAR", "EUR", "USD"])

    st.title("🏨 Yield Equilibrium Center")

    def run_calc(rms, adr, nts, mix, cp, hurdle, ev_r=0, tr_c=0):
        t_r = sum(rms)
        if t_r <= 0: return None
        px = (rms[0]*1 + rms[1]*2 + rms[2]*3)
        nt_r = (adr * t_r) / tx
        f_c = sum(q * m_map[p] * (px / t_r) for p, q in mix.items())
        ev_w = (ev_r * px)
