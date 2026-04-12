import streamlit as st

# --- BRANDING ---
st.set_page_config(page_title="Yield Equilibrium Master Auditor", layout="wide")
st.title("🏨 Yield Equilibrium: Full Property Segment Auditor")
st.markdown("Developed by **Gayan Nugawela** | *The Surgical Total Revenue Framework*")
st.divider()

# --- SIDEBAR: MASTER RATE CONFIG ---
st.sidebar.header("🍽️ F&B & MICE Net Credits")
st.sidebar.caption("Per Person Rates (Net of Tax)")
rate_bb = st.sidebar.number_input("Breakfast Credit", value=6.0)
rate_hb = st.sidebar.number_input("HB Supplement", value=12.0)
rate_fb = st.sidebar.number_input("FB Supplement", value=22.0)
rate_mice = st.sidebar.number_input("MICE / Meeting Package", value=30.0)

meal_map = {
    "RO": 0, "BB": rate_bb, "HB": rate_bb + rate_hb, 
    "FB": rate_bb + rate_fb, "MICE/Events": rate_bb + rate_mice
}

st.sidebar.divider()
tax_div = st.sidebar.number_input("Tax Divisor", value=1.2327, format="%.4f")
currency = st.sidebar.selectbox("Currency", ["OMR", "USD", "AED", "THB"])

# --- CALCULATION ENGINE ---
def run_audit(sgl, dbl, tpl, comp, adr, plan, trans, comm, p01, floor):
    paid_r = sgl + dbl + tpl
    total_r = paid_r + comp
    pax = (sgl * 1) + (dbl * 2) + (tpl * 3)
    
    if total_r == 0: return {"room_p": 0, "fb_p": 0, "unit": 0, "stat": "N/A", "col": "gray", "total_w": 0}

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

# Create two rows of columns to fit all 5 segments
row1_a, row1_b, row1_c = st.columns(3)
row2_a, row2_b = st.columns(2)

# Segment 1: Direct
with row1_a:
    with st.expander("👤 Direct / Individual", expanded=True):
        d_s = st.number_input("Direct SGL", 2, key="ds")
        d_d = st.number_input("Direct DBL", 5, key="dd")
        d_t = st.number_input("Direct TPL", 1, key="dt")
        d_adr = st.number_input("Direct ADR", 200.0, key="da")
        d_plan = st.selectbox("Direct Plan", ["RO", "BB", "HB"], index=1, key="dp")
        d_floor = st.number_input("Direct Floor", 110.0, key="df")

# Segment 2: Corporate (Individual)
with row1_b:
    with st.expander("💼 Corporate", expanded=True):
        c_s = st.number_input("Corp SGL", 10, key="cs")
        c_d = st.number_input("Corp DBL", 5, key="cd")
        c_t = st.number_input("Corp TPL", 0, key="ct")
        c_adr = st.number_input("Corp ADR", 160.0, key="ca")
        c_plan = st.selectbox("Corp Plan", ["RO", "BB"], index=1, key="cp")
        c_floor = st.number_input("Corp Floor", 90.0, key="cf")

# Segment 3: Group Tour & Travels
with row1_c:
    with st.expander("🌍 Group Tour & Travels", expanded=True):
        g_s = st.number_input("G-Tour SGL", 10, key="gs")
        g_d = st.number_input("G-Tour DBL", 20, key="gd")
        g_t = st.number_input("G-Tour TPL", 5, key="gt")
        g_adr = st.number_input("G-Tour ADR", 140.0, key="ga")
        g_plan = st.selectbox("G-Tour Plan", ["BB", "HB", "FB"], index=1, key="gp")
        g_floor = st.number_input("G-Tour Floor", 80.0, key="gf")

# Segment 4: Corporate Groups / MICE
with row2_a:
    with st.expander("🏢 Corporate Groups / MICE", expanded=True):
        m_s = st.number_input("MICE SGL", 15, key="ms")
        m_d = st.number_input("MICE DBL", 10, key="md")
        m_t = st.number_input("MICE TPL", 2, key="mt")
        m_adr = st.number_input("MICE ADR", 150.0, key="ma")
        m_plan = st.selectbox("MICE Plan", ["HB", "FB", "MICE/Events"], index=2, key="mp")
        m_floor = st.number_input("MICE Floor", 85.0, key="mf")

# Segment 5: OTA (Standard)
with row2_b:
    with st.expander("📱 OTA / Booking.com", expanded=True):
        o_s = st.number_input("OTA SGL", 5, key="os")
        o_d = st.number_input("OTA DBL", 15, key="od")
        o_t = st.number_input("OTA TPL", 3, key="ot")
        o_adr = st.number_input("OTA ADR", 190.0, key="oa")
        o_plan = st.selectbox("OTA Plan", ["RO", "BB", "HB"], index=1, key="op")
        o_floor = st.number_input("OTA Floor", 100.0, key="of")

# --- EXECUTE AUDITS ---
res_direct = run_audit(d_s, d_d, d_t, 0, d_adr, d_plan, 0, 0.0, 10.0, d_floor)
res_corp = run_audit(c_s, c_d, c_t, 0, c_adr, c_plan, 0, 0.0, 10.0, c_floor)
res_tour = run_audit(g_s, g_d, g_t, 2, g_adr, g_plan, 0, 0.15, 10.0, g_floor)
res_mice = run_audit(m_s, m_d, m_t, 3, m_adr, m_plan, 150.0, 0.10, 10.0, m_floor)
res_ota = run_audit(o_s, o_d, o_t, 0, o_adr, o_plan, 0, 0.18, 10.0, o_floor)

# --- DISPLAY RESULTS ---
st.divider()
st.header("📊 Audit Results Summary")

def display_res(name, res):
    st.markdown(f"### {name}")
    st.metric("Surgical Unit Net", f"{currency} {res['unit']:.2f}")
    st.markdown(f"Status: :{res['col']}[{res['stat']}]")
    st.caption(f"F&B/Events Rev: {currency} {res['fb_p']:,.0f}")

# Display in columns
c1, c2, c3, c4, c5 = st.columns(5)
with c1: display_res("Direct", res_direct)
with c2: display_res("Corporate", res_corp)
with c3: display_res("Tour & Travel", res_tour)
with c4: display_res("Corp Group", res_mice)
with c5: display_res("OTA", res_ota)

# --- TOTAL PROPERTY WEALTH ---
st.divider()
st.header("🏢 Property Wealth Total")
total_room_p = res_direct['room_p'] + res_corp['room_p'] + res_tour['room_p'] + res_mice['room_p'] + res_ota['room_p']
total_fb_p = res_direct['fb_p'] + res_corp['fb_p'] + res_tour['fb_p'] + res_mice['fb_p'] + res_ota['fb_p']

m1, m2, m3 = st.columns(3)
m1.metric("Total Net Room Wealth", f"{currency} {total_room_p:,.2f}")
m2.metric("Total F&B/Events Revenue", f"{currency} {total_fb_p:,.2f}")
m3.metric("Combined Property Wealth", f"{currency} {(total_room_p + total_fb_p):,.2f}")
