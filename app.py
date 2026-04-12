import streamlit as st

# --- BRANDING & STYLE ---
st.set_page_config(page_title="Yield Equilibrium Auditor", layout="wide")
st.markdown("<style>.stMetric { background-color: white; border: 1px solid #ddd; padding: 10px; border-radius: 10px; } .row-box { background-color: rgba(0,0,0,0.03); padding: 12px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid; }</style>", unsafe_allow_html=True)

st.title("Yield Equilibrium: Total Revenue Command Center")
st.caption("Developed by Gayan Nugawela | Full Meal Plan Allocation Logic Active")

# --- SIDEBAR SETTINGS ---
with st.sidebar:
    st.header("1. Meal Plan Net Costs (Per Pax)")
    c_bb = st.number_input("Breakfast Cost", value=5.0)
    c_lh = st.number_input("Lunch Cost", value=7.0)
    c_dr = st.number_input("Dinner Cost", value=10.0)
    c_sai = st.number_input("SAI Supplement", value=8.0)
    c_ai = st.number_input("AI Supplement", value=15.0)
    
    # Logic: Summing costs for each plan
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
    
    # Surgical Pax Ratio
    pax_ratio = ((s * 1.0) + (d * 2.0) + (t * 3.0)) / paid
    total_net_rev = (adr * paid) / tax_div
    
    # Total F&B cost across all meal plans
    fb_total = sum(qty * meal_costs[plan] * pax_ratio for plan, qty in counts.items())
    
    # Net Wealth Calculation
    profit = ((total_net_rev - fb_total) * (1.0 - comm)) - (p01_fee * paid)
    unit_wealth = profit / paid
    
    if unit_wealth >= (floor + 10
