import streamlit as st
import pandas as pd

# --- AUTHENTICATION ---
def check_pwd():
    if "auth" not in st.session_state:
        st.session_state["auth"] = False
    if not st.session_state["auth"]:
        st.title("🏨 Yield Equilibrium Center")
        p = st.text_input("Access Key", type="password")
        if st.button("Unlock Dashboard") or (p == "Gayan2026"):
            st.session_state["auth"] = True
            st.rerun()
        return False
    return True

if check_pwd():
    st.set_page_config(layout="wide", page_title="Yield Equilibrium")
    
    # --- EXECUTIVE INTERFACE STYLING ---
    st.markdown("""
        <style>
        .stApp { background: #f0f8ff; }
        [data-testid="stSidebar"] { background: #1e293b !important; }
        /* Force Sidebar text to be white and bold */
        [data-testid="stSidebar"] * { color: #ffffff !important; }
        .stMetric { background: white; border-radius: 12px; padding: 10px; border: 1px solid #cbd5e1; }
        .card { padding: 12px; border-radius: 10px; border-left: 10px solid; 
                background: white; color: #1e3a8a !important; font-weight: bold; margin-bottom: 10px; }
        .pill { padding: 5px 15px; border-radius: 20px; color: white !important; font-weight: bold; display: inline-block; }
        </style>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown("## 👨‍💼 Gayan Nugawela")
        st.write("MBA | CRME | CHRM | RevOps")
        st.divider()
        h_inv = st.number_input("Total Property Inventory", 1, 1000, 237)
        st.write("---")
        tx = st.number_input("Tax Divisor", 1.0, 2.0, 1.2327)
        op_pct = st.slider("OTA Commission %", 0, 50, 18)
        cu = st.selectbox("Currency Unit", ["OMR","AED","USD","SAR"])

    st.title("🏨 Yield Equilibrium Center")
    st.markdown("---")

    def run_calc(rms, adr, nts, cp, hur, ev=0, tr=0):
        t_r = sum(rms)
        if t_r <= 0: return None
        px = (rms[0]*1) + (rms[1]*2) + (rms[2]*3)
        nt_r = (adr * t_r) / tx
        comm = nt_r * (cp / 100)
        # Revenue Equilibrium Math
        tp = (nt_r - comm + (ev*px/tx)) * nts - (tr/tx)
        u = tp / (t_r * nts)
        imp = (t_r / h_inv) * 100
        af = hur * 0.75 if nts > 7 else hur
        # Status Logic
        if u >= (af + 5): s, c = "OPTIMIZED", "#28a745"
        elif u >= af: s, c = "MARGINAL", "#f59e0b"
        else: s, c = "DILUTIVE", "#ef4444"
        return {"u":u, "s":s, "c":c, "tp":tp, "imp":imp}

    def seg_ui(nm, cl, ky, r_d, h_d, cp_v, is_g=False):
        st.markdown(f"<div class='card' style='border-left-color:{cl}'>{nm}</div>", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns([1, 2
