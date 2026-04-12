import streamlit as st

# --- BRANDING & STYLE ---
st.set_page_config(page_title="Yield Equilibrium Master Auditor", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { border: 1px solid #dee2e6; padding: 10px; border-radius: 8px; background-color: white; }
    .definition-box { font-size: 13px; color: #555; margin-top: 5px; line-height: 1.3; font-style: italic; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏨 Yield Equilibrium: Strategic Command Center")
st.markdown("Developed by **Gayan Nugawela** | *Director-Level Property Audit*")
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
    
    if paid_r <= 0:
        return {"room_p": 0.0, "fb_p": 0.0, "unit": 0.0, "stat": "Waiting...", "col": "gray", "def": "Enter inventory to begin audit."}
    
    # Calculate pax ratio for weighted extraction
    pax_ratio = ((sgl * 1.0) + (dbl * 2.0) + (tpl * 3.0)) / paid_r
    total_net_rev = (adr * paid_r) / tax_div
    
    # Extract F&B Wealth surgically based on the mix
    total_fb_rev = sum(count * meal_map[plan] * pax_ratio for plan, count in plan_counts.items())
    
    room_wealth = total_net_rev - total_fb_rev - (trans / tax_div)
    
    # Final profit calculation - fully closed
    total_room_profit = (room_wealth * (1.0 - comm)) - (p01 * total_r)
    unit_net = total_room_profit / total_r
    
    # Verdict Logic (Optimized, Marginal, Dilutive)
    if unit_net >= (floor + 10.0):
        res = {"stat": "🟢 OPTIMIZED", "col": "green", "def": "High
