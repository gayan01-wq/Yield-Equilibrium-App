import streamlit as st

# --- 1. CONFIG ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium")

# --- 2. AUTHENTICATION ---
if "auth_key" not in st.session_state:
    st.session_state["auth_key"] = False

if not st.session_state["auth_key"]:
    st.title("Yield Equilibrium")
    st.subheader("Strategic Decision Support System")
    pwd = st.text_input("Access Key", type="password")
    if st.button("Unlock Dashboard"):
        if pwd == "Gayan2026":
            st.session_state["auth_key"] = True
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
    
    h_total = st.number_input("Total Inventory Baseline", 1, 5000, 237)
    
    curr_list = sorted([
        "OMR", "AED", "SAR", "QAR", "BHD", "KWD", 
        "EUR", "GBP", "USD", "CHF", "LKR", "INR", "THB", "SGD"
    ])
    cu = st.selectbox("Currency", curr_list)
    
    st.divider()
    st.write("### Statutory & Costs")
    p01 = st.number_input("P01 Fixed Fee", 0.0, 100.0, 6.90)
    tx = st.number_input("Tax Divisor", 1.0, 2.5, 1.2327, format="%.4f")
    comm_pct = st.slider("OTA Commission %", 0, 50, 18) / 100
    
    st.divider()
    st.write("### Unit Operating Costs")
    m_bb = st.number_input("BB Cost", 0.0, 500.0, 2.0)
    m_hb = st.number_input("HB Cost", 0.0, 500.0, 8.0)
    m_fb = st.number_input("FB Cost", 0.0, 500.0, 14.0)
    m_ai = st.number_input("AI Cost", 0.0, 500.0, 27.0)
    m_map = {"RO": 0.0, "BB": m_bb, "HB": m_hb, "FB": m_fb, "AI": m_ai}
    
    if st.button("🔒 Logout"):
        st.session_state["auth_key"] = False
        st.rerun()

# --- 4. CALCULATION ENGINE ---
def calculate_wealth(rooms, adr, nights, mix, comm, floor):
    qty = sum(rooms)
    if qty <= 0: return None
    
    pax = (rooms[0]*1 + rooms[1]*2 + rooms[2]*3) / qty
    util = (qty / h_total) * 100
    hurdle = floor * 1.25 if util >= 20.0 else floor
    
    net_rev = adr / tx
    meals = sum((mix[p]/qty) * m_map[p] * pax for p in mix)
    unit_w = ((net_rev - meals - ((net_rev - meals) * comm)) - p01)
    
    total_w = unit_w * qty * nights
    eff = (total_w / (adr * qty * nights) * 100) if adr > 0 else 0
    
    if unit_w < (hurdle * 0.8) or unit_w <= 0:
        return {"u": unit_w, "l": "DILUTIVE", "c": "red", "t": total_w, "ut": util, "e": eff, "d": "REJECT: Zero wealth contribution."}
    elif unit_w < hurdle:
        return {"u": unit_w, "l": "MARGINAL", "c": "orange", "t": total_w, "ut": util, "e": eff, "d": "FILL ONLY: Low efficiency."}
    else:
        return {"u": unit_w, "l": "OPTIMIZED", "c": "green", "t": total_w, "ut": util, "e": eff, "d": "ACCEPT: High-efficiency wealth generator."}

# --- 5. UI SEGMENTS ---
st.title("Yield Equilibrium")
st.write(f"### Asset Audit: {h_total} Rooms Baseline")

results = []

def draw_segment(label, key, d_adr, d_fl, is_ota=False):
    st.subheader(label)
    col1, col2, col3 = st.columns([1, 1.5, 1.2])
    with col1:
        s = st.number_input("SGL", 0, key=key+"s")
        d = st.number_input("DBL", 0, key=key+"d")
        t = st.number_input("TPL", 0, key=key+"t")
        n = st.number_input("Nights", 1, key=key+"n")
    with col2:
        m_cols = st.columns(3)
        mix = {
            "RO": m_cols[0].number_input("RO", 0, key=key+"ro"),
            "BB": m_cols[0].number_input("BB", 0, key=key+"bb"),
            "HB": m_cols[1].number_input("HB", 0, key=key+"hb"),
            "FB": m_cols[1].number_input("FB", 0, key=key+"fb"),
            "AI": m_cols[2].number_input("AI", 0, key=key+"ai")
        }
        adr = st.number_input("Gross ADR", 0.0, 5000.0, d_adr, key=key+"adr")
        fl = st.number_input("Market Floor", 0.0, 5000.0, d_fl, key=key+"fl")
    
    res = calculate_wealth([s,d,t], adr, n, mix, (comm_pct if is_ota else 0.0), fl)
    results.append(res)
    
    with col3:
        if res:
            st.metric("Net Wealth / Room", f"{cu} {res['u']:,.2f}")
            st.markdown(f"### Status: :{res['c']}[{res['l']}]")
            st.write(f"**Directive:** {res['d']}")
            st.write(f"Utilization: {res['ut']:.1f}% | Efficiency: {res['e']:.1f}%")
            st.write(f"Segment Wealth: **{res['t']:,.0f}**")
        else:
            st.info("Input inventory")
    st.divider()

draw_segment("1. OTA / Digital Channels", "ota", 60.0, 35.0, is_ota=True)
draw_segment("2. Direct / FIT Portfolio", "fit", 65.0, 40.0)
draw_segment("3. Contracted / Wholesale", "whl", 45.0, 25.0)
draw_segment("4. Groups / MICE Business", "grp", 55.0, 30.0)

# --- 6. FOOTER ---
final_w = sum(r['t'] for r in results if r)
st.markdown(f"""
    <div style="background-color:#2c3e50; padding:30px; border-radius:15px; text-align:center;">
        <h2 style="color:white; margin:0;">Total Portfolio Bottom Line</h2>
        <h1 style="color:#27ae60; margin:0; font-size:3.5rem;">{cu} {final_w:,.2f}</h1>
    </div>
""", unsafe_allow_html=True)

st.divider()
st.header("The 03 Pillars of Yield Equilibrium")
p1, p2, p3 = st.columns(3)
p1.info("**1. Wealth Stripping:** Isolating net liquidity by removing taxes, commissions, and variable costs.")
p2.warning("**2. Capacity Sensitivity:** Raising yield requirements as occupancy hits >20% to prevent FIT displacement.")
p3.success("**3. Efficiency Indexing:** Measuring the % of gross revenue that reaches the bank as pure profit.")
