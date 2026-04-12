import streamlit as st

# --- BRANDING & CUSTOM CSS ---
st.set_page_config(page_title="Yield Equilibrium Master Auditor", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 10px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("🏨 Yield Equilibrium: Full Property Command Center")
st.markdown("Developed by **Gayan Nugawela** | *Director-Level Total Revenue Strategy*")
st.divider()

# --- SIDEBAR: MASTER ALLOCATIONS ---
st.sidebar.header("🍽️ Per Person Net Costs")
c_bb = st.sidebar.number_input("Breakfast Allocation", value=5.0)
c_lh = st.sidebar.number_input("Lunch Allocation", value=7.0)
c_dr = st.sidebar.number_input("Dinner Allocation", value=10.0)
c_sai = st.sidebar.number_input("SAI Allocation", value=8.0)
c_ai = st.sidebar.number_input("AI Allocation", value=15.0)

meal_map = {
    "RO": 0, "BB": c_bb, "HB": c_bb + c_dr, "FB": c_bb + c_lh + c_dr,
    "SAI": c_bb + c_lh + c_dr + c_sai, "AI": c_bb + c_lh + c_dr + c_sai + c_ai
}

st.sidebar.divider()
tax_div = st.sidebar.number_input("Tax Divisor", value=1.2327, format="%.4f")
currency = st.sidebar.selectbox("Currency", ["OMR", "USD", "AED", "THB"])

# --- CALCULATION ENGINE ---
def run_audit(sgl, dbl, tpl, comp, adr, plan_counts, trans, comm, p01, floor):
    paid_r = sgl + dbl + tpl
    total_r = paid_r + comp
    pax_ratio = ((sgl*1) + (dbl*2) + (tpl*3)) / paid_r if paid_r > 0 else 0
    
    if total_r == 0: 
        return {"room_p": 0, "fb_p": 0, "unit": 0, "stat": "N/A", "col": "gray", "total_w": 0}
    
    total_net_rev = (adr * paid_r) / tax_div
    total_fb_rev = sum(count * meal_map[plan] * pax_ratio for plan, count in plan_counts.items())
    room_wealth = total_net_rev - total_fb_rev - (trans / tax_div)
    total_room_profit = (room_wealth *
