import streamlit as st

# --- BRANDING ---
st.set_page_config(page_title="Yield Equilibrium Master Auditor", layout="wide")
st.title("🏨 Yield Equilibrium: Full Property & F&B Auditor")
st.markdown("Developed by **Gayan Nugawela** | *The Surgical Total Revenue Framework*")
st.divider()

# --- SIDEBAR: DETAILED F&B ALLOCATIONS (PER PERSON) ---
st.sidebar.header("🍽️ Per Person Net Costs")
st.sidebar.caption("Enter the internal cost per guest")

# Exact words as requested - no brackets
cost_bb = st.sidebar.number_input("Breakfast Allocation", value=5.0)
cost_lunch = st.sidebar.number_input("Lunch Allocation", value=7.0)
cost_dinner = st.sidebar.number_input("Dinner Allocation", value=10.0)
cost_sai = st.sidebar.number_input("SAI Allocation", value=8.0)
cost_ai = st.sidebar.number_input("AI Allocation", value=15.0)
cost_mice = st.sidebar.number_input("MICE/Delegate Supplement", value=20.0)

# Build the Meal Map
# SAI = BB + Lunch + Dinner + SAI Specific Cost
# AI = BB + Lunch + Dinner + SAI Specific Cost + AI Specific Cost
meal_map = {
    "RO": 0,
    "BB": cost_bb,
    "HB": cost_bb + cost_dinner,
    "FB": cost_bb + cost_lunch + cost_dinner,
    "SAI": cost_bb + cost_lunch + cost_dinner + cost_sai,
    "AI": cost_bb + cost_lunch + cost_dinner + cost_sai + cost_ai,
    "MICE": cost_bb + cost_mice
}

st.sidebar.divider()
tax_div = st.sidebar.number_input("Tax Divisor", value=1.2327, format="%.4f")
currency = st.sidebar.selectbox("Currency", ["OMR", "USD", "AED", "THB"])

# --- CALCULATION ENGINE ---
def run_audit(sgl, dbl, tpl, comp, adr, plan, trans, comm, p01, floor):
    paid_r = sgl + dbl + tpl
    total_r = paid_r + comp
    pax = (sgl * 1) + (dbl * 2) + (tpl * 3)
    
    if total_r == 0: 
        return {"room_p": 0, "fb_p": 0, "unit": 0, "stat": "N/A", "col": "gray"}

    total_net_rev = (adr * paid_r) / tax_div
    total_fb_rev = meal_map[plan] * pax
    room_wealth = total_net_rev - total_fb_rev - (trans / tax_div)
    total_room_profit = (room_wealth * (1 - comm)) - (p01 * total_r)
    
    unit_net = total_room_profit / total_r
    status, col = ("🔴 DILUTIVE", "red")
    if unit_net >= (floor + 10): status, col = ("🟢 OPTIMIZED", "green")
    elif unit_net >= floor: status, col = ("🟡 STABLE", "orange")
    
    return {"room_p": total_room_profit, "fb_p": total_fb_rev, "unit": unit_net, "stat": status, "col": col}

# --- SEGMENT INPUTS ---
st.header("📊 Detailed Segment Inputs")
row1_a, row1_b, row1_c = st.columns(3)
row2_a, row2_b = st.columns(2)

def segment_box(col, label, key_prefix, default_adr, default_floor, plans):
    with col:
        with st.expander(f"📍 {label}", expanded=True):
            s = st.number_input(f"{label} SGL", 5, key=f"{key_prefix}s")
            d = st.number_input(f"{label} DBL", 10, key=f"{
