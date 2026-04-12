import streamlit as st
import pandas as pd

# --- PASSWORD PROTECTION ---
def check_password():
    if "auth" not in st.session_state:
        st.session_state["auth"] = False
    if not st.session_state["auth"]:
        st.title("🏨 Yield Equilibrium Center")
        pwd = st.text_input("Access Key", type="password")
        if st.button("Unlock") or (pwd == "Gayan2026"): 
            st.session_state["auth"] = True
            st.rerun()
        return False
    return True

if check_password():
    st.set_page_config(layout="wide", page_title="Yield Equilibrium")
    st.markdown("<style>.stMetric{background:#fff;border:1px solid #eee;padding:10px;border-radius:10px}.card{padding:8px;border-radius:8px;margin-bottom:5px;border-left:8px solid;font-weight:bold}</style>",unsafe_allow_html=True)
    
    with st.sidebar:
        st.title("👨‍💼 Architect")
        st.subheader("Gayan Nugawela")
        st.write("MBA | CRME | CHRM | RevOps")
        st.caption("Revenue Management Expert & SME")
        st.divider()
        
        st.title("⚙️ Global Settings")
        h_nm = st.text_input("Hotel", "Wyndham Garden Salalah")
        h_cp = st.number_input("Total Inventory", 1, 1000, 158)
        st.header("🍽️ Meals (Net)")
        b, l, d = st.number_input("BB", 0., 500., 2.), st.number_input("LN", 0., 500., 6.), st.number_input("DN", 0., 500., 6.)
        s, a = st.number_input("SAI", 0., 500., 8.), st.number_input("AI", 0., 500., 15.)
        m = {"RO":0, "BB":b, "HB":b+d, "FB":b+l+d, "SAI":b+l+d+s, "AI":b+l+d+s+a}
        p01, tx = st.number_input("P01 Fee", 0., 100., 6.9), st.number_input("Tax Div", 1., 2., 1.2327, format="%.4f")
        op = st.slider("OTA Comm %", 0, 50, 18) / 100
        cu = st.selectbox("Currency", ["OMR", "AED", "SAR", "THB", "EUR", "GBP", "USD"])

    st.title("🏨 Yield Equilibrium Center")

    def run(rms, adr, nts, mix, cp, fl, ev_rev=0, total_tr_cost=0):
        t_rms = sum(rms)
        if t_rms <= 0: return None
        pax = (rms[0]*1 + rms[1]*2 + rms[2]*3)
        gross_total = (adr * t_rms * nts) + (ev_rev * pax * nts)
        nt_rev, fb_cost = (adr * t_rms) / tx, sum(q * m[p] * (pax / t_rms) for p, q in mix.items())
        ev_w = (ev_rev * pax) / tx
        cm = (nt_rev - fb_cost) * cp
        dp = ((nt_rev - fb_cost - cm) - (p01 * t_rms)) + (ev_w / t_rms)
        tp = (dp * t_rms * nts) - (total_tr_cost / tx)
        u = tp / (t_rms * nts)
        af = fl * 0.75 if nts > 7 else fl
        fric = (1 - (tp / gross_total)) * 100 if gross_total > 0 else 0
        if fric < 26: fric_lb = "Net Contribution"
        elif 26 <= fric < 38: fric_lb = "Yield Dilution"
        else: fric_lb = "Revenue Erosion"
        if u < af: lb, cl = "DILUTIVE", "#e74c3c"
        elif af <= u < (af + 5): lb, cl = "MARGINAL", "#f1c40f"
        else: lb, cl = "OPTIMIZED", "#27ae60"
        return {"u": u, "s": lb, "c": cl, "tp": tp, "pax": pax, "fric": fric, "fric_lb": fric_lb}

    def seg(nm, cl, bg, kp, ad_d, fl_d, cp, is_group=False):
        st.markdown(f"<div class='card' style='background:{bg};border-left-color:{cl}'>{nm}</div>", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns([1, 2.8, 1, 1.2])
        ev_r, tr_c = 0.0, 0.0
        with c1:
            sgl, dbl, tpl = st.number_input("SGL",0,key=kp+"s"), st.number_input("DBL",0,key=kp+"d"), st.number_input("TPL",0,key=kp+"t")
            nt = st.number_input("Nights", 1, 365, key=kp+"n")
        with c2:
            st.write("Meal Basis")
            ca, cb, cc = st.columns(3)
            q = {"RO": ca.number_input("RO",0,key=kp+"ro"), "BB": ca.number_input("BB",0,key=kp+"b"), "HB": cb.number_input("HB",0,key=kp+"h"), "FB": cb.number_input("FB",0,key=kp+"f"), "SAI": cc.number_input("SAI",0,key=kp+"sa"), "AI": cc.number_input("AI",0,key=kp+"ai")}
            if is_group:
                cx, cy = st.columns(2)
                ev_r = cx.number_input("Event/Pax", 0.0, key=kp+"ev")
                tr_c = cy.number_input("Trans Cost", 0.0, key=kp+"tr")
        with c3:
            ad = st.number_input("Rate", 0., 5000., float(ad_d), key=kp+"a")
            fl = st.number_input("Market Hurdle", 0., 2000., float(fl_d), key=kp+"fl")
        res = run([sgl, dbl, tpl], ad, nt, q, cp, fl, ev_r, tr_c)
        if res:
            with c4:
                st.metric("Wealth (Stay/Room)", f"{cu} {res['u']:.2f}")
                st.markdown(f"<b style='color:{res['c']}'>{res['s']}</b>", unsafe_allow_html=True)
                st.write(f"Pax: **{res['pax']}**")
                st.write(f"{res['fric_lb']}: **{res['fric']:.1f}%**")
                st.caption("(Tax + Comm + Meals + Fees)")
                st.write(f"Stay Wealth (Total): **{res['tp']:,.0f}**")
        return res

    st.header(f"🧳 Strategic Audit: {h_nm}")
    r1 = seg("OTA Segment", "#2ecc71", "#e8f5e9", "ot", 60, 35, op)
    r2 = seg("Direct/FIT", "#2980b9", "#e3f2fd", "di", 65, 40, 0.0)
    r3 = seg("Wholesale", "#e67e22", "#fff3e0", "wh", 45, 25, 0.2)
    r4 = seg("Corporate", "#8e44ad", "#f3e5f5", "co", 58, 32, 0.0)
    r5 = seg("Group Tour & Travels", "#d35400", "#fbe9e7", "gt", 40, 20, 0.15, is_group=True)
    r6 = seg("Group Corporate (MICE)", "#2c3e50", "#eceff1", "gc", 55, 30, 0.0, is_group=True)
    
    st.divider()
    all_res = {"OTA": r1, "Direct": r2, "Wholesale": r3, "Corporate": r4, "Group T&T": r5, "MICE": r6}
    active_res = {k: v for k, v in all_res.items() if v}

    if active_res:
        total_wealth = sum(v['tp'] for v in active_res.values())
        st.metric(f"Total Portfolio Wealth ({cu})", f"{total_wealth:,.2f}")
        
        # --- STRATEGIC ANALYSIS SECTION ---
        st.subheader("📊 Yield Equilibrium Breakdown")
        col_chart, col_text = st.columns([2, 1])
        
        with col_chart:
            chart_data = pd.DataFrame({
                "Segment": active_res.keys(),
                "Wealth Contribution": [v['tp'] for v in active_res.values()]
            })
            st.bar_chart(chart_data.set_index("Segment"))
            st.caption("Wealth Contribution per Segment: A visual representation of Integrated Yield.")

        with col_text:
            st.markdown("### 🔍 The SME Insight")
            st.markdown(f"""
            **Yield Equilibrium Logic:**
            1. **Tax Stripping:** Gross ADR is immediately divided by the **{tx}** Tax Divisor.
            2. **Ancillary Weight:** Event revenue is calculated per pax, acting as a **Yield Multiplier**.
            3. **Variable Drag:** Meal costs and **P01 ({p01})** fees are stripped to find the 'Cold Wealth'.
            4. **Friction Scaling:** Efficiency is labeled based on the % of total deductions.
            5. **Status Hierarchy:** Based on the **Market Hurdle** vs the final Net Room Wealth.
            """)

    if st.button("🔒 Log Out"):
        st.session_state["auth"] = False
        st.rerun()
