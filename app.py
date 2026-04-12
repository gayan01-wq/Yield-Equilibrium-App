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
            background: #0e1117 !important; 
        }
        /* Make sidebar text white */
        [data-testid="stSidebar"] * {
            color: white !important;
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
            color: #004085 !important; 
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
        ev_w = (ev * px) / tx
        comm = (nt_r - f_c) * cp
        dp = ((nt_r-f_c-comm)-(p01*t_r))+(ev_w/t_r)
        tp = (dp * t_r * nts) - (tr / tx)
        u = tp / (t_r * nts)
        imp = (t_r / h_inv) * 100
        af = hur * 0.75 if nts > 7 else hur
        if u >= (af + 5): s, c = "OPTIMIZED", "#28a745"
        elif u >= af: s, c = "MARGINAL", "#ffc107"
        else: s, c = "DILUTIVE", "#dc3545"
        return {"u":u, "s":s, "c":c, "tp":tp, "imp":imp}

    def seg_ui(nm, cl, ky, r_d, h_d, cp, is_g=False):
        st.markdown(f"<div class='card' style='border-left-color:{cl}'>{nm}</div>", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns([1, 2, 1, 1.5])
        with c1:
            sr = st.number_input("SGL", 0, key=ky+"s")
            dr = st.number_input("DBL", 0, key=ky+"d")
            tr = st.number_input("TPL", 0, key=ky+"t")
            n = st.number_input("Nts", 1, 365, key=ky+"n")
        with c2:
            st.write("Meals (BB Default)")
            ev = st.number_input("Ev",0.,key=ky+"e") if is_g else 0.0
            tr_c = st.number_input("Tr",0.,key=ky+"t") if is_g else 0.0
        with c3:
            adr = st.number_input("Rate", 0.0, 5000.0, float(r_d), key=ky+"r")
            hur = st.number_input("Hur", 0.0, 2000.0, float(h_d), key=ky+"h")
        res = run_calc([sr, dr, tr], adr, n, cp, hur, ev, tr_c)
        if res:
            with c4:
                st.metric("Wealth", f"{cu} {res['u']:.2f}")
                st.markdown(f"<div class='pill' style='background:{res['c']}'>{res['s']}</div>", unsafe_allow_html=True)
                st.write(f"Impact: {res['imp']:.1f}%")
        return res

    # --- RENDER ---
    r1 = seg_ui("OTA Channels", "#28a745", "ot", 60, 35, op)
    r2 = seg_ui("Direct / FIT", "#007bff", "dr", 65, 40, 0.0)
    r3 = seg_ui("MICE", "#6c757d", "mi", 55, 30, 0.0, True)

    st.divider()
    active = {k: v for k, v in {"OTA":r1,"Direct":r2,"MICE":r3}.items() if v}
    if active:
        st.subheader("📊 Yield Analysis Ratio")
        df = pd.DataFrame({
            "Segment": list(active.keys()),
            "Wealth": [v['u'] for v in active.values()],
            "Impact": [v['imp'] for v in active.values()]
        }).set_index("Segment")
        st.bar_chart(df)

    if st.button("Log Out"):
        st.session_state["auth"] = False
        st.rerun()
