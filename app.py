import streamlit as st

# --- BRANDING ---
st.set_page_config(page_title="Yield Equilibrium Master Auditor", layout="wide")
st.title("🏨 Yield Equilibrium: Full Property & F&B Auditor")
st.markdown("Developed by **Gayan Nugawela** | *The Surgical Total Revenue Framework*")
st.divider()

# --- SIDEBAR: DETAILED F&B ALLOCATIONS (PER PERSON) ---
st.sidebar.header("🍽️ Per Person Net Costs")
cost_bb = st.sidebar.number_input("Breakfast Cost", value=5.0)
cost_lunch = st.sidebar.number_input("Lunch Cost", value=7.0)
cost_dinner = st.sidebar.number_input("Dinner Cost", value=10.0)
cost_soft_bev = st.sidebar.number_input("Soft Beverage Cost (SAI)", value=8.0)
cost_liq = st.sidebar.number_input("Liquor/Alcohol Cost (AI)", value=15.0)
cost_mice = st.sidebar.number_input("MICE/Delegate Supplement", value=20.0)

# Build the Meal Map
meal_map = {
    "RO": 0,
    "BB": cost_bb,
    "HB": cost_bb + cost_dinner,
    "FB": cost_bb + cost_lunch + cost_dinner,
    "SAI": cost_bb + cost_lunch + cost_dinner + cost_soft_bev,
    "AI": cost_bb + cost_lunch + cost_dinner + cost_soft_bev + cost_liq,
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
        return {"room_p": 0, "fb_p": 0, "unit": 0, "stat": "N/A", "col": "gray", "total_w": 0}

    total_net_rev = (adr * paid_r) / tax_div
    total_fb_rev = meal_map[plan] * pax
    room_wealth = total_net_rev - total_fb_rev - (trans / tax_div)
    total_room_profit = (room_wealth * (1 - comm)) - (p01 * total_r)
    
    unit_net = total_room_profit / total_r
    status, col = ("🔴 DILUTIVE", "red")
    if unit_net >= (floor + 10): status, col = ("🟢 OPTIMIZED", "green")
    elif unit_net >= floor: status, col = ("🟡 STABLE", "orange")
    
    return {"room_p": total_room_profit, "fb_p": total_fb_rev, "unit": unit_net, "stat": status, "col": col, "total_w": total_room_profit + total_fb_rev}

# --- SEGMENT INPUTS ---
st.header("📊 Detailed Segment Inputs")
row1_a, row1_b, row1_c = st.columns(3)
row2_a, row2_b = st.columns(2)

def segment_box(col, label, key_prefix, default_adr, default_floor, plans):
    with col:
        with st.expander(f"📍 {label}", expanded=True):
            s = st.number_input(f"{label} SGL", 5, key=f"{key_prefix}s")
            d = st.number_input(f"{label} DBL", 10, key=f"{key_prefix}d")
            t = st.number_input(f"{label} TPL", 2, key=f"{key_prefix}t")
            c = st.number_input(f"{label} COMP", 0, key=f"{key_prefix}c")
            adr = st.number_input(f"{label} Gross ADR", default_adr, key=f"{key_prefix}a")
            plan = st.selectbox(f"{label} Plan", plans, key=f"{key_prefix}p")
            flr = st.number_input(f"{label} Floor", default_floor, key=f"{key_prefix}f")
            return s, d, t, c, adr, plan, flr

# Capture Data
d_data = segment_box(row1_a, "Direct", "dir", 200.0, 110.0, ["RO", "BB", "HB"])
c_data = segment_box(row1_b, "Corporate", "cor", 160.0, 95.0, ["RO", "BB"])
t_data = segment_box(row1_c, "Group Tour & Travel", "tou", 140.0, 80.0, ["BB", "HB", "FB", "SAI", "AI"])
m_data = segment_box(row2_a, "Corporate Groups", "mic", 155.0, 85.0, ["HB", "FB", "MICE"])
o_data = segment_box(row2_b, "OTA", "ota", 190.0, 100.0, ["RO", "BB", "HB"])

# --- EXECUTE AUDITS ---
res_dir = run_audit(*d_data, 0, 0.0, 10.0, d_data[6])
res_corp = run_audit(*c_data, 0, 0.0, 10.0, c_data[6])
res_tour = run_audit(*t_data, 0, 0.15, 10.0, t_data[6])
res_mice = run_audit(*m_data, 150.0, 0.10, 10.0, m_data[6])
res_ota = run_audit(*o_data, 0, 0.18, 10.0, o_data[6])

# --- RESULTS SUMMARY ---
st.divider()
st.header("📊 Audit Results Summary")

def display_res(name, res):
    st.markdown(f"### {name}")
    st.metric("Surgical Net", f"{currency} {res['unit']:.2f}")
    st.markdown(f"Status: :{res['col']}[{res['stat']}]")
    st.caption(f"F&B/Events Rev: {currency} {res['fb_p']:,.0f}")

c1, c2, c3, c4, c5 = st.columns(5)
with c1: display_res("Direct", res_dir)
with c2: display_res("Corporate", res_corp)
with c3: display_res("Tour & Travel", res_tour)
with c4: display_res("Corp Group", res_mice)
with c5: display_res("OTA", res_ota)

# --- TOTAL PROPERTY WEALTH ---
st.divider()
st.header("🏢 Total Property Wealth Summary")
total_room_p = sum(r['room_p'] for r in [res_dir, res_corp, res_tour, res_mice, res_ota])
total_fb_p = sum(r['fb_p'] for r in [res_dir, res_corp, res_tour, res_mice, res_ota])

m1, m2, m3 = st.columns(3)
m1.metric("Total Net Room Wealth", f"{currency} {total_room_p:,.2f}")
m2.metric("Total F&B/Events Revenue", f"{currency} {total_fb_p:,.2f}")
m3.metric("Combined Property Wealth", f"{currency} {(total_room_p + total_fb_p):,.2f}")
