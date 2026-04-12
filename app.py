import streamlit as st

# --- BRANDING ---
st.set_page_config(page_title="Yield Equilibrium: Master Auditor", layout="wide")
st.title("🏨 Yield Equilibrium: Full Property Auditor")
st.markdown("Developed by **Gayan Nugawela** | *Segment & Enterprise Group Strategy*")
st.divider()

# --- SIDEBAR: MASTER RATE CONFIG ---
st.sidebar.header("🍽️ F&B & MICE Net Credits")
rate_bb = st.sidebar.number_input("Breakfast Credit", value=6.0)
rate_hb = st.sidebar.number_input("HB Supplement", value=12.0)
rate_fb = st.sidebar.number_input("FB Supplement", value=22.0)
rate_mice = st.sidebar.number_input("MICE Day Delegate Rate (DDR)", value=30.0)

meal_map = {"RO": 0, "BB": rate_bb, "HB": rate_bb + rate_hb, "FB": rate_bb + rate_fb, "MICE": rate_bb + rate_mice}

st.sidebar.divider()
tax_div = st.sidebar.number_input("Tax Divisor", value=1.2327, format="%.4f")
currency = st.sidebar.selectbox("Currency", ["OMR", "USD", "AED", "THB"])

# --- CALCULATION ENGINE ---
def run_audit(sgl, dbl, tpl, comp, adr, plan, trans, comm, p01, floor):
    paid_r = sgl + dbl + tpl
    total_r = paid_r + comp
    pax = (sgl * 1) + (dbl * 2) + (tpl * 3)
    
    if total_r == 0: return None

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
st.header("📊 Segment-Wise Analysis")
col_a, col_b, col_c = st.columns(3)

with col_a:
    with st.expander("OTA / FIT", expanded=True):
        o_s = st.number_input("OTA SGL", 5, key="os")
        o_d = st.number_input("OTA DBL", 10, key="od")
        o_adr = st.number_input("OTA ADR", 185.0, key="oa")
        o_plan = st.selectbox("OTA Plan", ["RO", "BB", "HB"], index=1, key="op")
        o_floor = st.number_input("OTA Floor", 90.0, key="of")

with col_b:
    with st.expander("Wholesale", expanded=True):
        w_s = st.number_input("WHL SGL", 10, key="ws")
        w_d = st.number_input("WHL DBL", 20, key="wd")
        w_adr = st.number_input("WHL ADR", 145.0, key="wa")
        w_plan = st.selectbox("WHL Plan", ["BB", "HB", "FB"], index=1, key="wp")
        w_floor = st.number_input("WHL Floor", 80.0, key="wf")

with col_c:
    with st.expander("MICE Group", expanded=True):
        m_s = st.number_input("MICE SGL", 10, key="ms")
        m_d = st.number_input("MICE DBL", 15, key="md")
        m_adr = st.number_input("MICE ADR", 155.0, key="ma")
        m_plan = st.selectbox("MICE Plan", ["HB", "FB", "MICE"], index=2, key="mp")
        m_floor = st.number_input("MICE Floor", 85.0, key="mf")

# --- EXECUTE & SHOW RESULTS ---
st.divider()
res_ota = run_audit(o_s, o_d, 0, 0, o_adr, o_plan, 0, 0.18, 10.0, o_floor)
res_whl = run_audit(w_s, w_d, 0, 2, w_adr, w_plan, 0, 0.15, 10.0, w_floor)
res_mice = run_audit(m_s, m_d, 0, 3, m_adr, m_plan, 100.0, 0.10, 10.0, m_floor)

r1, r2, r3 = st.columns(3)
for r, res, name in zip([r1, r2, r3], [res_ota, res_whl, res_mice], ["OTA", "Wholesale", "MICE"]):
    with r:
        st.subheader(name)
        st.metric("Surgical Net", f"{currency} {res['unit']:.2f}")
        st.markdown(f"Status: :{res['col']}[{res['stat']}]")
        st.caption(f"F&B Contribution: {currency} {res['fb_p']:,.0f}")

st.divider()
st.header("🏢 Property Wealth Total")
total_w = res_ota['total_w'] + res_whl['total_w'] + res_mice['total_w']
st.metric("Combined Property Wealth (Rooms + F&B)", f"{currency} {total_w:,.2f}")
