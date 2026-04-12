import streamlit as st

# --- CORE CONFIG ---
st.set_page_config(page_title="Yield Equilibrium Auditor", layout="wide")
st.markdown("<style>.stMetric { background-color: white; border: 1px solid #ddd; padding: 10px; border-radius: 10px; } .row-box { background-color: rgba(0,0,0,0.03); padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid; }</style>", unsafe_allow_html=True)

st.title("🏨 Yield Equilibrium: Strategic Command Center")
st.caption("Developed by Gayan Nugawela | Director-Level Property Audit")

# --- SIDEBAR SETTINGS ---
with st.sidebar:
    st.header("🍽️ F&B Net Costs")
    m_bb, m_lh, m_dr = st.number_input("Breakfast", 5.0), st.number_input("Lunch", 7.0), st.number_input("Dinner", 10.0)
    m_sai, m_ai = st.number_input("SAI", 8.0), st.number_input("AI", 15.0)
    tax_div = st.number_input("Tax Divisor", 1.2327, format="%.4f")
    currency = st.selectbox("Currency", ["OMR", "USD", "AED", "THB"])

meal_map = {"RO": 0, "BB": m_bb, "HB": m_bb+m_dr, "FB": m_bb+m_lh+m_dr, "SAI": m_bb+m_lh+m_dr+m_sai, "AI": m_bb+m_lh+m_dr+m_sai+m_ai}

# --- ENGINE ---
def run_audit(s, d, t, adr, counts, comm, p01, floor):
    paid = s + d + t
    if paid <= 0: return {"rp": 0, "fp": 0, "un": 0, "st": "Waiting...", "cl": "gray", "df": "Enter inventory."}
    
    pax_ratio = ((s*1) + (d*2) + (t*3)) / paid
    net_rev = (adr * paid) / tax_div
    fb_rev = sum(qty * meal_map[pl] * pax_ratio for pl, qty in counts.items())
    
    profit = ((net_rev - fb_rev) * (1 - comm)) - (p01 * paid)
    unit = profit / paid
    
    if unit >= (floor + 10): res = {"st": "🟢 OPTIMIZED", "cl": "green", "df": "Strong wealth retention."}
    elif unit >= floor: res = {"st": "🟡 MARGINAL", "cl": "orange", "
