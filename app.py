import streamlit as st

# --- BRANDING ---
st.set_page_config(page_title="Yield Equilibrium Auditor", layout="wide")
st.markdown("<style>.stMetric { background-color: white; border: 1px solid #ddd; padding: 10px; border-radius: 10px; } .row-box { background-color: rgba(0,0,0,0.03); padding: 12px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid; }</style>", unsafe_allow_html=True)

st.title("Yield Equilibrium: Total Revenue Command Center")
st.caption("Developed by Gayan Nugawela | Full Meal Plan Allocation Logic")

# --- SIDEBAR SETTINGS ---
with st.sidebar:
    st.header("1. Meal Plan Net Costs")
    c_bb, c_lh, c_dr = st.number_input("Breakfast", 5.0), st.number_input("Lunch", 7.0), st.number_input("Dinner", 10.0)
    c_sai, c_ai = st.number_input("SAI Supplement", 8.0), st.number_input("AI Supplement", 15.0)
    
    meals = {
        "RO": 0.0, "BB": c_bb, "HB": c_bb + c_dr, "FB": c_bb + c_lh + c_dr,
        "SAI": c_bb + c_lh + c_dr + c_sai, "AI": c_bb + c_lh + c_dr + c_sai + c_ai
    }

    st.header("2. Fees")
    p01 = st.number_input("Maintenance (Per Room)", 10.0)
    tax = st.number_input("Tax Divisor", 1.2327, format="%.4f")
    cur = st.selectbox("Currency", ["OMR", "USD", "AED", "THB"])

# --- ENGINE ---
def audit(s, d, t, adr, counts, comm, floor):
    paid = s + d + t
    if paid <= 0: return {"rp": 0, "un": 0, "st": "ENTER ROOMS", "cl": "gray", "tfb": 0}
    
    pax = ((s * 1.0) + (d * 2.0) + (t * 3.0)) / paid
    net_rev = (adr * paid) / tax
    fb_cost = sum(qty * meals[plan] * pax for plan, qty in counts.items())
    
    prof = ((net_rev - fb_cost) * (1.0 - comm)) - (p01 * paid)
    unit = prof / paid
    
    if unit >= (floor + 10): res = {"st": "OPTIMIZED", "cl": "green"}
    elif unit >= floor: res = {"st": "MARGINAL", "cl": "orange"}
    else: res = {"st": "DILUTIVE", "cl": "red"}
    
    res.update({"rp": prof, "un": unit, "tfb": fb_cost})
    return res

# --- UI ROW ---
def segment(label, color, kp, adr_d, flr_d, comm):
    st.markdown(f"<div class='row-box' style='border-left-color: {color};'><h3>{label}</h3></div>", unsafe_allow_html=True)
    c1, c2, c3, c4
