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
    
    # Custom CSS for styling
    st.markdown("""
        <style>
        .stMetric {background:#fff; border:1px solid #eee; padding:10px; border-radius:10px}
        .card {padding:8px; border-radius:8px; margin-bottom:5px; border-left:8px solid; font-weight:bold}
        </style>
    """, unsafe_allow_html=True)
    
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
        b = st.number_input("BB", 0., 500., 2.)
        l = st.number_input("LN", 0., 500., 6.)
        d = st.number_input("DN", 0., 500., 6.)
        s = st.number_input("SAI", 0., 500., 8.)
        a = st.number_input("AI", 0., 500., 15.)
        m = {"RO":0, "BB":b, "HB":b+d, "FB":b+l+d, "SAI":b+l+d+s, "AI":b+l+d+s+a}
        
        p01 = st.number_input("P01 Fee", 0., 100., 6.9)
        tx = st.number_input("Tax Div", 1., 2., 1.2327, format="%.4f")
        op = st.slider("OTA Comm %", 0, 50, 18) / 100
        cu = st.selectbox("Currency", ["OMR", "AED", "SAR", "THB", "EUR", "GBP", "USD"])

    # --- HEADER WITH REFRESH BUTTON ---
    col_title, col_btn = st.columns([4, 1])
    with col_title:
        st.title("🏨 Yield Equilibrium Center")
    with col_btn:
        st.write("") 
        if st.button("🔄 Clear Audit Data"):
            # Resets transaction keys without touching global settings
            for key in list(st.session_state.keys()):
                if any(kp in key for kp in ["ot", "di", "wh", "co", "gt", "gc"]):
                    if "n" in key: st.session_state[key] = 1
                    else: st.session_state[key] = 0.0 if isinstance(st.session_state[key], float) else 0
            st.rerun()

    def run(rms, adr, nts, mix, cp, fl, ev_rev=0, total_tr_cost=0):
        t_rms = sum(rms)
        if t_rms <= 0: return None
        pax = (rms[0]*1 + rms[1]*2 + rms[2]*3)
        gross_total = (adr * t_rms * nts) + (ev_rev * pax * nts)
        
        nt_rev = (adr * t_rms) / tx
        fb_cost = sum(q * m[p] * (pax / t_rms) for p, q in mix.items())
        ev_w = (ev_rev * pax) / tx
        cm = (nt_rev - fb_cost) * cp
        
        dp = ((nt_rev - fb_cost - cm) - (p01 * t_rms)) + (ev_w / t_rms)
        tp = (dp * t_rms * nts) - (total_tr_cost / tx)
        u = tp / (t_rms * nts)
        
        # Calculate impact for displacement insight
        inv_impact = (t_rms / h_cp) * 100
        
        af = fl * 0.75 if nts > 7 else fl
        fric = (1 - (tp / gross_total)) * 100 if gross_total > 0 else 0
        
        if fric < 26: fric_lb = "Net Contribution"
        elif 26 <= fric < 38: fric_lb = "Yield Dilution"
        else: fric_lb = "Revenue Erosion"
        
        if u < af: lb, cl = "DILUTIVE", "#e74c3c"
        elif af <= u < (af + 5): lb, cl = "MARGINAL", "#f1c40f"
        else: lb, cl = "OPTIMIZED", "#27ae60"
        
        return {"u": u
