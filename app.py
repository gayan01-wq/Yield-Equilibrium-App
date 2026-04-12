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
    
    # Surgical Pax Ratio calculation
    pax_ratio = ((sgl * 1.0) + (dbl * 2.0) + (tpl * 3.0)) / paid_r
    total_net_rev = (adr * paid_r) / tax_div
    
    # Weighted F&B Extraction
    total_fb_rev = sum(count * meal_map[plan] * pax_ratio for plan, count in plan_counts.items())
    
    room_wealth = total_net_rev - total_fb_rev - (trans / tax_div)
    
    # Final Wealth Calculation
    total_room_profit = (room_wealth * (1.0 - comm)) - (p01 * total_r)
    unit_net = total_room_profit / total_r
    
    # Verdict Logic & Indications
    if unit_net >= (floor + 10.0):
        res = {"stat": "🟢 OPTIMIZED", "col": "green", "def": "High wealth retention. Exceeds profit floor targets."}
    elif unit_net >= floor:
        res = {"stat": "🟡 MARGINAL", "col": "orange", "def": "Meets basic floor. Low room wealth efficiency."}
    else:
        res = {"stat": "🔴 DILUTIVE", "col": "red", "def": "Wealth Leakage. Costs are eroding room profit."}
    
    res.update({"room_p": total_room_profit, "fb_p": total_fb_rev, "unit": unit_net})
    return res

# --- SEGMENT ROW FUNCTION ---
def segment_row(icon, label, color, key_p, adr_def, floor_def, comm_rate):
    st.markdown(f"""<div style="background-color: {color}15; border-left: 8px solid {color}; padding: 12px; border-radius: 8px; margin-top: 15px;">
        <h3 style="margin:0; color: {color};">{icon} {label}</h3>
        </div>""", unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns([1.5, 2, 1.5, 1.5])
    
    with c1:
        s = st.number_input(f"SGL Rooms", 0, key=f"{key_p}s")
        d = st.number_input(f"DBL Rooms", 0, key=f"{key_p}d")
        t = st.number_input(f"TPL Rooms", 0, key=f"{key_p}t")
        total_rooms = s + d + t
    
    with c2:
        st.caption(f"Distribute {total_rooms} Rooms:")
        p_bb = st.number_input(f"Qty BB", 0, total_rooms, key=f"{key_p}pbb")
        p_hb = st.number_input(f"Qty HB", 0, total_rooms, key=f"{key_p}phb")
        p_fb = st.number_input(f"Qty FB", 0, total_rooms, key=f"{key_p}pfb")
        counts = {"BB": p_bb, "HB": p_hb, "FB": p_fb, "RO": total_rooms - (p_bb + p_hb + p_fb), "SAI": 0, "AI": 0}
        
    with c3:
        adr = st.number_input(f"Gross ADR", adr_def, key=f"{key_p}a")
        flr = st.number_input(f"Floor", floor_def, key=f"{key_p}f")
        
    res = run_audit(s, d, t, 0, adr, counts, 0.0, comm_rate, 10.0, flr)
    
    with c4:
        st.metric("Surgical Net", f"{currency} {res['unit']:.2f}")
        st.markdown(f"<p style='color:{res['col']}; font-weight:bold; margin-bottom:0;'>{res['stat']}</p>", unsafe_allow_html=True)
        st.markdown(f"<div class='definition-box'>{res['def']}</div>", unsafe_allow_html=True)
    
    return res

# --- RENDER GROUPS SECTION ---
st.header("🏢 Group & Wholesale Segments")
res_who = segment_row("✈️", "Wholesale", "#e67e22", "who", 130.0, 75.0, 0.20)
res_tour = segment_row("🚌", "Group Tour & Travel", "#d35400", "tou", 140.0, 80.0, 0.15)
res_mice = segment_row("🤝", "Corporate Groups / MICE", "#2c3e50", "mic", 150.0, 85.0, 0.0)

st.markdown("<br>", unsafe_allow_html=True)

# --- RENDER INDIVIDUALS SECTION ---
st.header("👤 Individual & FIT Segments")
res_dir = segment_row("🏠", "Direct / Member", "#3498db", "dir", 200.0, 110.0, 0.0)
res_corp = segment_row("💼", "Individual Corporate", "#9b59b6", "cor", 160.0, 95.0, 0.0)
res_ota = segment_row("📱", "OTA", "#2ecc71", "ota", 190.0, 100.0, 0.18)

# --- PROPERTY WEALTH SUMMARY ---
st.divider()
st.header("🏢 Property Wealth Summary")
all_res = [res_who, res_tour, res_mice, res_dir, res_corp, res_ota]
total_room_wealth = sum(r['room_p'] for r in all_res)
total_fb_allocation = sum(r['fb_p'] for r in all_res)

m1, m2, m3 = st.columns(3)
m1.metric("Total Room Wealth", f"{currency} {total_room_wealth:,.2f}")
m2.metric("Total F&B Allocation", f"{currency} {total_fb_allocation:,.2f}")
m3.metric("Combined Property Wealth", f"{currency} {(total_room_wealth + total_fb_allocation):,.2f}")
