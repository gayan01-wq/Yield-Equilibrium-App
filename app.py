import streamlit as st

# --- CORE CONFIG ---
st.set_page_config(page_title="Yield Equilibrium Auditor", layout="wide")
st.markdown("<style>.stMetric { background-color: white; border: 1px solid #ddd; padding: 10px; border-radius: 10px; } .row-box { background-color: rgba(0,0,0,0.03); padding: 12px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid; }</style>", unsafe_allow_html=True)

st.title("Yield Equilibrium: Strategic Command Center")
st.caption("Developed by Gayan Nugawela | Full 6-Segment Property Audit")

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
    if paid <= 0: return {"rp": 0.0, "un": 0.0, "st": "Waiting", "cl": "gray", "tfb": 0.0}
    
    # Surgical Pax Ratio
    pax_ratio = ((s * 1.0) + (d * 2.0) + (t * 3.0)) / paid
    total_net_rev = (adr * paid) / tax_div
    
    # FB Logic: BB rooms use pax cost, everything else uses RO Amenity cost
    q_ro = max(0, paid - q_bb)
    fb_total_cost = (q_bb * m_bb * pax_ratio) + (q_ro * m_ro)
    
    # Net Wealth Calculation
    total_profit = ((total_net_rev - fb_total_cost) * (1.0 - comm)) - (p01_fee * paid)
    unit_wealth = total_profit / paid
    
    if unit_wealth >= (floor + 10.0): res = {"st": "OPTIMIZED", "cl": "green"}
    elif unit_wealth >= floor: res = {"st": "MARGINAL", "cl": "orange"}
    else: res = {"st": "DILUTIVE
