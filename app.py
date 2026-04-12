import streamlit as st

# --- CORE CONFIG ---
st.set_page_config(page_title="Yield Equilibrium Auditor", layout="wide")
st.markdown("<style>.stMetric { background-color: white; border: 1px solid #ddd; padding: 10px; border-radius: 10px; } .row-box { background-color: rgba(0,0,0,0.03); padding: 12px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid; }</style>", unsafe_allow_html=True)

st.title("Yield Equilibrium: Strategic Command Center")
st.caption("Developed by Gayan Nugawela | Surgical F&B and Fee Transparency")

# --- SIDEBAR SETTINGS ---
with st.sidebar:
    st.header("1. F&B Costs (Per Room)")
    m_ro = st.number_input("RO Amenities Cost", value=4.0)
    m_bb = st.number_input("Breakfast Cost (Per Pax)", value=5.0)
    
    st.header("2. Operating Fees")
    p01_fee = st.number_input("Maintenance Fee (Per Room)", value=10.0)
    tax_div = st.number_input("Tax Divisor", value=1.2327, format="%.4f")
    
    st.header("3. Commissions (%)")
    c_ota = st.slider("OTA Comm %", 0, 30, 18) / 100
    c_who = st.slider("Wholesale Comm %", 0, 30, 20) / 100
    currency = st.selectbox("Currency", ["OMR", "USD", "AED", "THB"])

# --- CALCULATION ENGINE ---
def run_audit(s, d, t, adr, counts, comm, floor):
    paid = s + d + t
    if paid <= 0: return {"rp": 0.0, "un": 0.0, "st": "Waiting", "cl": "gray", "tfb": 0.0}
    
    # Surgical Pax Ratio
    pax_ratio = ((s * 1.0) + (d * 2.0) + (t * 3.0)) / paid
    total_net_rev = (adr * paid) / tax_div
    
    # FB Logic: RO gets the flat amenity cost, BB gets the per-pax cost
    fb_ro = counts["RO"] * m_ro
    fb_bb = counts["BB"] * (m_bb * pax_ratio)
    total_fb_cost = fb_ro + fb_bb
    
    # Net Wealth Calculation
    total_profit = ((total_net_rev - total_fb_cost) * (1.0 - comm)) - (p01_fee * paid)
    unit_wealth = total_profit / paid
    
    if unit_wealth >= (floor + 10.0): res = {"st": "OPTIMIZED", "cl": "green"}
    elif unit_wealth >= floor: res = {"st": "MARGINAL", "cl": "orange"}
    else: res = {"st": "DILUTIVE", "cl": "red"}
    
    res.update({"rp": total_profit, "un": unit_wealth, "tfb": total_fb_cost})
    return res

# --- UI SEGMENT ROW ---
def segment(label, color, kp, adr_d, flr_d, comm_rate):
    st.markdown(f"<div class='row-box' style='border-left-color: {color};'><h3>{label}</h3></div>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns([1.5, 2, 1.5, 1.5])
    
    with c1:
        s = st.number_input("SGL Rooms", 0, key=kp+"s")
        d = st.number_input("DBL Rooms", 0, key=kp+"d")
        t = st.number_input("TPL Rooms", 0, key=kp+"t")
    
    with c2:
        tot = s + d + t
        q_bb = st.number_input("BB Qty", 0, tot, key=kp+"b")
        # Every room not BB is considered RO
        q_ro = tot - q_bb
        st.write(f"RO Rooms: {q_ro}")
        counts = {"BB": q_bb, "RO": q_ro}
    
    with c3:
        adr = st.number_input("Rate per Room", 1.0, 5000.0, float(adr_d), key=kp+"a")
        flr = st.number_input("Profit Floor", 1.0, 2000.0, float(flr_d), key=kp+"fl")
    
    res = run_audit(s, d, t, adr, counts, comm_rate, flr)
    
    with c4:
        st.metric("Net Room Wealth", f"{currency} {res['un']:.2f}")
        st.markdown(f"<b style='color:{res['cl']}'>{res['st']}</b>", unsafe_allow_html=True)
        st.caption(f"F&B Total: {res['tfb']:.2f} | Fee: {p01_fee*tot}")
    return res

# --- DASHBOARD ---
st.header("Groups & Wholesale")
r1 = segment("Wholesale", "#e67e22", "wh", 45, 25, c_who)
r2 = segment("Group Corporate", "#2c3e50", "gc", 55, 30, 0.0)

st.header("Individual & FIT")
r3 = segment("Direct / FIT", "#3498db", "di", 65, 40, 0.0)
r4 = segment("OTA Segment", "#2ecc71", "ot", 60, 35, c_ota)

# --- PROPERTY SUMMARY ---
st.divider()
all_res = [r1, r2, r3, r4]
t_r = sum(r['rp'] for r in all_res)
t_f = sum(r['tfb'] for r in all_res)

m1, m2 = st.columns(2)
m1.metric("Total Property Net Wealth", f"{currency} {t_r:,.2f}")
m2.metric("Total F&B / Amenity Allocation", f"{currency} {t_f:,.2f}")
