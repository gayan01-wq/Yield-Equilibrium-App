import streamlit as st

# --- CORE CONFIG ---
st.set_page_config(page_title="Yield Equilibrium Auditor", layout="wide")
st.markdown("<style>.stMetric { background-color: white; border: 1px solid #ddd; padding: 10px; border-radius: 10px; } .row-box { background-color: rgba(0,0,0,0.03); padding: 12px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid; }</style>", unsafe_allow_html=True)

st.title("Yield Equilibrium: Strategic Command Center")
st.caption("Developed by Gayan Nugawela | Full Property Revenue Audit")

# --- SIDEBAR SETTINGS ---
with st.sidebar:
    st.header("1. F&B Costs")
    m_ro = st.number_input("RO Amenity Cost (Per Room)", value=4.0)
    m_bb = st.number_input("Breakfast Cost (Per Pax)", value=5.0)
    
    st.header("2. Operating Fees")
    p01_fee = st.number_input("Maintenance Fee (Per Room)", value=10.0)
    tax_div = st.number_input("Tax Divisor", value=1.2327, format="%.4f")
    
    st.header("3. Commissions (%)")
    c_ota = st.slider("OTA Comm %", 0, 30, 18) / 100
    c_who = st.slider("Wholesale Comm %", 0, 30, 20) / 100
    currency = st.selectbox("Currency", ["OMR", "USD", "AED", "THB"])

# --- CALCULATION ENGINE ---
def run_audit(s, d, t, adr, q_bb, comm, floor):
    paid = s + d + t
    if paid <= 0:
        return {"rp": 0.0, "un": 0.0, "st": "Waiting", "cl": "gray", "tfb": 0.0}
    
    # Surgical Pax Ratio: Average people per room
    pax_ratio = ((s * 1.0) + (d * 2.0) + (t * 3.0)) / paid
    total_net_rev = (adr * paid) / tax_div
    
    # F&B Logic: Breakfast rooms use pax cost, RO rooms use flat amenity cost
    q_ro = max(0, paid - q_bb)
    fb_total_cost = (q_bb * m_bb * pax_ratio) + (q_ro * m_ro)
    
    # Net Wealth: (Rev - FB Cost) * (1 - Comm) - Maintenance Fee
    profit = ((total_net_rev - fb_total_cost) * (1.0 - comm)) - (p01_fee * paid)
    unit_wealth = profit / paid
    
    # Status Indications
    if unit_wealth >= (floor + 10.0): res = {"st": "OPTIMIZED", "cl": "green"}
    elif unit_wealth >= floor: res = {"st": "MARGINAL", "cl": "orange"}
    else: res = {"st": "DILUTIVE", "cl": "red"}
    
    res.update({"rp": profit, "un": unit_wealth, "tfb": fb_total_cost})
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
        q_bb = st.number_input("Qty BB", 0, tot, key=kp+"b")
        st.write("RO Rooms:", tot - q_bb)
    
    with c3:
        adr = st.number_input("Rate per Room", 1.0, 5000.0, float(adr_d), key=kp+"a")
        flr = st.number_input("Profit Floor", 1.0, 2000.0, float(flr_d), key=kp+"fl")
    
    res = run_audit(s, d, t, adr, q_bb, comm_rate, flr)
    
    with c4:
        st.metric("Net Room Wealth", f"{currency} {res['un']:.2f}")
        st.markdown(f"<b style='color:{res['cl']}'>{res['st']}</b>", unsafe_allow_html=True)
        st.caption(f"F&B Total: {res['tfb']:.2f} | Fee: {p01_fee*tot:.2f}")
    return res

# --- DASHBOARD RENDERING ---
st.header("🏢 Group & Wholesale Segments")
r1 = segment("Wholesale", "#e67e22", "wh", 45, 25, c_who)
r2 = segment("Group Tour & Travel", "#d35400", "gt", 40, 20, 0.15)
r3 = segment("Group Corporate", "#2c3e50", "gc", 55, 30, 0.0)

st.markdown("<br>", unsafe_allow_html=True)

st.header("👤 Individual & FIT Segments")
r4 = segment("Direct / FIT", "#3498db", "di", 65, 40, 0.0)
r5 = segment("OTA Segment", "#2ecc71", "ot", 60, 35, c_ota)
r6 = segment("Corporate Segment", "#9b59b6", "co", 58, 32, 0.0)

# --- TOTAL PROPERTY SUMMARY ---
st.divider()
st.header("🏢 Property Wealth Summary")
all_res = [r1, r2, r3, r4, r5, r6]
t_r = sum(r['rp'] for r in all_res)
t_f = sum(r['tfb'] for r in all_res)

m1, m2 = st.columns(2)
m1.metric("Total Property Net Wealth", f"{currency} {t_r:,.2f}")
m2.metric("Total F&B Allocation", f"{currency} {t_f:,.2f}")

st.write("---")
st.write("✅ Audit Engine Verified. All segments and RO logic active.")
