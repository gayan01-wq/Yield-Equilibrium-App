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
            background: #e6f3ff !important; 
        }
        .stMetric { 
            background: white; 
            border-radius: 10px; 
            padding: 10px; 
        }
        .card { 
            padding: 10px; 
            border-radius: 8px; 
            border-left: 10px solid; 
            background: white; 
            color: #004085; 
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
        st.write("### 🍽️ Meals")
        b = st.number_input("BB", 0.0, 500.0, 2.0)
        l = st.number_input("LN", 0.0, 500.0, 6.0)
        d = st.number_input("DN", 0.0, 500.0, 6.0)
        s = st.number_input("SAI", 0.0, 500.0, 8.0)
        a = st.number_input("AI", 0.0, 500.0, 15.0)
        m_map = {
            "RO": 0, "BB": b, "HB": b+d,
            "FB": b+l+d, "SAI": b+l+d+s, 
            "AI": b+l+d+s+a
        }
        p01 = st.number_input("P01", 0.0, 100.0, 6.9)
        tx = st.number_input("Tax", 1.0, 2.0, 1.2327)
        op_val = st.slider("OTA %", 0, 50, 18)
        op = op_val / 100
        cu = st.selectbox("Cur", ["OMR","AED","USD"])

    st.title("🏨 Yield Equilibrium Center")

    def run_calc(rms, adr, nts, cp, hur, ev=0, tr=0):
        t_r = sum(rms)
        if t_r <= 0: return None
        px = (rms[0]*1) + (rms[1]*2) + (rms[2]*3)
        nt_r = (adr * t_r) / tx
        f_c = sum(m_map["BB"]*(px/t_r) for i in range(1))
        # (Simplified meal logic for stability)
        ev_w = (ev * px) / tx
        comm = (nt_r - f_c) * cp
        dp = ((nt_r-f_c-comm)-(p01*t_r))+(ev_w/t_r)
        tp = (dp * t_r * nts) - (tr / tx)
        u = tp / (t_r * n
