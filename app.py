import streamlit as st
import pandas as pd

# --- 1. CONFIG & THEME ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 1.8rem !important; }
    .stMetric {background:#fff; border:1px solid #eee; padding:15px; border-radius:12px;}
    .card {padding:12px; border-radius:10px; margin-bottom:10px; border-left:12px solid; font-weight:bold; color: #2c3e50;}
    .dominance-warn {color: #d35400; font-weight: bold; border: 2px solid #d35400; padding: 8px; border-radius: 5px; text-align: center; background: #fff5f0;}
    </style>
""", unsafe_allow_html=True)

# --- 2. PASSWORD PROTECTION ---
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
        st.divider()
        h_nm = st.text_input("Hotel Name", "Wyndham Garden Salalah")
        h_cp = st.number_input("Total Inventory", 1, 1000, 158)
        cu = st.selectbox("Currency", ["OMR", "AED", "SAR", "USD", "LKR"])
        st.divider()
        c_side1, c_side2 = st.columns(2)
        p01 = c_side1.number_input("P01 Fee", 0., 100., 6.9)
        tx = c_side2.number_input("Tax Div", 1.0, 2.5, 1.2327, format="%.4f")
        op_comm = st.slider("OTA Comm %", 0, 50, 18) / 100
        st.divider()
        b_cost = st.number_input("BB Cost", 0., 500., 2.0)
        d_cost = st.number_input("DN Cost", 0., 500., 6.0)
        m_map = {"RO": 0.0, "BB": b_cost, "HB": b_cost+d_cost, "FB": b_cost+12.0, "SAI": b_cost+14.0, "AI": b_cost+21.0}

    def run_calculation(rms, adr, nts, mix, cp, fl, ev_rev=0):
        t_rms = sum(rms)
        if t_rms <= 0: return None
        pax = (rms[0]*1 + rms[1]*2 + rms[2]*3)
        inv_impact = (t_rms / h_cp) * 100
        eff_h = fl * 1.25 if inv_impact >= 50.0 else fl
        if nts >= 5: eff_h *= 0.90
        nt_rev = (adr * t_rms) / tx
        fb_cost = sum(q * m_map[p] * (pax / t_rms) for p, q in mix.items())
        dp = ((nt_rev - fb_cost - ((nt_rev-fb_cost)*cp)) - (p01 * t_rms)) + ((ev_rev * pax) / tx / t_rms)
        tp = (dp * t_rms * nts)
        u = tp / (t_rms * nts)
        if u < (eff_h * 0.8) or tp <= 0: lb, cl = "DILUTIVE", "#e74c3c"
        elif u < eff_h: lb, cl = "MARGINAL", "#f1c40f"
        else: lb, cl = "OPTIMIZED", "#27ae60"
        return {"u": u, "s": lb, "c": cl, "tp": tp, "impact": inv_impact, "risk": inv_impact >= 50.0}

    def seg(nm, cl, bg, kp, ad_d, fl_d, cp, is_group=False):
        st.markdown(f"<div class='card' style='background:{bg};border-left-color:{cl}'>{nm}</div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1.3, 2.2, 1.5])
        with c1:
            st.caption("Stay Dynamics")
            sgl, dbl, tpl = st.number_input("SGL",0,key=kp+"s"), st.number_input("DBL",0,key=kp+"d"), st.number_input("TPL",0,key=kp+"t")
            nt = st.number_input("Nights", 1, key=kp+"n")
        with c2:
            st.caption("Strategy & Meals")
            ca, cb, cc = st.columns(3)
            q = {"RO": ca.number_input("RO", 0, key=kp+"ro"), "BB": ca.number_input("BB", 0, key=kp+"b"),
                 "HB": cb.number_input("HB", 0, key=kp+"h"), "FB": cb.number_input("FB", 0, key=kp+"f"),
                 "SAI": cc.number_input("SAI", 0, key=kp+"sa"), "AI": cc.number_input("AI", 0, key=kp+"ai")}
            
            # --- STABLE PRICING FRAME ---
            with st.container(border=True):
                st.caption("PRICING FRAME")
                r_col, h_col = st.columns(2)
                ad = r_col.number_input("Gross ADR", 0.0, 5000.0, float(ad_d), key=kp+"a")
                fl = h_col.number_input("Market Floor", 0.0, 2000.0, float(fl_d), key=kp+"fl")
            
            ev_r = st.number_input("Event Rev/Pax", 0.0, key=kp+"ev") if is_group else 0.0
        
        res = run_calculation([sgl, dbl, tpl], ad, nt, q, cp, fl, ev_r)
        with c3:
            st.caption("Wealth Result")
            if res:
                st.metric("Wealth / Room", f"{cu} {res['u']:,.2f}")
                st.markdown(f"<h3 style='color:{res['c']}; text-align:center;'>{res['s']}</h3>", unsafe_allow_html=True)
                if res['risk']: st.markdown(f"<div class='dominance-warn'>⚠️ DOMINANCE RISK: {res['impact']:.1f}%</div>", unsafe_allow_html=True)
                st.write(f"Total Wealth: **{res['tp']:,.0f}**")
            else: st.info("Input Inventory")

    st.header(f"🧳 Portfolio Audit: {h_nm}")
    seg("OTA Segment", "#2ecc71", "#e8f5e9", "ot", 60, 35, op_comm)
    st.divider()
    seg("Direct / FIT", "#2980b9", "#ebf5fb", "di", 65, 40, 0.0)
    st.divider()
    seg("Wholesale", "#e67e22", "#fff3e0", "wh", 45, 25, 0.2)
    st.divider()
    seg("MICE & Groups", "#2c3e50", "#eceff1", "gc", 55, 30, 0.0, is_group=True)

    if st.button("🔒 Log Out"):
        st.session_state["auth"] = False
        st.rerun()
