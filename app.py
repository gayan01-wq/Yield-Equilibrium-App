import streamlit as st
import pandas as pd

# --- ACCESS CONTROL ---
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
    # --- EXECUTIVE STYLING ---
    st.set_page_config(layout="wide", page_title="Yield Equilibrium SME")
    
    st.markdown("""
        <style>
        .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
        [data-testid="stSidebar"] { background-color: #0e1117 !important; color: white; }
        .stMetric { background: rgba(255, 255, 255, 0.8); backdrop-filter: blur(10px); border-radius: 15px; padding: 15px; }
        .card { padding: 12px; border-radius: 12px; margin-bottom: 10px; border-left: 10px solid; font-weight: bold; background: rgba(255, 255, 255, 0.6); }
        h1, h2, h3 { color: #1e3a8a; }
        </style>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown("<h2 style='color:white;'>👨‍💼 Architect</h2>", unsafe_allow_html=True)
        st.markdown("<h3 style='color:#60a5fa; margin-bottom:0;'>Gayan Nugawela</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color:white; font-size:14px;'>MBA | CRME | CHRM | RevOps</p>", unsafe_allow_html=True)
        st.caption("Revenue Management Expert & SME")
        st.divider()
        
        st.title("⚙️ Global Settings")
        h_nm = st.text_input("Hotel Entity", "Global Portfolio Audit")
        h_cp = st.number_input("Total Inventory", 1, 1000, 158)
        
        st.markdown("### 🍽️ Meals (Net)")
        b = st.number_input("BB", 0.0, 500.0, 2.0)
        l = st.number_input("LN", 0.0, 500.0, 6.0)
        d = st.number_input("DN", 0.0, 500.0, 6.0)
        s = st.number_input("SAI", 0.0, 500.0, 8.0)
        a = st.number_input("AI", 0.0, 500.0, 15.0)
        m = {"RO":0, "BB":b, "HB":b+d, "FB":b+l+d, "SAI":b+l+d+s, "AI":b+l+d+s+a}
        
        p01 = st.number_input("P01 Fee", 0.0, 100.0, 6.9)
        tx = st.number_input("Tax Divisor", 1.0, 2.0, 1.2327, format="%.4f")
        op = st.slider("OTA Commission %", 0, 50, 18) / 100
        cu = st.selectbox("Currency", ["OMR", "AED", "SAR", "THB", "EUR", "GBP", "USD"])

    st.title("🏨 Yield Equilibrium Center")
    st.markdown("---")

    def run(rms, adr, nts, mix, cp, fl, ev_r=0, tr_c=0):
        t_rms = sum(rms)
        if t_rms <= 0:
            return None
        pax = (rms[0]*1 + rms[1]*2 + rms[2]*3)
        gross = (adr * t_rms * nts) + (ev_r * pax * nts)
        nt_rev = (adr * t_rms) / tx
        fb_c = sum(q * m[p] * (pax / t_rms) for p, q in mix.items())
        ev_w = (ev_r * pax) / tx
        cm = (nt_rev - fb_c) * cp
        dp = ((nt_rev - fb_c - cm) - (p01 * t_rms)) + (ev_w / t_rms)
        tp = (dp * t_rms * nts) - (tr_c / tx)
        u = tp / (t_rms * nts)
        af = fl * 0.75 if nts > 7 else fl
        fric = (1 - (tp / gross)) * 100 if gross > 0 else 0
        
        if fric < 26: 
            f_lb = "Net Contribution"
        elif 26 <= fric < 38: 
            f_lb = "Yield Dilution"
        else: 
            f_lb = "Revenue Erosion"
        
        if u < af: 
            lb, cl = "DILUTIVE", "#e74c3c"
        elif af <= u < (af + 5): 
            lb, cl = "MARGINAL", "#f1c40f"
        else: 
            lb, cl = "OPTIMIZED", "#27ae60"
        
        return {"u": u, "s": lb, "c": cl, "tp": tp, "pax": pax, "fric": fric, "f_lb": f_lb}

    def seg(nm, cl, kp, ad_d, fl_d, cp, is_grp=False):
        st.markdown(f"<div class='card' style='border-left-color:{cl}'>{nm}</div>", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns([1, 2.8, 1, 1.2])
        ev_r, tr_c = 0.0, 0.0
        with c1:
            sgl = st.number_input("SGL", 0, key=kp+"s")
            dbl = st.number_input("DBL", 0, key=kp+"d")
            tpl = st.number_input("TPL", 0, key=kp+"t")
            nt = st.number_input("Nights", 1, 365, key=kp+"n")
        with c2:
            st.write("Meal Basis")
            ca, cb, cc = st.columns(3)
            q = {
                "RO": ca.number_input("RO", 0, key=kp+"ro"),
                "BB": ca.number_input("BB", 0, key=kp+"b"),
                "HB": cb.number_input("HB", 0, key=kp+"h"),
                "FB": cb.number_input("FB", 0, key=kp+"f"),
                "SAI": cc.number_input("SAI", 0, key=kp+"sa"),
                "AI": cc.number_input("AI", 0, key=kp+"ai")
            }
            if is_grp:
                cx, cy = st.columns(2)
                ev_r = cx.number_input("Event/Pax", 0.0, key=kp+"ev")
                tr_c = cy.number_input("Trans Cost", 0.0, key=kp+"tr")
        with c3:
            ad = st.number_input("Rate", 0., 5000., float(ad_d), key=kp+"a")
            fl = st.number_input("Market Hurdle", 0., 2000., float(fl_d), key=kp+"fl")
        res = run([sgl, dbl, tpl], ad, nt, q, cp, fl, ev_r, tr_c)
        if res:
            with c4:
                st.metric("Wealth (Room)", f"{cu} {res['u']:.2f}")
                st.markdown(f"<b style='color:{res['c']}'>{res['s']}</b>", unsafe_allow_html=True)
                st.write(f"{res['f_lb']}: **{res['fric']:.1f}%**")
                st.caption("(Tax+Comm+Meals+Fees)")
                st.write(f"Total Wealth: **{res['tp']:,.0f}**")
        return res

    # Segments
    r1 = seg("OTA Channels", "#2ecc71", "ot", 60.0, 35.0, op)
    r2 = seg("Direct / FIT", "#2980b9", "di", 65.0, 40.0, 0.0)
    r3 = seg("Wholesale / B2B", "#e67e22", "wh", 45.0, 25.0, 0.2)
    r4 = seg("Corporate Contracts", "#8e44ad", "co", 58.0, 32.0, 0.0)
    r5 = seg("Leisure Groups", "#d35400", "gt", 40.0, 20.0, 0.15, is_grp=True)
    r6 = seg("MICE / Events", "#2c3e50", "gc", 55.0, 30.0, 0.0, is_grp=True)
    
    st.divider()
    all_res = {"OTA": r1, "Direct": r2, "Wholesale": r3, "Corporate": r4, "Groups": r5, "MICE": r6}
    active_res = {k: v for k, v in all_res.items() if v}

    if active_res:
        total_wealth = sum(v['tp'] for v in active_res.values())
        st.metric(f"🏢 Total Portfolio Wealth ({cu})", f"{total_wealth:,.2f}")
        st.markdown("### 📊 Yield Equilibrium Breakdown")
        col_c, col_t = st.columns([2, 1.2])
        with col_c:
            df = pd.DataFrame({"Segment": list(active_res.keys()), "Wealth": [v['tp'] for v in active_res.values()]})
            st.bar_chart(df.set_index("Segment"))
        with col_t:
            st.markdown("#### 🔍 SME Insights")
            st.info(f"Tax: {tx} | P01: {p01} | Integrated Yield Applied.")

    if st.button("🔒 Log Out"):
        st.session_state["auth"] = False
        st.rerun()
