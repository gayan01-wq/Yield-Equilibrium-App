import streamlit as st
import pandas as pd

# --- AUTH ---
def check_pwd():
    if "auth" not in st.session_state:
        st.session_state["auth"] = False
    if not st.session_state["auth"]:
        st.title("🏨 Yield Equilibrium")
        p = st.text_input("Key", type="password")
        if st.button("Open") or (p == "Gayan2026"):
            st.session_state["auth"] = True
            st.rerun()
        return False
    return True

if check_pwd():
    st.set_page_config(layout="wide")
    
    # --- STYLE ---
    st.markdown("""
        <style>
        .stApp { background: #f0f8ff; }
        [data-testid="stSidebar"] { 
            background: #1e293b !important; 
        }
        [data-testid="stSidebar"] * {
            color: #ffffff !important;
        }
        .stMetric { 
            background: white; 
            border-radius: 10px; 
            padding: 10px; 
            border: 1px solid #cbd5e1;
        }
        .card { 
            padding: 10px; 
            border-radius: 8px; 
            border-left: 10px solid; 
            background: white; 
            color: #1e3a8a !important; 
            font-weight: bold; 
        }
        .pill { 
            padding: 4px 12px; 
            border-radius: 20px; 
            color: white !important; 
            font-weight: bold; 
            display: inline-block; 
        }
        </style>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.write("## 👨‍💼 Gayan Nugawela")
        st.write("MBA | CRME | CHRM")
        h_inv = st.number_input("Rooms", 1, 1000, 237)
        st.write("---")
        tx = st.number_input("Tax", 1.0, 2.0, 1.2327)
        op_pct = st.slider("OTA %", 0, 50, 18)
        cu = st.selectbox("Cur", ["OMR","AED","USD"])

    st.title("🏨 Yield Equilibrium Center")

    def run_calc(rms, adr, nts, cp, hur, ev=0, tr=0):
        t_r = sum(rms)
        if t_r <= 0: return None
        px = (rms[0]*1) + (rms[1]*2) + (rms[2]*3)
        nt_r = (adr * t_r) / tx
        comm = nt_r * (cp / 100)
        tp = (nt_r - comm + (ev*px/tx)) * nts - (tr/tx)
        u = tp / (t_r * nts)
        imp = (t_r / h_inv) * 100
        af = hur * 0.75 if nts > 7 else hur
        if u >= (af + 5): s, c = "OPTIMIZED", "#28a745"
        elif u >= af: s, c = "MARGINAL", "#f59e0b"
        else: s, c = "DILUTIVE", "#ef4444"
        return {"u":u, "s":s, "c":c, "tp":tp, "imp":imp}

    def seg_ui(nm, cl, ky, r_d, h_d, cp_v, is_g=False):
        st.markdown(f"<div class='card' style='border-left-color:{cl}'>{nm}</div>", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns([1, 2, 1, 1.5])
        with c1:
            sr = st.number_input("SGL", 0, key=ky+"_s")
            dr = st.number_input("DBL", 0, key=ky+"_d")
            tr = st.number_input("TPL", 0, key=ky+"_t")
            n = st.number_input("Nts", 1, 365, key=ky+"_n")
