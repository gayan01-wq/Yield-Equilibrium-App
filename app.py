import streamlit as st
import pandas as pd

# --- 1. CONFIG & THEME ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .main-title { font-size: 3rem !important; font-weight: 800; color: #2c3e50; text-align: center; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 2px; border-bottom: 5px solid #3498db; padding-bottom: 5px; }
    .framework-subtitle { text-align: center; color: #7f8c8d; font-style: italic; font-size: 1.1rem; margin-bottom: 30px; }
    [data-testid="stMetricValue"] { font-size: 1.8rem !important; }
    .stMetric {background:#fff; border:1px solid #eee; padding:15px; border-radius:12px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);}
    .card {padding:12px; border-radius:10px; margin-bottom:10px; border-left:12px solid; font-weight:bold; color: #2c3e50;}
    .dominance-warn {color: #d35400; font-weight: bold; border: 2px solid #d35400; padding: 8px; border-radius: 5px; text-align: center; background: #fff5f0;}
    .pillar-box {background:#f8f9fa; padding:15px; border-radius:10px; border-top:4px solid #2c3e50; min-height: 180px; margin-bottom: 20px;}
    .coach-note {padding: 12px; border-radius: 8px; font-size: 0.95rem; margin-top: 10px; border: 2px solid #eee; background-color: #fdfefe; line-height: 1.4;}
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
    with st.sidebar:
        st.title("👨‍💼 Architect")
        st.subheader("Gayan Nugawela")
        st.caption("Revenue management specialist- SME")
        st.divider()
        st.header("⚙️ Global Architecture")
        h_nm = st.text_input("Hotel Name", "Wyndham Garden Salalah")
        h_cp = st.number_input("Total Inventory", 1, 1000, 158)
        
        # Comprehensive Currency List
        currencies = [
            "OMR", "AED", "SAR", "QAR", "BHD", "KWD", "JOD", "EGP", "ILS",
            "EUR", "GBP", "CHF", "USD", "LKR", "INR", "JPY", "CNY", "SGD", "THB"
        ]
        cu = st.selectbox("Currency", sorted(currencies))
        
        st.divider()
        st.header("📊 Statutory & Costs")
        c_side1, c_side2 = st.columns([1, 1.3]) 
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

        st.divider()
        st.markdown("<div class='copyright-text'>© 2026 Gayan Nugawela<br><b>Yield Equilibrium™ Framework</b><br>All Rights Reserved.</div>", unsafe_allow_html=True)

    # --- 3. DYNAMIC STRATEGIC COACHING ---
    def get_coach_note(status, tp, total_gross, room_count):
        efficiency = (tp / total_gross * 100) if total_gross > 0 else 0
        
        if status == "DILUTIVE":
            color = "#e74c3c"
            title = "🚩 UNPROFITABLE / HIGH FRICTION"
            if room_count <= 2:
                msg = f"At low volume, fixed fees consume the margin ({efficiency:.1f}% efficiency). This specific booking is a loss. Only accept if part of a larger direct strategy."
            else:
                msg = f"Fundamental pricing failure. Even with volume, the efficiency is only {efficiency:.1f}%. You are trading rooms for nearly zero wealth return."
        
        elif status == "MARGINAL":
            color = "#f1c40f"
            title = "⚠️ VOLUME DEPENDENT / FILLER"
            msg = f"Wealth efficiency is {efficiency:.1f}%. While total wealth grows with more rooms, this is essentially 'Occupancy Filler'. Displace only with higher FIT demand."
            
        else: # OPTIMIZED
            color = "#27ae60"
            title = "💎 OPTIMIZED WEALTH GENERATOR"
            msg = f"Strong core pricing with {efficiency:.1f}% efficiency. This segment builds genuine hotel wealth and should be prioritized in the mix."
            
        return f"<div style='border-left: 5px solid {color}; padding-left: 10px;'><b>{title}</b><br>{msg}</div>"

    # --- 4. ENGINE ---
    def run_calculation(rms, adr, nts, mix, cp, fl, ev_rev=0):
        t_rms = sum(rms)
        if t_rms <= 0: return None
        pax = (rms[0]*1 + rms[1]*2 + rms[2]*3)
        inv_impact = (t_rms / h_cp) * 100
        eff_h = fl * 1.25 if inv_impact >= 50.0 else fl
        if nts >= 5: eff_h *= 0.90
        
        gross_rev = adr * t_rms * nts
        nt_rev = (adr * t_rms) / tx
        fb_cost = sum(q * m_map[p] * (pax / t_rms) for p, q in mix.items())
        
        # Wealth Stripping Math
        dp = ((nt_rev - fb_cost - ((nt_rev-fb_cost)*cp)) - (p01 * t_rms)) + ((ev_rev * pax) / tx / t_rms)
        tp = (dp * t_rms * nts)
        u = tp / (t_rms * nts)
        
        if u < (eff_h * 0.8) or tp <= 0: lb, cl = "DILUTIVE", "#e74c3c"
        elif u < eff_h: lb, cl = "MARGINAL", "#f1c40f"
        else: lb, cl = "OPTIMIZED", "#27ae60"
        
        return {"u": u, "s": lb, "c": cl, "tp": tp, "impact": inv_impact, "risk": inv_impact >= 50.0, "gross": gross_rev, "t_rms": t_rms}

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
        
        res = run_calculation([sgl, dbl, tpl], ad, nt, q,
