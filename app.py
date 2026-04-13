import streamlit as st
import pandas as pd

# --- CONFIG & THEME ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .stMetric {background:#fff; border:1px solid #eee; padding:15px; border-radius:12px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);}
    .card {padding:12px; border-radius:10px; margin-bottom:10px; border-left:12px solid; font-weight:bold; font-size: 1.1em; color: #2c3e50;}
    .density-warn {color: #e67e22; font-weight: bold; border: 1px solid #e67e22; padding: 5px; border-radius: 5px; display: block; margin-top: 5px; text-align: center;}
    .section-head {color: #34495e; font-size: 0.9em; font-weight: bold; text-transform: uppercase; margin-bottom: 8px; border-bottom: 1px solid #eee;}
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
        
        st.header("⚙️ Global Architecture")
        h_nm = st.text_input("Hotel Name", "Wyndham Garden Salalah")
        h_cp = st.number_input("Total Inventory", 1, 1000, 158)
        cu = st.selectbox("Currency", ["OMR", "AED", "SAR", "USD", "LKR", "GBP", "EUR"])
        
        st.divider()
        st.header("📊 Statutory & Fixed Costs")
        # Grouped P01 and Tax Divisor together as requested
        c_side1, c_side2 = st.columns(2)
        p01 = c_side1.number_input("P01 Fee", 0., 100., 6.9)
        tx = c_side2.number_input("Tax Div", 1.0, 2.5, 1.2327, format="%.4f")
        op = st.slider("OTA Comm %", 0, 50, 18) / 100
        
        st.divider()
        st.header("🍽️ Meal Costs (Net)")
        b = st.number_input("BB Cost", 0., 500., 2.0)
        l = st.number_input("LN Cost", 0., 500., 6.0)
        d_cost = st.number_input("DN Cost", 0., 500., 6.0)
        s_cost = st.number_input("SAI Supplement", 0., 500., 8.0)
        a_cost = st.number_input("AI Supplement", 0., 500., 15.0)
        
        m_map = {
            "RO": 0.0, "BB": b, "HB": b + d_cost, 
            "FB": b + l + d_cost, "SAI": b + l + d_cost + s_cost, 
            "AI": b + l + d_cost + s_cost + a_cost
        }
        
        st.divider()
        risk_premium = 0.15 

    # --- CORE ENGINE ---
    def run_calculation(rms, adr, nts, mix, cp, fl, ev_rev=0, total_tr_cost=0):
        t_rms = sum(rms)
        if t_rms <= 0: return None
        
        pax = (rms[0]*1 + rms[1]*2 + rms[2]*3)
        inv_impact = (t_rms / h_cp) * 100
        
        # 20% Density Rule & LOS Logic
        effective_hurdle = fl
        density_alert = False
        if inv_impact >= 20.0:
            effective_hurdle = fl * (1 + risk_premium)
            density_alert = True
        if nts > 7:
            effective_hurdle = effective_hurdle * 0.85

        gross_total = (adr * t_rms * nts) + (ev_rev * pax * nts)
        nt_rev = (adr * t_rms) / tx
        fb_cost = sum(q * m_map[p] * (pax / t_rms) for p, q in mix.items())
        ev_w = (ev_rev * pax) / tx
        cm = (nt_rev - fb_cost) * cp
        dp = ((nt_rev - fb_cost - cm) - (p01 * t_rms)) + (ev_w / t_rms)
        tp = (dp * t_rms * nts) - (total_tr_cost / tx)
        u = tp / (t_rms * nts)
        
        if u < effective_hurdle: lb, cl = "DILUTIVE", "#e74c3c"
        elif effective_hurdle <= u < (effective_hurdle + 5): lb, cl = "MARGINAL", "#f1c40f"
        else: lb, cl = "OPTIMIZED", "#27ae60"
        
        return {"u": u, "s": lb, "c": cl, "tp": tp, "impact": inv_impact, "risk": density_alert}

    def seg(nm, cl, bg, kp, ad_d, fl_d, cp, is_group=False):
        st.markdown(f"<div class='card' style='background:{bg};border-left-color:{cl}'>{nm}</div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1.3, 2.4, 1.3])
        
        with c1:
            st.markdown("<div class='section-head'>Stay Details</div>", unsafe_allow_html=True)
            sgl = st.number_input("SGL Rooms", 0, key=kp+"s")
            dbl = st.number_input("DBL Rooms", 0, key=kp+"d")
            tpl = st.number_input("TPL Rooms", 0, key=kp+"t")
            nt = st.number_input("Total Nights", 1, 365, key=kp+"n")
            
        with c2:
            st.markdown("<div class='section-head'>Meal Plan Distribution</div>", unsafe_allow_html=True)
            ca, cb, cc = st.columns(3)
            q = {"RO": ca.number_input("RO", 0, key=kp+"ro"), "BB": ca.number_input("BB", 0, key=kp+"b"),
                 "HB": cb.number_input("HB", 0, key=kp+"h"), "FB": cb.number_input("FB", 0, key=kp+"f"),
                 "SAI": cc.number_input("SAI", 0, key=kp+"sa"), "AI": cc.number_input("AI", 0, key=kp+"ai")}
            
            # Rate and Hurdle Box Aligned Separately & Nicely
            st.markdown("<div class='section-head'>Pricing Strategy</div>", unsafe_allow_html=True)
            r_col, h_col = st.columns(2)
            ad = r_col.number_input("Gross ADR", 0., 5000., float(ad_d), key=kp+"a")
            fl = h_col.number_input("Market Hurdle", 0., 2000., float(fl_d), key=kp+"fl")
            
            ev_r, tr_c = 0.0, 0.0
            if is_group:
                st.markdown("<div class='section-head'>Ancillary & Logistics</div>", unsafe_allow_html=True)
                gx, gy = st.columns(2)
                ev_r = gx.number_input("Event Rev/Pax", 0.0, key=kp+"ev")
                tr_c = gy.number_input("Trans. Cost", 0.0, key=kp+"tr")
        
        res = run_calculation([sgl, dbl, tpl], ad, nt, q, cp, fl, ev_r, tr_c)
        
        with c3:
            st.markdown("<div class='section-head'>Wealth Window</div>", unsafe_allow_html=True)
            if res:
                st.metric("Wealth Per Room", f"{cu} {res['u']:.2f}")
                st.markdown(f"<h3 style='color:{res['c']}; margin:0; text-align:center;'>{res['s']}</h3>", unsafe_allow_html=True)
                if res['risk']: st.markdown("<span class='density-warn'>⚠️ DENSITY DISPLACEMENT</span>", unsafe_allow_html=True)
                st.divider()
                st.write(f"Net Stay Wealth: **{res['tp']:,.0f}**")
                st.write(f"Inv. Impact: **{res['impact']:.1f}%**")
            else:
                st.info("Awaiting Input")
        return res

    st.header(f"🧳 Strategic Audit: {h_nm}")
    r1 = seg("OTA Segment", "#2ecc71", "#e8f5e9", "ot", 60, 35, op)
    st.divider()
    r2 = seg("Direct / FIT", "#2980b9", "#e3f2fd", "di", 65, 40, 0.0)
    st.divider()
    r3 = seg("Wholesale", "#e67e22", "#fff3e0", "wh", 45, 25, 0.2)
    st.divider()
    r4 = seg("MICE & Groups", "#2c3e50", "#eceff1", "gc", 55, 30, 0.0, is_group=True)
    
    if st.button("🔒 Log Out"):
        st.session_state["auth"] = False
        st.rerun()
