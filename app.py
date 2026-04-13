import streamlit as st

# --- 1. SETTINGS ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium")

# --- 2. AUTHENTICATION ---
if "auth" not in st.session_state:
    st.session_state["auth"] = False

if not st.session_state["auth"]:
    st.title("Yield Equilibrium")
    st.subheader("Strategic Decision Support System")
    pwd = st.text_input("Access Key", type="password")
    if st.button("Unlock Dashboard"):
        if pwd == "Gayan2026":
            st.session_state["auth"] = True
            st.rerun()
        else:
            st.error("Invalid Key")
    st.stop()

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("Architect")
    st.write("**Gayan Nugawela**")
    st.caption("Revenue management specialist- SME")
    st.divider()
    
    h_name = st.text_input("Hotel Name", "Wyndham Garden Salalah")
    h_total = st.number_input("Total Inventory", 1, 1000, 158)
    cu = st.selectbox("Currency", ["OMR", "AED", "SAR", "QAR", "EUR", "GBP", "USD", "LKR", "INR"])
    
    st.divider()
    st.write("### Statutory & Costs")
    p01 = st.number_input("P01 Fee", 0.0, 100.0, 6.90)
    tx = st.number_input("Tax Divisor", 1.0, 2.5, 1.2327, format="%.4f")
    comm_pct = st.slider("OTA Commission %", 0, 50, 18) / 100
    
    st.divider()
    st.write("### Meal Costs")
    m_bb = st.number_input("BB", 0.0, 500.0, 2.0)
    m_hb = st.number_input("HB", 0.0, 500.0, 8.0)
    m_fb = st.number_input("FB", 0.0, 500.0, 14.0)
    m_sai = st.number_input("SAI", 0.0, 500.0, 22.0)
    m_ai = st.number_input("AI", 0.0, 500.0, 27.0)
    
    m_map = {"RO": 0.0, "BB": m_bb, "HB": m_hb, "FB": m_fb, "SAI": m_sai, "AI": m_ai}
    
    if st.button("🔒 Logout"):
        st.session_state["auth"] = False
        st.rerun()

# --- 4. ENGINE ---
def calculate_wealth(rooms, adr, nights, meal_plan, commission, floor_price, event_rev=0):
    total_rooms = sum(rooms)
    if total_rooms <= 0: return None
    
    pax_count = (rooms[0]*1 + rooms[1]*2 + rooms[2]*3)
    occ_percent = (total_rooms / h_total) * 100
    
    hurdle = floor_price * 1.25 if occ_percent >= 50.0 else floor_price
    if nights >= 5: hurdle *= 0.90
    
    gross_total = adr * total_rooms * nights
    net_revenue = (adr * total_rooms) / tx
    meals_total = sum(v * m_map[k] * (pax_count / total_rooms) for k, v in meal_plan.items())
    
    wealth_per_room = ((net_revenue - meals_total - ((net_revenue - meals_total) * commission)) - (p01 * total_rooms)) + ((event_rev * pax_count) / tx / total_rooms)
    total_wealth = wealth_per_room * total_rooms * nights
    unit_wealth = total_wealth / (total_rooms * nights)
    
    status, color = ("OPTIMIZED", "green")
    if unit_wealth < (hurdle * 0.8) or total_wealth <= 0: status, color = ("DILUTIVE", "red")
    elif unit_wealth < hurdle: status, color = ("MARGINAL", "orange")
        
    return {"u": unit_wealth, "label": status, "color": color, "total": total_wealth, "gross": gross_total, "qty": total_rooms, "impact": occ_percent}

# --- 5. UI SEGMENTS ---
def show_segment(title, key, start_adr, start_fl, comm_val, is_group=False):
    st.header(title)
    col1, col2, col3 = st.columns([1, 2, 1.2])
    
    # INDENTATION FIXED BELOW
    with col1:
        st.write("**Inventory**")
        s = st.number_input("SGL", 0, key=key+"s")
        d = st.number_input("DBL", 0, key=key+"d")
        t = st.number_input("TPL", 0, key=key+"t")
        n = st.number_input("Nights", 1, key=key+"n")
        
    with col2:
        st.write("**Meal Mix & Price**")
        m_cols = st.columns(3)
        meal_mix = {
            "RO": m_cols[0].number_input("RO", 0, key=key+"ro"),
            "BB": m_cols[0].number_input("BB", 0, key=key+"bb"),
            "HB": m_cols[1].number_input("HB", 0, key=key+"hb"),
            "FB": m_cols[1].number_input("FB", 0, key=key+"fb"),
            "SAI": m_cols[2].number_input("SAI", 0, key=key+"sai"),
            "AI": m_cols[2].number_input("AI", 0, key=key+"ai")
        }
        st.write("---")
        adr_val = st.number_input("Gross ADR", 0.0, 5000.0, float(start_adr), key=key+"adr")
        floor_val = st.number_input("Market Floor", 0.0, 2000.0, float(start_fl), key=key+"fl")
        ev_val = st.number_input("Event Revenue /Pax", 0.0, key=key+"ev") if is_group else 0
        
    res = calculate_wealth([s, d, t], adr_val, n, meal_mix, comm_val, floor_val, ev_val)
    
    with col3:
        st.write("**Strategy Result**")
        if res:
            st.metric("Net Wealth / Room", f"{cu} {res['u']:,.2f}")
            st.subheader(f"Status: :{res['color']}[{res['label']}]")
            efficiency = (res['total'] / res['gross'] * 100) if res['gross'] > 0 else 0
            
            if res['label'] == "DILUTIVE":
                note = f"🚩 Reject: Efficiency is only {efficiency:.1f}%. Margin is too low."
            elif res['label'] == "MARGINAL":
                note = f"⚠️ Filler: {efficiency:.1f}% efficiency. SCALE improves wealth, but FIT is better."
            else:
                note = f"💎 Priority: {efficiency:.1f}% efficiency. This builds genuine asset wealth."
            
            st.info(note)
            if res['impact'] >= 50: st.warning(f"DOMINANCE RISK: {res['impact']:.1f}%")
            st.write(f"Total Wealth: **{res['total']:,.0f}**")
            st.write(f"Wealth Efficiency: **{efficiency:.1f}%**")
        else:
            st.info("Enter inventory to calculate.")
    st.divider()
    return res

# --- 6. MAIN DASHBOARD ---
st.title("Yield Equilibrium")
st.write(f"### Portfolio Audit: {h_name}")

r1 = show_segment("OTA Segment", "ota", 60, 35, comm_pct)
r2 = show_segment("Direct / FIT", "fit", 65, 40, 0.0)
r3 = show_segment("Wholesale", "whl", 45, 25, 0.20)
r4 = show_segment("MICE & Groups", "grp", 55, 30, 0.0, is_group=True)

# Final Portfolio Total
final_sum = sum(r['total'] for r in [r1, r2, r3, r4] if r)
st.metric(f"Total Portfolio Net Wealth ({cu})", f"{final_sum:,.0f}")

st.divider()
st.write("### The 03 Pillars of Yield Equilibrium")
p_cols = st.columns(3)
p_cols[0].info("**1. Wealth Stripping:** Net liquidity isolation.")
p_cols[1].info("**2. Friction Indexing:** Overhead loss measurement.")
p_cols[2].info("**3. Displacement:** Yield protection.")
