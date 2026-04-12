import streamlit as st

# --- BRANDING ---
st.set_page_config(page_title="Yield Equilibrium Master Auditor", layout="wide")
st.title("🏨 Yield Equilibrium: Full Property Auditor")
st.markdown("Developed by **Gayan Nugawela** | *Mixed Plan & Total Revenue Strategy*")
st.divider()

# --- SIDEBAR: MASTER ALLOCATIONS (PER PERSON) ---
st.sidebar.header("🍽️ Per Person Net Costs")
c_bb = st.sidebar.number_input("Breakfast Allocation", value=5.0)
c_lh = st.sidebar.number_input("Lunch Allocation", value=7.0)
c_dr = st.sidebar.number_input("Dinner Allocation", value=10.0)
c_sai = st.sidebar.number_input("SAI Allocation", value=8.0)
c_ai = st.sidebar.number_input("AI Allocation", value=15.0)

# Build the Price Map
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

    # 1. Net Revenue
    total_net_rev = (adr * paid_r) / tax_div
    
    # 2. Weighted F&B Extraction (Mixed Plan Logic)
    total_fb_rev = sum(count * meal_map[plan] * pax_ratio for plan, count in plan_counts.items())
    
    # 3. Profit
    room_wealth = total_net_rev - total_fb_rev - (trans / tax_div)
    total_room_profit = (room_wealth * (1 - comm)) - (p01 * total_r)
    
    unit_net = total_room_profit / total_r
    status, col = ("🔴 DILUTIVE", "red")
    if unit_net >= (floor + 10): status, col = ("🟢 OPTIMIZED", "green")
    elif unit_net >= floor: status, col = ("🟡 STABLE", "orange")
    
    return {"room_p": total_room_profit, "fb_p": total_fb_rev, "unit": unit_net, "stat": status, "col": col, "total_w": total_room_profit + total_fb_rev}

# --- SEGMENT INPUTS ---
st.header("📊 Segment Audit (Mixed Plans Enabled)")
row1 = st.columns(3)
row2 = st.columns(3)

def segment_ui(col, icon, label, key_p, adr_def, floor_def):
    with col:
        with st.expander(f"{icon} {label}", expanded=True):
            s = st.number_input(f"SGL Rooms", 0, key=f"{key_p}s")
            d = st.number_input(f"DBL Rooms", 0, key=f"{key_p}d")
            t = st.number_input(f"TPL Rooms", 0, key=f"{key_p}t")
            c = st.number_input(f"COMP Rooms", 0, key=f"{key_p}c")
            total = s + d + t
            
            st.markdown("---")
            st.caption(f"Distribute {total} Rooms across plans:")
            p_bb = st.number_input("Qty on BB", 0, total, key=f"{key_p}pbb")
            p_hb = st.number_input("Qty on HB", 0, total, key=f"{key_p}phb")
            p_fb = st.number_input("Qty on FB", 0, total, key=f"{key_p}pfb")
            
            st.markdown("---")
            adr = st.number_input("Gross ADR", adr_def, key=f"{key_p}a")
            flr = st.number_input("Floor", floor_def, key=f"{key_p}f")
            
            counts = {"BB": p_bb, "HB": p_hb, "FB": p_fb, "RO": total - (p_bb+p_hb+p_fb), "SAI":0, "AI":0}
            return [s, d, t, c, adr, counts, flr]

# Core Segments
d_data = segment_ui(row1[0], "👤", "Direct", "dir", 200.0, 110.0)
c_data = segment_ui(row1[1], "💼", "Corporate", "cor", 160.0, 95.0)
w_data = segment_ui(row1[2], "✈️", "Wholesale", "who", 130.0, 75.0)
g_data = segment_ui(row2[0], "🚌", "Group Tour", "tou", 140.0, 80.0)
m_data = segment_ui(row2[1], "🏢", "MICE", "mic", 155.0, 85.0)
o_data = segment_ui(row2[2], "📱", "OTA", "ota", 190.0, 100.0)

# --- EXECUTE ---
segments = [("Direct", d_data, 0, 0), ("Corp", c_data, 0, 0), ("Whl", w_data, 0, 0.20),
            ("Tour", g_data, 0, 0.15), ("MICE", m_data, 150, 0.10), ("OTA", o_data, 0, 0.18)]

st.divider()
res_cols = st.columns(6)
res_list = []

for i, (name, data, trans, comm) in enumerate(segments):
    results = run_audit(data[0], data[1], data[2], data[3], data[4], data[5], trans, comm, 10.0, data[6])
    res_list.append(results)
    with res_cols[i]:
        st.markdown(f"### {name}")
        st.metric("Surgical Net", f"{currency} {results['unit']:.2f}")
        st.markdown(f"Status: :{results['col']}[{results['stat']}]")

# --- TOTAL PROPERTY WEALTH ---
st.divider()
t_room = sum(r['room_p'] for r in res_list)
t_fb = sum(r['fb_p'] for r in res_list)
m1, m2, m3 = st.columns(3)
m1.metric("Total Room Wealth", f"{currency} {t_room:,.2f}")
m2.metric("Total F&B Revenue", f"{currency} {t_fb:,.2f}")
m3.metric("Combined Property Wealth", f"{currency} {(t_room + t_fb):,.2f}")
