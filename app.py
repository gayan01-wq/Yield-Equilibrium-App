import streamlit as st
import pandas as pd

# --- ACCESS ---
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
    st.set_page_config(layout="wide", page_title="Yield Equilibrium")
    
    # --- LIGHT BLUE THEME ---
    st.markdown("""
        <style>
        .stApp { background-color: #f0f8ff; }
        [data-testid="stSidebar"] { background-color: #e6f3ff !important; }
        [data-testid="stSidebar"] * { color: #004085 !important; }
        .stMetric { background: white; border-radius: 12px; padding: 10px; border: 1px solid #cce5ff; }
        .card { padding: 10px; border-radius: 8px; margin-bottom: 8px; border-left: 10px solid; 
                background: white; color: #004085; font-weight: bold; }
        .status-pill { padding: 4px 12px; border-radius: 20px; color: white !important; font-weight: bold; display: inline-block; }
        </style>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown("## 👨‍💼 Architect")
        st.subheader("Gayan Nugawela")
        st.write("MBA | CRME | CHRM | RevOps")
        st.divider()
        h_inv = st.number_input("Total Inventory", 1, 1000, 237)
        st.markdown("### 🍽️ Meals (Net)")
        b = st.number_input("BB", 0.0, 500.0, 2.0)
        l = st.number_input("LN", 0.0, 500.0, 6.0)
        d = st.number_input("DN", 0.0, 500.0, 6.0)
        s = st.number_input("SAI", 0.0, 500.0, 8.0)
        a = st.number_input("AI", 0.0, 500.0, 15.0)
        m_map = {"RO":0, "BB":b, "HB":b+d, "FB":b+l+d, "SAI":b+l+d+s, "AI":b+l+d+s+a}
        p01 = st.number_input("P01 Fee", 0.0, 100.0, 6.9)
        tx = st.number_input("Tax Divisor", 1.0, 2.0, 1.2327)
        op = st.slider("OTA Comm %", 0, 50, 18) / 100
        cu = st.selectbox("Currency", ["OMR", "AED", "SAR", "EUR", "USD"])

    st.title("🏨 Yield Equilibrium Center")

    def run_calc(rms, adr, nts, mix, cp, hurdle, ev_r=0, tr_c=0):
        t_r = sum(rms)
        if t_r <= 0: return None
        # Short lines to prevent SyntaxErrors
        px = (rms[0]*1) + (rms[1]*2) + (rms[2]*3)
        nt_r = (adr * t_r) / tx
        f_c = sum(q * m_map[p] * (px / t_r) for p, q in mix.items())
        ev_w = (ev_r * px) / tx
        comm = (nt_r - f_c) * cp
        dp = ((nt_r - f_c - comm) - (p01 * t_r)) + (ev_w / t_r)
        tp =
