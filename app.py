import streamlit as st

# --- CORE CONFIG ---
st.set_page_config(page_title="Yield Equilibrium Auditor", layout="wide")
st.markdown("<style>.stMetric { background-color: white; border: 1px solid #ddd; padding: 10px; border-radius: 10px; } .row-box { background-color: rgba(0,0,0,0.03); padding: 12px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid; }</style>", unsafe_allow_html=True)

st.title("Yield Equilibrium: Command Center")
st.caption("Developed by Gayan Nugawela | Strategic Property Audit")

# --- SIDEBAR ---
with st.sidebar:
    st.header("FB Net Costs")
    m_bb, m_lh, m_dr = st.number_input("Breakfast", 5.0), st.number_input("Lunch", 7.0), st.number_input("Dinner", 10.0)
    m_sai, m_ai = st.number_input("SAI", 8.0), st.number_input("AI", 15.0)
    tax_div = st.number_input("Tax Divisor", 1.2327, format="%.4f")
    currency = st.selectbox("Currency", ["OMR", "USD", "AED", "THB"])

meal_map = {"RO": 0, "BB": m_bb, "HB": m_bb+m_dr, "FB": m_bb+m_lh+m_dr, "SAI": m_bb+m_lh+m_dr+m_sai, "AI": m_bb+m_lh+m_dr+m_sai+m_ai}

# --- ENGINE ---
def run_audit(s, d, t, adr, counts, comm, floor):
    paid = s + d + t
    if paid <= 0: return {"rp": 0, "fp": 0, "un": 0, "st": "Waiting", "cl": "gray"}
    pax_ratio = ((s*1.0) + (d*2.0) + (t*3.0)) / paid
    net_rev = (adr * paid) / tax_div
    fb_rev = sum(qty * meal_map[pl] * pax_ratio for pl, qty in counts.items())
    profit = ((net_rev - fb_rev) * (1.0 - comm)) - (10.0 * paid)
    unit = profit / paid
    if unit >= (floor + 10): res = {"st": "OPTIMIZED", "cl": "green"}
    elif unit >= floor: res = {"st": "MARGINAL", "cl": "orange"}
    else: res = {"st": "DILUTIVE", "cl": "red"}
    res.update({"rp": profit, "fp": fb_rev, "un": unit})
    return res

# --- UI ROW ---
def segment(icon, label, color, kp, adr_d, flr_d, comm):
    st.markdown(f"<div class='row-box' style='border-left-color: {color};'><h3>{icon} {label}</h3></div>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns([1.5, 2, 1.5, 1.5])
    with c1:
        s, d, t = st.number_input("SGL", 0, key=kp+"s"), st.number_input("DBL", 0, key=kp+"d"), st.number_input("TPL", 0, key=kp+"t")
    with c2:
        tot = s+d+t
        q_bb, q_hb, q_fb = st.number_input("BB Qty", 0, tot, key=kp+"b"), st.number_input("HB Qty", 0, tot, key=kp+"h"), st.number_input("FB Qty", 0, tot, key=kp+"f")
        counts = {"BB": q_bb, "HB": q_hb, "FB": q_fb, "RO": max(0, tot-(q_bb+q_hb+q_fb)), "SAI": 0, "AI": 0}
    with c3:
        adr = st.number_input("ADR", 1.0, 5000.0, float(adr_d), key=kp+"a")
        flr = st.number_input("Floor", 1.0, 2000.0, float(flr_d), key=kp+"fl")
    res = run_audit(s, d, t, adr, counts, comm, flr)
    with c4:
        st.metric("Net Profit", f"{currency} {res['un']:.2f}")
        st.markdown(f"<b style='color:{res['cl']}'>{res['st']}</b>", unsafe_allow_html=True)
    return res

# --- RENDER ---
st.header("Groups & Wholesale")
r1 = segment("A", "Wholesale", "#e67e22", "wh", 130, 75, 0.20)
r2 = segment("B", "MICE
