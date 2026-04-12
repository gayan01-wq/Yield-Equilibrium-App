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
    
    # --- EXECUTIVE INTERFACE STYLE ---
    st.markdown("""
        <style>
        .stApp { background: #f0f8ff; }
        [data-testid="stSidebar"] { 
            background: #0e1117 !important; 
        }
        /* Force high-visibility white text */
        [data-testid="stSidebar"] * { 
            color: #ffffff !important; 
            font-weight: bold !important;
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
        st.write("## 👨‍💼 Architect")
        st.write("### Gayan Nugawela")
        st.write("MBA | CRME | CHRM | RevOps")
        st.divider()
        h_inv = st.number_input("Inventory", 1, 1000, 237)
        st.write("---")
        tx = st.number_input("Tax", 1.0, 2.0, 1.2327)
        op_pct = st.slider("OTA %", 0, 50, 18)
        cu = st.selectbox("Cur", ["OMR","AED","USD","SAR"])

    st.title("🏨 Yield Equilibrium Center")

    def run_calc(rms, adr, nts, cp, hur, ev=0, tr=0):
        t_r = sum(rms)
        if t_r <= 0: return None
        px = (rms[0]*1) + (rms[1]*2) + (rms[2]*3)
        nt_r = (adr * t_r) / tx
        comm = nt_r * (cp / 100)
        # Strategic Wealth Logic
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
        with c2:
            st.write("Audit Adjustments")
            ev = st.number_input("Ev/Pax", 0., key=ky+"_e") if is_g else 0.0
            tc = st.number_input("Cost", 0., key=ky+"_tr") if is_g else 0.0
        with c3:
            adr = st.number_input("Rate", 0.0, 5000.0, float(r_d), key=ky+"_r")
            hur = st.number_input("Hur", 0.0, 2000.0, float(h_d), key=ky+"_h")
        res = run_calc([sr, dr, tr], adr, n, cp_v, hur, ev, tc)
        if res:
            with c4:
                st.metric("Wealth", f"{cu} {res['u']:.2f}")
                st.markdown(f"<div class='pill' style='background:{res['c']}'>{res['s']}</div>", unsafe_allow_html=True)
                st.write(f"Impact: {res['imp']:.1f}%")
        return res

    # --- RENDER SEGMENTS ---
    r1 = seg_ui("OTA Channels", "#2ecc71", "ot", 60, 35, op_pct)
    r2 = seg_ui("Direct / FIT", "#3b82f6", "dr", 65, 40, 0)
    r3 = seg_ui("MICE / Groups", "#64748b", "mi", 55, 30, 0, True)

    st.divider()
    if st.button("Log Out", key="exit"):
        st.session_state["auth"] = False
        st.rerun()
