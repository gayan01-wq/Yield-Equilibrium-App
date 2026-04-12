import streamlit as st

# --- CORE CONFIG ---
st.set_page_config(page_title="Yield Equilibrium Auditor", layout="wide")
st.markdown("<style>.stMetric { background-color: white; border: 1px solid #ddd; padding: 10px; border-radius: 10px; } .row-box { background-color: rgba(0,0,0,0.03); padding: 12px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid; }</style>", unsafe_allow_html=True)

st.title("Yield Equilibrium: Total Revenue Command Center")
st.caption("Developed by Gayan Nugawela | HB, FB, AI, SAI Allocation Logic Active")

# --- SIDEBAR SETTINGS ---
with st.sidebar:
    st.header("1. Meal Plan Net Costs (Per Pax)")
    c_bb = st.number_input("Breakfast Cost", value=5.0)
    c_lh = st.number_input("Lunch Cost", value=7.0)
    c_dr = st.number_input("Dinner Cost", value=10.0)
    c_sai = st.number_input("SAI Supplement", value=8.0)
    c_ai = st.number_input("AI Supplement", value=15.0)
    
    # Logic mapping for the engine
    meal_costs = {
        "RO": 0.0,
        "BB": c_bb,
        "HB": c_bb + c_dr,
        "FB": c_bb + c_lh + c_dr,
        "SAI": c_bb + c_lh + c_dr + c_sai,
        "AI": c_bb + c_lh + c_dr + c_sai + c_ai
    }

    st.header("2. Operating Fees")
    p01_fee = st.number_input("Maintenance Fee (Per Room)", value=10.0)
    tax_div = st.number_input("Tax Divisor", value=1.2327, format="%.4f")
    currency = st.selectbox("Currency", ["OMR", "USD", "AED", "THB"])

# --- CALCULATION ENGINE ---
def run_audit(s, d, t, adr, counts, comm, floor):
    paid = s + d + t
    if paid <= 0:
        return {"rp": 0.0, "un": 0.0, "st": "Waiting", "cl": "gray", "tfb": 0.0}
    
    pax_ratio = ((s * 1.0) + (d * 2.0) + (t * 3.0)) / paid
    total_net_rev = (adr * paid) / tax_div
    
    # Total F&B cost based on the mix of meal plans
    fb_total = sum(qty * meal_costs[plan] * pax_ratio for plan, qty in counts.items())
    
    # Net Wealth: (Rev - F&B) * (1 - Comm) - Fees
    profit = ((total_net_rev - fb_total) * (1.0 - comm)) - (p01_fee * paid)
    unit_wealth = profit / paid
    
    if unit_wealth >= (floor + 10.0): res = {"st": "OPTIMIZED", "cl": "green"}
    elif unit_wealth >= floor: res = {"st": "MARGINAL", "cl": "orange"}
    else: res = {"st": "DILUTIVE", "cl": "red"}
    
    res.update({"rp": profit, "un": unit_wealth, "tfb": fb_total})
    return res

# --- UI SEGMENT ROW ---
def segment(label, color, kp, adr_d, flr_d, comm_rate):
    st.markdown(f"<div class='row-box' style='border-left-color: {color};'><h3>{label}</h3></div>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns([1.5, 2.5, 1.2, 1.2])
    
    with c1:
        s = st.number_input("SGL", 0, key=kp+"s")
        d = st.number_input("DBL", 0, key=kp+"d")
        t = st.number_input("TPL", 0, key=kp+"t")
        tot = s + d + t
    
    with c2:
        st.write(f"Meal Mix (Total: {tot})")
        col_a, col_b = st.columns(2)
        with col_a:
            q_bb = st.number_input("BB Qty", 0, tot, key=kp+"bb")
            q_hb = st.number_input("HB Qty", 0, tot, key=kp+"hb")
            q_fb = st.number_input("FB Qty", 0, tot, key=kp+"fb")
        with col_b:
            q_sai = st.number_input("SAI Qty", 0, tot, key=kp+"sai")
            q_ai = st.number_input("AI Qty", 0, tot, key=kp+"ai")
        
        q_ro = max(0, tot - (q_bb + q_hb + q_fb + q_sai + q_ai))
        counts = {"BB": q_bb, "HB": q_hb, "FB": q_fb, "SAI": q_sai, "AI": q_ai, "RO": q_ro}
    
    with c3:
        adr = st.number_input("Gross ADR", 1.0, 5000.0, float(adr_d), key=kp+"a")
        flr = st.number_input("Floor", 1.0, 2000.0, float(flr_d), key=kp+"fl")
    
    res = run_audit
