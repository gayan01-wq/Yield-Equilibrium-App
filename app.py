import streamlit as st

# --- CORE CONFIG ---
st.set_page_config(page_title="Yield Equilibrium Auditor", layout="wide")
st.markdown("<style>.stMetric { background-color: white; border: 1px solid #ddd; padding: 10px; border-radius: 10px; } .row-box { background-color: rgba(0,0,0,0.03); padding: 12px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid; }</style>", unsafe_allow_html=True)

st.title("Yield Equilibrium: Strategic Command Center")
st.caption("Developed by Gayan Nugawela | Full Property Total Revenue Audit")

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
    
    # Surgical Pax Ratio (SGL=1, DBL=2, TPL=3)
    pax_ratio = ((s * 1.0) + (d * 2.0) + (t * 3.0)) / paid
    total_net_rev = (adr * paid) / tax_div
    
    # F&B Logic: Breakfast rooms use pax cost, the rest (RO) use flat amenity cost
    q_ro = max(0, paid - q_bb)
    fb_total_cost = (q_bb * m_bb * pax_ratio) + (q_ro * m_ro)
    
    # Net Wealth Calculation (Revenue minus F&B, then minus Commission and Fees)
    profit = ((total_net_rev - fb_total_cost) * (1.0 - comm)) - (p01_fee * paid)
    unit_wealth = profit / paid
    
    # Status Indications
    if unit_wealth >= (floor + 10.0):
        res = {"st": "OPTIMIZED", "cl": "green"}
    elif unit_wealth >= floor:
        res = {"st": "MARGINAL", "cl": "orange"}
    else:
        res = {"st": "DILUTIVE", "cl": "red"}
    
    res.update({"rp": profit, "un": unit_wealth, "tfb": fb_total_cost})
    return res

# --- UI SEGMENT ROW ---
def segment(label, color, kp, adr_d, flr_d, comm_rate):
    st.markdown(f"<div class='row-box' style='border-left-color: {color};'><h3>{label}</h3></div>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns([1.5, 2, 1.5, 1.5])
    
    with c1:
        s = st.number_input("SGL
