import streamlit as st

# --- BRANDING ---
st.set_page_config(page_title="Yield Equilibrium Master Auditor", layout="wide")
st.markdown("""
    <style>
    .segment-card {
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 10px;
        border-left: 10px solid;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏨 Yield Equilibrium: Full Property Auditor")
st.markdown("Developed by **Gayan Nugawela** | *The Surgical Total Revenue Command Center*")
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
    if total_r == 0: return {"room_p": 0, "fb_p": 0, "unit": 0, "stat": "N/A", "col": "gray", "total_w": 0}
    
    total_net_rev = (adr * paid_r) / tax_div
    total_fb_rev = sum(count * meal_map[plan] * pax_ratio for plan, count in plan_counts.items())
    room_wealth = total_net_rev - total_fb_rev - (trans / tax_div)
    total_room_profit = (room_wealth * (1 - comm)) - (p01 * total_r)
    
    unit_net = total_room_profit / total_r
    status, col = ("🔴 DILUTIVE", "red")
    if unit_net >= (floor + 10): status, col = ("🟢 OPTIMIZED", "green")
    elif unit_net >= floor: status, col = ("🟡 STABLE", "orange")
    
    return {"room_p": total_room_profit, "fb_p": total_fb_rev, "unit": unit_net, "stat": status, "col": col, "total_w": total_room_profit + total_fb_rev}

# --- SEGMENT ROWS ---
def segment_row(icon, label, color, key_p, adr_def, floor_def):
    st.markdown(f"""<div style="background-color: {color}22; border-left: 10px solid {color}; padding: 15px; border-radius: 10px;">
        <h3 style="margin:0;">{icon} {label} Segment</h3>
        </div>""", unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns([1.5, 2, 1.5, 1.5])
    
    with c1:
        st.caption("Inventory")
        s = st.number_input(f"SGL", 0, key=f"{key_p}s")
        d = st.number_input(f"DBL", 0, key=f"{key_p}d")
        t = st.number_input(f"TPL", 0, key=f"{key_p}t")
        total = s + d + t
    
    with c2:
        st.caption(f"Meal Distribution ({total} rooms)")
        p_bb = st.number_input("Qty BB", 0, total, key=f"{key_p}pbb")
        p_hb = st.number_input("Qty HB", 0, total, key=f"{key_p}phb")
        p_fb = st.number_input("Qty FB", 0, total, key=f"{key_p}pfb")
        counts = {"BB": p_bb, "HB": p_hb, "FB": p_fb, "RO": total - (p_bb+p_hb+p_fb), "SAI":0, "AI":0}
        
    with c3:
        st.caption("Commercials")
        adr = st.number_input("Gross ADR", adr_def, key=f"{key_p}a")
        flr = st.number_input("Floor", floor_def, key=f"{key_p}f")
        
    # Execution
    res = run_audit(s, d, t, 0, adr, counts, 0, 0, 10.0, flr
