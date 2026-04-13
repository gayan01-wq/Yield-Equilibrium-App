import streamlit as st

# --- 1. SETTINGS ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium")

# --- 2. AUTHENTICATION ---
if "auth" not in st.session_state:
    st.session_state["auth"] = False

if not st.session_state["auth"]:
    st.title("Yield Equilibrium")
    pwd = st.text_input("Access Key", type="password")
    if st.button("Unlock Dashboard"):
        if pwd == "Gayan2026":
            st.session_state["auth"] = True
            st.rerun()
        else: st.error("Invalid Key")
    st.stop()

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("Architect")
    st.write("**Gayan Nugawela**")
    st.divider()
    
    # NEW: CRISIS MODE TOGGLE
    crisis_mode = st.toggle("🚨 ACTIVATE CRISIS MODE", help="Enable during extreme market downturns to focus on Cash Flow over Profit.")
    
    h_total = st.number_input("Total Inventory Baseline", 1, 5000, 237)
    cu = st.selectbox("Currency", ["OMR", "AED", "SAR", "QAR", "EUR", "GBP", "USD", "LKR", "INR"])
    
    st.divider()
    st.write("### Statutory & Costs")
    p01 = st.number_input("P01 / Fixed Fee", 0.0, 100.0, 6.90)
    tx = st.number_input("Tax Divisor", 1.0, 2.5, 1.2327, format="%.4f")
    comm_pct = st.slider("Commission %", 0, 50, 18) / 100
    
    st.divider()
    st.write("### Operating Costs")
    m_bb, m_hb = st.number_input("BB Cost", 0.0, 500.0, 2.0), st.number_input("HB Cost", 0.0, 500.0, 8.0)
    m_fb, m_ai = st.number_input("FB Cost", 0.0, 500.0, 14.0), st.number_input("AI Cost", 0.0, 500.0, 27.0)
    m_map = {"RO": 0.0, "BB": m_bb, "HB": m_hb, "FB": m_fb, "AI": m_ai}
    
    if st.button("🔒 Logout"):
        st.session_state["auth"] = False
        st.rerun()

# --- 4. ENGINE (Crisis-Aware) ---
def calculate_wealth(rooms, adr, nights, meal_plan, commission, floor_price):
    total_rooms = sum(rooms)
    if total_rooms <= 0: return None
    
    pax_per_room = (rooms[0]*1 + rooms[1]*2 + rooms[2]*3) / total_rooms
    utilization = (total_rooms / h_total) * 100
    
    # Normal Hurdle Logic
    hurdle = floor_price * 1.25 if utilization >= 20.0 else floor_price
    
    unit_net_rev = adr / tx
    unit_meal_cost = sum((qty/total_rooms) * m_map[plan] * pax_per_room for plan, qty in meal_plan.items())
    
    # Core Wealth calculation
    unit_wealth = ((unit_net_rev - unit_meal_cost - ((unit_net_rev - unit_meal_cost) * commission)) - p01)
    
    total_wealth = unit_wealth * total_rooms * nights
    gross_total = adr * total_rooms * nights
    efficiency = (total_wealth / gross_total * 100) if gross_total > 0 else 0
    
    # --- CRISIS LOGIC ---
    if crisis_mode:
        if unit_wealth > 0:
            status, color = "CASH FLOW POSITIVE", "blue"
            note = "✅ **Crisis Accept:** Deal covers variable costs and contributes to fixed overheads. Essential for survival."
        else:
            status, color = "BLEEDING CASH", "red"
            note = "❌ **Total Loss:** This deal costs more to serve than it earns. Reject even in a crisis."
    else:
        if unit_wealth < (hurdle * 0.8) or unit_wealth <= 0:
            status, color = "DILUTIVE", "red"
            note = "🚩 **Reject:** Yield is below asset standards."
        elif unit_wealth < hurdle:
            status, color = "MARGINAL", "orange"
            note = "⚠️ **Filler:** High capacity use for low profit."
        else:
            status, color = "OPTIMIZED", "green"
            note = "💎 **Optimal:** High-efficiency wealth generator."
            
    return {"u": unit_wealth, "label": status, "color": color, "total": total_wealth, "gross": gross_total, "util": utilization, "eff": efficiency, "note": note}

# --- 5. UI SEGMENTS ---
def show_segment(title, key, d_adr, d_fl, comm):
    st.header(title)
    c1, c2, c3 = st.columns([1, 2, 1.2])
    with c1:
        s, d, t = st.number_input("SGL",0,key=key+"s"), st.number_input("DBL",0,key=key+"d"), st.number_input("TPL",0,key=key+"t")
        n = st.number_input("Nights", 1, key=key+"n")
    with c2:
        m_cols = st.columns(3)
        mix = {"RO": m_cols[0].number_input("RO",0,key=key+"ro"), "BB": m_cols[0].number_input("BB",0,key=key+"bb"),
               "HB": m_cols[1].number_input("HB",0,key=key+"hb"), "FB": m_cols[1].number_input("FB",0,key=key+"fb"),
               "AI": m_cols[2].number_input("AI",0,key=key+"ai")}
        adr_val = st.number_input("Gross ADR", 0.0, 5000.0, float(d_adr), key=key+"adr")
        floor_val = st.number_input("Market Floor", 0.0, 2000.0, float(d_fl), key=key+"fl")
        
    res = calculate_wealth([s, d, t], adr_val, n, mix, comm, floor_val)
    
    with c3:
        if res:
            st.metric("Net Unit Wealth", f"{cu} {res['u']:,.2f}")
            st.subheader(f"Status: :{res['color']}[{res['label']}]")
            st.progress(res['util'] / 100)
            st.info(res['note'])
            st.write(f"Efficiency: **{res['eff']:.1f}%**")
            st.write(f"Total Wealth: **{res['total']:,.0f}**")
    st.divider()
    return res

# --- 6. DASHBOARD ---
st.title("Yield Equilibrium")
if crisis_mode:
    st.warning("⚠️ **CRISIS MODE ACTIVE:** Analysis focused on Cash Flow & Variable Cost Recovery.")
else:
    st.caption("Strategic Decision Engine for Net Wealth Building.")

r1 = show_segment("OTA / Digital", "ota", 60, 35, comm_pct)
r2 = show_segment("Direct / FIT", "fit", 65, 40, 0.0)
r3 = show_segment("Contracted / Whl", "whl", 45, 25, 0.20)
r4 = show_segment("Groups / MICE", "grp", 55, 30, 0.0)

st.divider()
final_sum = sum(r['total'] for r in [r1, r2, r3, r4] if r)
st.metric("Total Bottom Line Contribution", f"{cu} {final_sum:,.2f}")
