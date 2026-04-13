import streamlit as st
import pandas as pd

# --- CONFIG & THEME ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium", initial_sidebar_state="expanded")

# Custom CSS for UI Stability
st.markdown("""
    <style>
    .stMetric {background:#fff; border:1px solid #eee; padding:15px; border-radius:12px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);}
    .card {padding:10px; border-radius:8px; margin-bottom:8px; border-left:10px solid; font-weight:bold; font-size: 1.1em;}
    .pillar-box {background:#f8f9fa; padding:15px; border-radius:10px; border-top:4px solid #2c3e50; min-height: 200px;}
    .density-warn {color: #e67e22; font-weight: bold; border: 1px solid #e67e22; padding: 5px; border-radius: 5px; display: block; margin-top: 5px;}
    .wealth-box {background: #fcfcfc; border: 1px solid #ddd; padding: 10px; border-radius: 8px; margin-top: 10px;}
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
        
        st.title("⚙️ Global Settings")
        h_nm = st.text_input("Hotel", "Wyndham Garden Salalah")
        h_cp = st.number_input("Total Inventory", 1, 1000, 158)
        
        st.header("🍽️ Meals (Net)")
        b = st.number_input("BB", 0., 500., 2.0)
        l = st.number_input("LN", 0., 500., 6.0)
        d_cost = st.number_input("DN", 0., 500., 6.0)
        s_cost = st.number_input("SAI", 0., 500., 8.0)
        a_cost = st.number_input("AI", 0., 500., 15.0)
        
        m = {
            "RO": 0.0, "BB": b, "HB": b + d_cost, 
            "FB": b + l + d_cost, "SAI": b + l + d_cost + s_cost, 
            "AI": b + l + d_cost + s_cost + a_cost
        }
        
        p01 = st.number_input("P01 Fee", 0., 100., 6.9)
        tx = st.number_input("Tax Div", 1.0, 2.5, 1.2327, format="%.4f")
        op = st.slider("OTA Comm %", 0, 50, 18) / 100
        cu = st.selectbox("Currency", ["OMR", "AED", "SAR", "USD", "LKR", "GBP", "EUR"])
        
        st.divider()
        st.subheader("📈 Yield Multipliers")
        risk_premium = 0.15 # 15% displacement risk

    # --- CORE ENGINE WITH DENSITY LOGIC ---
    def run(rms, adr, nts, mix, cp, fl, ev_rev=0, total_tr_cost=0):
        t_rms = sum(rms)
        if t_rms <= 0: return None
        
        pax = (rms[0]*1 + rms[1]*2 + rms[2]*3)
        inv_impact = (t_rms / h_cp) * 100
        
        # 20% DENSITY LOGIC
        effective_hurdle = fl
        density_alert = False
        if inv_impact >= 20.0:
            effective_hurdle = fl * (1 + risk_premium)
            density_alert = True
            
        # LOS VELOCITY
        if nts > 7:
            effective_hurdle = effective_hurdle * 0.85

        gross_total = (adr * t_rms * nts) + (ev_rev * pax * nts)
        nt_rev = (adr * t_rms) / tx
        fb_cost = sum(q * m[p] * (pax / t_rms) for p, q in mix.items())
        ev_w = (ev_rev * pax) / tx
        cm = (nt_rev - fb_cost) * cp
        dp = ((nt_rev - fb_cost - cm) - (p01 * t_rms)) + (ev_w / t_rms)
        tp = (dp * t_rms * nts) - (total_tr_cost / tx)
        u = tp / (t_rms * nts)
        
        fric = (1 - (tp / gross_total)) * 100 if gross_total > 0 else 0
        
        if u < effective_hurdle: lb, cl = "DILUTIVE", "#e74c3c"
        elif effective_hurdle <= u < (effective_hurdle + 5): lb, cl = "MARGINAL", "#f1c40f"
        else: lb, cl = "OPTIMIZED", "#27ae60"
        
        return {"u": u, "s": lb, "c": cl, "tp": tp, "pax": pax, "fric": fric, "impact": inv_impact, "risk": density_alert, "h_eff": effective_hurdle}

    def seg(nm, cl, bg, kp, ad_d, fl_d, cp, is_group=False):
        st.markdown(f"<div class='card' style='background:{bg};border-left-color:{cl}'>{nm}</div>", unsafe_allow_html=True)
        # Ratio adjusted to [1.2, 2.5, 1.3] to prevent column squashing
        c1, c2, c3 = st.columns([1.2, 2.5, 1.3])
        ev_r, tr_c = 0.0, 0.0
        
        with c1:
            sgl = st.number_input("SGL", 0, key=kp+"s")
            dbl = st.number_input("DBL", 0, key=kp+"d")
            tpl = st.number_input("TPL", 0, key=kp+"t")
            nt = st.number_input("Nights", 1, 365, key=kp+"n")
        with c2:
            st.write("Meal Plan")
            ca, cb, cc = st.columns(3)
            q = {"RO": ca.number_input("RO", 0, key=kp+"ro"), "BB": ca.number_input("BB", 0, key=kp+"b"),
                 "HB": cb.number_input("HB", 0, key=kp+"h"), "FB": cb.number_input("FB", 0, key=kp+"f"),
                 "SAI": cc.number_input("SAI", 0, key=kp+"sa"), "AI": cc.number_input("AI", 0, key=kp+"ai")}
            
            rate_col, hurdle_col = st.columns(2)
            ad = rate_col.number_input("Rate", 0., 5000., float(ad_d), key=kp+"a")
            fl = hurdle_col.number_input("Hurdle", 0., 2000., float(fl_d), key=kp+"fl")
            
            if is_group:
                cx, cy = st.columns(2)
                ev_r = cx.number_input("Event/Pax", 0.0, key=kp+"ev")
                tr_c = cy.number_input("Trans Cost", 0.0, key=kp+"tr")
        
        res = run([sgl, dbl, tpl], ad, nt, q, cp, fl, ev_r, tr_c)
        
        with c3:
            if res:
                st.metric("Wealth/Room", f"{cu} {res['u']:.2f}")
                st.markdown(f"<h3 style='color:{res['c']}; margin:0;'>{res['s']}</h3>", unsafe_allow_html=True)
                if res['risk']: st.markdown("<span class='density-warn'>⚠️ HIGH DENSITY RISK</span>", unsafe_allow_html=True)
                st.write(f"Impact: **{res['impact']:.1f}%**")
                st.write(f"Total Wealth: **{res['tp']:,.0f}**")
            else:
                st.info("Input Required")
        return res

    st.header(f"🧳 Strategic Audit: {h_nm}")
    r1 = seg("OTA Segment", "#2ecc71", "#e8f5e9", "ot", 60, 35, op)
    st.divider()
    r2 = seg("Direct/FIT", "#2980b9", "#e3f2fd", "di", 65, 40, 0.0)
    st.divider()
    r3 = seg("Wholesale", "#e67e22", "#fff3e0", "wh", 45, 25, 0.2)
    st.divider()
    r4 = seg("Corporate", "#8e44ad", "#f3e5f5", "co", 58, 32, 0.0)
    st.divider()
    r5 = seg("Group T&T", "#d35400", "#fbe9e7", "gt", 40, 20, 0.15, is_group=True)
    st.divider()
    r6 = seg("Group Corporate (MICE)", "#2c3e50", "#eceff1", "gc", 55, 30, 0.0, is_group=True)
    
    # Portfolio Summary
    st.divider()
    all_res = {"OTA": r1, "Direct": r2, "Wholesale": r3, "Corporate": r4, "Group": r5, "MICE": r6}
    active_res = {k: v for k, v in all_res.items() if v}

    if active_res:
        t_wealth = sum(v['tp'] for v in active_res.values())
        st.metric(f"Total Portfolio Net Wealth ({cu})", f"{t_wealth:,.2f}")
        chart_data = pd.DataFrame({"Segment": active_res.keys(), "Wealth": [v['tp'] for v in active_res.values()]})
        st.bar_chart(chart_data.set_index("Segment"))

    if st.button("🔒 Log Out"):
        st.session_state["auth"] = False
        st.rerun()
