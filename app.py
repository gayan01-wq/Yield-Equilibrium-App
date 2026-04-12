import streamlit as st

# --- BRANDING ---
st.set_page_config(page_title="Yield Equilibrium: Enterprise Auditor", layout="wide")
st.title("🏨 Yield Equilibrium: Enterprise Group & MICE Auditor")
st.markdown("Developed by **Gayan Nugawela** | *Total Property Wealth Strategy*")
st.divider()

# --- SIDEBAR: MASTER RATE CONFIG ---
st.sidebar.header("🍽️ F&B & MICE Net Credits")
st.sidebar.caption("Per Person Rates (Net of Tax)")
rate_bb = st.sidebar.number_input("Breakfast Credit", value=6.0)
rate_hb = st.sidebar.number_input("HB Supplement", value=12.0)
rate_fb = st.sidebar.number_input("FB Supplement", value=22.0)
rate_mice = st.sidebar.number_input("MICE / Meeting Package (DDR)", value=30.0)

meal_map = {
    "RO": 0, "BB": rate_bb, "HB": rate_bb + rate_hb, 
    "FB": rate_bb + rate_fb, "MICE/Events": rate_bb + rate_mice
}

st.sidebar.divider()
st.sidebar.header("⚙️ Global Settings")
tax_div = st.sidebar.number_input("Tax Divisor", value=1.2327, format="%.4f")
currency = st.sidebar.selectbox("Currency", ["OMR", "USD", "AED", "THB"])

# --- ADVANCED GROUP INPUT ---
def get_enterprise_group(label):
    with st.expander(f"🏢 {label} - Strategic Input"):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("**Room Occupancy**")
            sgl = st.number_input(f"{label} SGL", value=10, step=1, key=f"{label}s")
            dbl = st.number_input(f"{label} DBL", value=20, step=1, key=f"{label}d")
            tpl = st.number_input(f"{label} TPL", value=5, step=1, key=f"{label}t")
            comp = st.number_input(f"{label} COMP Rooms", value=2, step=1, key=f"{label}cp")
        with c2:
            st.markdown("**Financials & Package**")
            adr = st.number_input(f"{label} Gross ADR", value=145.0, key=f"{label}a")
            plan = st.selectbox(f"{label} Package", ["RO", "BB", "HB", "FB", "MICE/Events"], index=4, key=f"{label}p")
            trans = st.number_input(f"{label} Transport Cost (Total)", value=100.0, key=f"{label}tr")
        with c3:
            st.markdown("**Yield Guardrails**")
            comm = st.number_input(f"{label} Comm %", value=0.10, key=f"{label}c")
            p01 = st.number_input(f"{label} Room Cost (P01)", value=10.0, key=f"{label}m")
            floor = st.number_input(f"{label} Room Profit Floor", value=85.0, key=f"{label}f")
            
    paid_r = sgl + dbl + tpl
    total_r = paid_r + comp
    pax = (sgl * 1) + (dbl * 2) + (tpl * 3)
    return paid_r, total_r, pax, adr, plan, trans, comm, p01, floor

# --- DATA ---
current_group = get_enterprise_group("Current Group Inquiry")

# --- CALCULATION ENGINE ---
def run_enterprise_audit(paid_r, total_r, pax, adr, plan, trans, comm, p01, floor):
    if total_r == 0: return None

    # 1. Total Net Revenue from Rooms (After Tax)
    total_net_rev = (adr * paid_r) / tax_div
    
    # 2. Extract F&B / Events Revenue (This is calculated separately)
    total_events_rev = meal_map[plan] * pax
    
    # 3. Surgical Room Profit (Removing F&B, Transport, Comm, and P01 for ALL rooms)
    # Note: Transport is a leakage from the Room side in this framework
    room_wealth_pre_cost = total_net_rev - total_events_rev - (trans / tax_div)
    total_room_profit = (room_wealth_pre_cost * (1 - comm)) - (p01 * total_r)
    
    unit_net_room = total_room_profit / total_r
    overall_total_wealth = total_room_profit + total_events_rev

    # Verdict Logic
    status, col = ("🔴 DILUTIVE", "red")
    if unit_net_room >= (floor + 10): status, col = ("🟢 OPTIMIZED", "green")
    elif unit_net_room >= floor: status, col = ("🟡 STABLE", "orange")
    
    return {
        "room_p": total_room_profit,
        "event_p": total_events_rev,
        "total_w": overall_total_wealth,
        "unit_r": unit_net_room,
        "stat": status,
        "col": col,
        "trans": trans,
        "comp": total_r - paid_r
    }

# --- RESULTS ---
res = run_enterprise_audit(*current_group)

if res:
    st.divider()
    st.header("📊 Surgical Audit Results")
    
    # Row 1: The Verdict
    v1, v2 = st.columns([1, 2])
    with v1:
        st.metric("Surgical Room Net", f"{currency} {res['unit_r']:.2f}")
        st.markdown(f"### Verdict: :{res['col']}[{res['stat']}]")
    with v2:
        st.info(f"**Analysis:** This segment uses **{current_group[1]}** physical keys and serves **{current_group[2]}** delegates. "
                f"Room wealth is impacted by **{res['comp']}** comp rooms and **{currency}{res['trans']}** in transport costs.")

    # Row 2: Departmental Breakdown
    st.divider()
    st.subheader("🏢 Departmental Contribution")
    d1, d2, d3 = st.columns(3)
    d1.metric("Rooms Department (Net Wealth)", f"{currency} {res['room_p']:,.2f}")
    d2.metric("F&B & Events Revenue", f"{currency} {res['event_p']:,.2f}")
    d3.metric("OVERALL GROUP PROFIT", f"{currency} {res['total_w']:,.2f}", delta="Total Net Impact")

    # Row 3: Visual Insights
    with st.expander("📝 Strategic Advice for this Group"):
        if res['col'] == "red":
            st.warning("This group is DILUTIVE. Consider reducing comp rooms or increasing the MICE package rate to balance the Room Department loss.")
        elif res['col'] == "orange":
            st.info("This group is STABLE. It is a good filler for low-occupancy periods but provides limited wealth growth.")
        else:
            st.success("This group is OPTIMIZED. This is a high-value 'Wealth Builder' for the property. Prioritize this booking!")
