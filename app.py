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
        /* High Contrast Sidebar Text */
        [data-testid="stSidebar"] * { color: #ffffff !important; font-weight: 500; }
        .stMetric { background: #ffffff; border-radius: 12px; padding: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .card { padding: 10px; border-radius: 8px; margin-bottom: 8px; border-left: 10px solid; 
                background: #ffffff; color: #1e3a8a; font-weight: bold; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
        /* Status Label Contrast */
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
        px = (rms[0]*1 + rms[1]*2 + rms[2]*3)
        grs = (adr * t_r * nts) + (ev_r * px * nts)
        nt_r = (adr * t_r) / tx
        f_c = sum(q * m_map[p] * (px / t_r) for p, q in mix.items())
        ev_w = (ev_r * px) / tx
        comm = (nt_r - f_c) * cp
        dp = ((nt_r - f_c - comm) - (p01 * t_r)) + (ev_w / t_r)
        tp = (dp * t_r * nts) - (tr_c / tx)
        u = tp / (t_r * nts)
        af = hurdle * 0.75 if nts > 7 else hurdle
        fric = (1 - (tp / grs)) * 100 if grs > 0 else 0
        imp = (t_r / h_inv) * 100
        
        # Color Logic
        if u >= (af + 5): s, c = "OPTIMIZED", "#27ae60"
        elif u >= af: s, c = "MARGINAL", "#f39c12" # Bright Orange
        else: s, c = "DILUTIVE", "#e74c3c"
        
        return {"u":u, "s":s, "c":c, "tp":tp, "fric":fric, "imp":imp}

    def seg_ui(name, clr, ky, r_def, h_def, comm, is_g=False):
        st.markdown(f"<div class='card' style='border-left-color:{clr}'>{name}</div>", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns([1, 2.5, 1, 1.5])
        with c1:
            sr, dr, tr = st.number_input("SGL",0,key=ky+"s"), st.number_input("DBL",0,key=ky+"d"), st.number_input("TPL",0,key=ky+"t")
            n = st.number_input("Nights", 1, 365, key=ky+"n")
        with c2:
            st.write("Meals")
            m1, m2, m3 = st.columns(3)
            q = {"RO": m1.number_input("RO",0,key=ky+"1"), "BB": m1.number_input("BB",0,key=ky+"2"), "HB": m2.number_input("HB",0,key=ky+"3"), "FB": m2.number_input("FB",0,key=ky+"4"), "SAI": m3.number_input("SAI",0,key=ky+"5"), "AI": m3.number_input("AI",0,key=ky+"6")}
            ev, tr_c = (st.number_input("Event",0.0,key=ky+"e"), st.number_input("Trans",0.0,key=ky+"t")) if is_g else (0.0, 0.0)
        with c3:
            adr = st.number_input("Rate", 0.0, 5000.0, float(r_def), key=ky+"r")
            hur = st.number_input("Hurdle", 0.0, 2000.0, float(h_def), key=ky+"h")
        res = run_calc([sr, dr, tr], adr, n, q, comm, hur, ev, tr_c)
        if res:
            with c4:
                st.metric("Wealth/Room", f"{cu} {res['u']:.2f}")
                st.markdown(f"<div class='status-pill' style='background:{res['c']}'>{res['s']}</div>", unsafe_allow_html=True)
                st.write(f"Impact: **{res['imp']:.1f}%**")
                st.write(f"Wealth: **{res['tp']:,.0f}**")
        return res

    # --- RENDER ---
    r1 = seg_ui("OTA Channels", "#2ecc71", "ot", 60, 35, op)
    r2 = seg_ui("Direct / FIT", "#2980b9", "dr", 65, 40, 0.0)
    r3 = seg_ui("Wholesale / B2B", "#e67e22", "wh", 45, 25, 0.2)
    r4 = seg_ui("MICE / Events", "#2c3e50", "mi", 55, 30, 0.0, is_g=True)

    if st.button("🔒 Log Out"):
        st.session_state["auth"] = False
        st.rerun()
