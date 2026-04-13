import streamlit as st
import pandas as pd

# --- CONFIGURATION ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium")

# --- PASSWORD PROTECTION ---
def check_password():
    if "auth" not in st.session_state:
        st.session_state["auth"] = False
    
    if not st.session_state["auth"]:
        st.title("🏨 Yield Equilibrium Center")
        pwd = st.text_input("Access Key", type="password")
        
        # Check if password matches
        if st.button("Unlock") or (pwd == "Gayan2026"): 
            if pwd == "Gayan2026":
                st.session_state["auth"] = True
                st.rerun()
            elif pwd != "":
                st.error("Invalid Key")
        return False
    return True

if check_password():
    # --- STYLING ---
    st.markdown("""
        <style>
        .stMetric {background:#fff; border:1px solid #eee; padding:10px; border-radius:10px}
        .card {padding:10px; border-radius:8px; margin-bottom:10px; border-left:8px solid; font-weight:bold; color: #2c3e50;}
        .pillar-box {background:#f8f9fa; padding:15px; border-radius:10px; border-top:4px solid #2c3e50; min-height: 200px;}
        </style>
    """, unsafe_allow_html=True)
    
    # --- SIDEBAR: ARCHITECT & SETTINGS ---
    with st.sidebar:
        st.title("👨‍💼 Architect")
        st.subheader("Gayan Nugawela")
        st.write("MBA | CRME | CHRM | RevOps")
        st.caption("Revenue Management Expert & SME")
        st.divider()
        
        st.title("⚙️ Global Settings")
        hotel_name = st.text_input("Hotel", "Wyndham Garden Salalah")
        inventory = st.number_input("Total Inventory", 1, 1000, 158)
        
        st.header("🍽️ Meals (Net)")
        b = st.number_input("BB", 0.0, 500.0, 2.0)
        l = st.number_input("LN", 0.0, 500.0, 6.0)
        d_cost = st.number_input("DN", 0.0, 500.0, 6.0)
        s_cost = st.number_input("SAI", 0.0, 500.0, 8.0)
        a_cost = st.number_input("AI", 0.0, 500.0, 15.0)
        
        meal_map = {
            "RO": 0.0, 
            "BB": b, 
            "HB": b + d_cost, 
            "FB": b + l + d_cost, 
            "SAI": b + l + d_cost + s_cost, 
            "AI": b + l + d_cost + s_cost + a_cost
        }
        
        p01_fee = st.number_input("P01 Fee", 0.0, 100.0, 6.9)
        tax_div = st.number_input("Tax Divisor", 1.0, 2.0, 1.2327, format="%.4f")
        ota_comm = st.slider("OTA Comm %", 0, 50, 18) / 100
        
        currency = st.selectbox("Currency", ["OMR", "AED", "SAR", "KWD", "BHD", "QAR", "USD", "EUR", "GBP"])

    # --- MAIN HEADER ---
    col_t, col_b = st.columns([4, 1])
    with col_t:
        st.title("🏨 Yield Equilibrium Center")
    with col_b:
        if st.button("🔄 Reset Audit"):
            for key in list(st.session_state.keys()):
                if any(kp in key for kp in ["ot", "di", "wh", "co", "gt", "gc"]):
                    st.session_state[key] = 1 if "n" in key else 0
            st.rerun()

    # --- CORE CALCULATION LOGIC ---
    def calculate_yield(rms, adr, nts, mix, comm_pct, hurdle, ev_rev=0, trans_cost=0):
        t_rms = sum(rms)
        if t_rms <= 0: return None
        
        pax = float(rms[0]*1 + rms[1]*2 + rms[2]*3)
        nts = float(nts)
        
        gross_total = (adr * t_rms * nts) + (ev_rev * pax * nts)
        net_rev_per_room = adr / tax_div
        
        # F&B Costing
        fb_cost_total = sum(q * meal_map[p] * (pax / t_rms) for p, q in mix.items())
        
        event_wealth = (ev_rev * pax) / tax_div
        comm_drag = (net_rev_per_room - fb_cost_total) * comm_pct
        
        daily_profit = (net_rev_per_room - fb_cost_total - comm_drag - p01_fee) + (event_wealth / t_rms)
        total_wealth = (daily_profit * t_rms * nts) - (trans_cost / tax_div)
        wealth_per_room = total_wealth / (t_rms * nts)
        
        fric = (1 - (total_wealth / gross_total)) * 100 if gross_total > 0 else 0
        
        # Status Color Logic
        if wealth_per_room < hurdle: status, color = "DILUTIVE", "#e74c3c"
        elif hurdle <= wealth_per_room < (hurdle + 5): status, color = "MARGINAL", "#f1c40f"
        else: status, color = "OPTIMIZED", "#27ae60"
        
        return {
            "u": wealth_per_room, "s": status, "c": color, 
            "tp": total_wealth, "pax": int(pax), "fric": fric, 
            "impact": (t_rms / inventory) * 100
        }

    # --- UI SEGMENT BUILDER ---
    def render
