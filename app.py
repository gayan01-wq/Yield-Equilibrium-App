import streamlit as st
import pandas as pd

# --- 1. CONFIG & THEME ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .main-title {
        font-size: 3rem !important;
        font-weight: 800;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 30px;
        text-transform: uppercase;
        letter-spacing: 2px;
        border-bottom: 5px solid #3498db;
        padding-bottom: 10px;
    }
    [data-testid="stMetricValue"] { font-size: 1.8rem !important; }
    .stMetric {background:#fff; border:1px solid #eee; padding:15px; border-radius:12px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);}
    .card {padding:12px; border-radius:10px; margin-bottom:10px; border-left:12px solid; font-weight:bold; color: #2c3e50;}
    .dominance-warn {color: #d35400; font-weight: bold; border: 2px solid #d35400; padding: 8px; border-radius: 5px; text-align: center; background: #fff5f0;}
    .pillar-box {background:#f8f9fa; padding:15px; border-radius:10px; border-top:4px solid #2c3e50; min-height: 180px; margin-bottom: 20px;}
    .stNumberInput input { font-size: 1.1rem !important; font-weight: bold !important; color: #2c3e50 !important; }
    .copyright-text {font-size: 0.75rem; color: #95a5a6; text-align: center; margin-top: 50px;}
    </style>
""", unsafe_allow_html=True)

# --- 2. PASSWORD PROTECTION ---
def check_password():
    if "auth" not in st.session_state:
        st.session_state["auth"] = False
    if not st.session_state["auth"]:
        st.markdown("<h1 class='main-title'>Yield Equilibrium</h1>", unsafe_allow_html=True)
        pwd = st.text_input("Access Key", type="password")
        if st.button("Unlock") or (pwd == "Gayan2026"): 
            if pwd == "Gayan2026":
                st.session_state["auth"] = True
                st.rerun()
            elif pwd != "": st.error("Invalid Key")
        return False
    return True

if check_password():
    # --- 3. SIDEBAR CONTROLS ---
    with st.sidebar:
        st.title("👨‍💼 Architect")
        st.subheader("Gayan Nugawela")
        st.caption("Revenue management specialist- SME")
        st.divider()
        
        st.header("⚙️ Global Architecture")
        h_nm = st.text_input("Hotel Name", "Wyndham Garden Salalah")
        h_cp = st.number_input("Total Inventory", 1, 1000, 158)
        
        currencies = [
            "OMR", "AED", "SAR", "QAR", "BHD", "KWD", "JOD", "EGP", "ILS",
            "EUR", "GBP", "CHF", "SEK", "NOK", "DKK", "PLN", "TRY",
            "USD", "LKR", "INR", "PKR", "BDT", "JPY", "CNY", "SGD", "HKD",
            "THB", "MYR", "IDR", "KRW", "VND", "PHP"
        ]
        cu = st.selectbox("Currency", sorted(currencies))
        
        st.divider()
        st.header("📊 Statutory & Costs")
        c_side1, c_side2 = st.columns([1, 1.2]) 
        p01 = c_side1.number_input("P01 Fee", 0., 100., 6.90)
        tx = c_side2.number_input("Tax Div", 1.0000, 2.5000, 1.2327, format="%.4f", step=0.0001)
        op_comm = st.slider("OTA Comm %", 0, 50, 18) / 100
        
        st.divider()
        st.header("🍽️ Meal Cost Allocation")
        mc_bb = st.number_input("BB Cost", 0.0, 500.0, 2.0)
        mc_hb = st.number_input("HB Cost", 0.0, 500.0, 8.0)
        mc_fb = st.number_input("FB Cost", 0.0, 500.0, 14.0)
        mc_sai = st.number_input("SAI Cost", 0.0, 500.0, 22.0)
        mc_ai = st.number_input("AI Cost", 0.0, 500.0, 27.0)
        
        m_map = {"RO": 0.0, "BB": mc_bb, "HB": mc_hb, "FB": mc_fb, "SAI": mc_sai, "AI": mc_ai}

        # --- COPYRIGHT SECTION ---
        st.divider()
        st.markdown("""
            <div class='copyright-text'>
                © 2026 Gayan Nugawela<br>
                <b>Yield Equilibrium™ Framework</b><br>
                All Rights Reserved.
            </div>
        """, unsafe_allow_html=True)

    # --- 4. CALCULATION ENGINE ---
    def run_calculation(rms, adr, nts, mix, cp, fl, ev_rev=0):
        t_rms = sum(rms)
        if t_rms <= 0: return {"u": 0, "tp": 0, "s": "N/A", "c": "#ccc", "impact": 0, "risk": False}
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
            st.caption("Meal Plan Allocation")
            ma, mb, mc = st.columns(3)
            q = {"RO": ma.number_input("RO", 0, key=kp+"ro"), "BB": ma.number_input("BB", 0, key=kp+"b"),
                 "HB": mb.number_input("HB", 0, key=kp+"h"), "FB": mb.number_input("FB", 0, key=kp+"f"),
                 "SAI": mc.number_input("SAI", 0, key=kp+"sa"), "AI": mc.number_input("AI", 0, key=kp+"ai")}
            with st.container(border=True):
                st.caption("PRICING FRAME")
                r_col, h_col = st.columns(2)
                ad = r_col.number_input("Gross ADR", 0.0, 5000.0, float(ad_d), key=kp+"a")
                fl = h_col.number_input("Market Floor", 0.0, 2000.0, float(fl_d), key=kp+"fl")
            ev_r = st.number_input("Event Rev/Pax", 0.0, key=kp+"ev") if is_group else 0.0
        
        res = run_calculation([sgl, dbl, tpl], ad, nt, q, cp, fl, ev_r)
        with c3:
            st.caption("Wealth Result")
            if (sgl + dbl + tpl) > 0:
                st.metric("Wealth / Room", f"{cu} {res['u']:,.2f}")
                st.markdown(f"<h3 style='color:{res['c']}; text-align:center;'>{res['s']}</h3>", unsafe_allow_html=True)
                if res['risk']: st.markdown(f"<div class='dominance-warn'>⚠️ DOMINANCE RISK: {res['impact']:.1f}%</div>", unsafe_allow_html=True)
                st.divider()
                st.write(f"Total Wealth: **{res['tp']:,.0f}**")
            else: st.info("Input Inventory")
        return res

    # --- 5. DASHBOARD TOP ---
    st.markdown("<h1 class='main-title'>Yield Equilibrium</h1>", unsafe_allow_html=True)
    st.header(f"🧳 Portfolio Audit: {h_nm}")
    r1 = seg("OTA Segment", "#2ecc71", "#e8f5e9", "ot", 60, 35, op_comm)
    st.divider()
    r2 = seg("Direct / FIT", "#2980b9", "#ebf5fb", "di", 65, 40, 0.0)
    st.divider()
    r3 = seg("Wholesale", "#e67e22", "#fff3e0", "wh", 45, 25, 0.2)
    st.divider()
    r4 = seg("MICE & Groups", "#2c3e50", "#eceff1", "gc", 55, 30, 0.0, is_group=True)

    # --- 6. PORTFOLIO WEALTH ---
    st.divider()
    total_w = sum(r['tp'] for r in [r1, r2, r3, r4] if r)
    st.metric(f"Total Portfolio Wealth ({cu})", f"{total_w:,.0f}")

    # --- 7. THE 03 PILLARS ---
    st.divider()
    st.subheader("🏛️ The 03 Pillars of Yield Equilibrium")
    p1, p2, p3 = st.columns(3)
    p1.markdown("<div class='pillar-box'><h4>1. Cold Wealth Stripping</h4><p>Isolating net liquidity by removing taxes, commissions, and variable room costs. This is the only revenue that truly lands in the bank.</p></div>", unsafe_allow_html=True)
    p2.markdown("<div class='pillar-box'><h4>2. Friction Indexing</h4><p>Measuring the % of revenue lost to overhead (Meals, Fees, Trans). Lower friction identifies high-quality segments.</p></div>", unsafe_allow_html=True)
    p3.markdown("<div class='pillar-box'><h4>3. Displacement Hurdle</h4><p>Calculating Market Hurdle against Net Wealth to ensure high-volume groups do not displace high-yield individual travelers.</p></div>", unsafe_allow_html=True)

    if st.button("🔒 Securely Log Out"):
        st.session_state["auth"] = False
        st.rerun()
