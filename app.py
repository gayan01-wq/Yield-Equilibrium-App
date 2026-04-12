import streamlit as st

# --- CORE CONFIG ---
st.set_page_config(page_title="Yield Equilibrium Auditor", layout="wide")
st.markdown("<style>.stMetric { background-color: white; border: 1px solid #ddd; padding: 10px; border-radius: 10px; } .row-box { background-color: rgba(0,0,0,0.03); padding: 12px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid; }</style>", unsafe_allow_html=True)

st.title("Yield Equilibrium: Full Property Command Center")
st.caption("Developed by Gayan Nugawela | Total Revenue Strategy")

# --- SIDEBAR SETTINGS ---
with st.sidebar:
    st.header("FB Net Costs")
    m_bb = st.number_input("Breakfast", value=5.0)
    m_lh = st.number_input("Lunch", value=7.0)
    m_dr = st.number_input("Dinner", value=10.0)
    m_sai = st.number_input("SAI", value=8.0)
    m_ai = st.number_input("AI", value=15.0)
    st.divider()
    tax_div = st.number_input("Tax Divisor", value=1.2327, format="%.4f")
    currency = st.selectbox("Currency", ["OMR", "USD", "AED", "THB"])

meal_map = {"RO": 0, "BB": m_bb, "HB": m_bb+m_dr, "FB": m_bb+m_lh+m_dr, "SAI": m_bb+m_lh+m_dr+m_sai, "AI": m_bb+m_lh+m_dr+m_sai+m_ai}

# --- CALCULATION ENGINE ---
def run_audit(s, d, t, adr, counts, comm, floor):
    paid = s + d + t
    if paid <= 0: return {"rp": 0.0, "fp": 0.0, "un": 0.0, "st": "Waiting", "cl": "gray"}
    
    # Surgical Pax Ratio
    pax_ratio = ((s * 1.0) + (d * 2.0) + (t * 3.0)) / paid
    net_rev = (adr * paid) / tax_div
    fb_rev = sum(qty * meal_map[pl] * pax_ratio for pl, qty in counts.items())
    
    # Net Wealth (Revenue minus FB, Commission, and P01 overhead)
    profit = ((net_rev - fb_rev) * (1.0 - comm)) - (10.0 * paid)
    unit = profit / paid
    
    # FIXED FLOOR LOGIC: Immediate Dilutive Trigger
    if unit >= (floor + 15.0): res = {"st": "OPTIMIZED", "cl": "green"}
    elif unit >= floor: res = {"st": "MARGINAL", "cl": "orange"}
    else: res = {"st": "DILUTIVE", "cl": "red"}
    
    res.update({"rp": profit, "fp": fb_rev, "un": unit})
    return res

# --- UI SEGMENT ROW ---
def segment(label, color, kp, adr_d, flr_d, comm):
    st.markdown(f"<div class='row-box' style='border-left-color: {color};'><h3>{label}</h3></div>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns([1.5, 2, 1.5, 1.5])
    
    with c1:
        s = st.number_input("SGL Rooms", 0, key=kp+"s")
        d = st.number_input("DBL Rooms", 0, key=kp+"d")
        t = st.number_input("TPL Rooms", 0, key=kp+"t")
    
    with c2:
        tot = s + d + t
        q_bb = st.number_input("BB Qty", 0, tot, key=kp+"b")
        q_hb = st.number_input("HB Qty", 0, tot, key=kp+"h")
        q_fb = st.number_input("FB Qty", 0, tot, key=kp+"f")
        counts = {"BB": q_bb, "HB": q_hb, "FB": q_fb, "RO": max(0, tot-(q_bb+q_hb+q_fb)), "SAI": 0, "AI": 0}
    
    with c3:
        adr = st.number_input("Gross ADR", 1.0, 5000.0, float(adr_d), key=kp+"a")
        flr = st.number_input("Profit Floor", 1.0, 2000.0, float(flr_d), key=kp+"fl")
    
    res = run_audit(s, d, t, adr, counts, comm, flr)
    
    with c4:
        st.metric("Net Room Wealth", f"{currency} {res['un']:.2f}")
        st.markdown(f"<b style='color:{res['cl']}'>{res['st']}</b>", unsafe_allow_html=True)
    return res

# --- DASHBOARD RENDER ---
st.header("Groups & Wholesale")
r1 = segment("Wholesale", "#e67e22", "wh", 130, 75, 0.20)
r2 = segment("Group Tour & Travels", "#d35400", "gt", 140, 80, 0.15)
r3 = segment("Group Corporate", "#2c3e50", "gc", 150, 85, 0.0)

st.header("Individual & FIT")
r4 = segment("Direct / FIT", "#3498db", "di", 200, 110, 0.0)
r5 = segment("OTA Segment", "#2ecc71", "ot", 190, 100, 0.18)
r6 = segment("Corporate Segment", "#9b59b6", "co", 160, 95, 0.0)

# --- PROPERTY SUMMARY ---
st.divider()
all_res = [r1, r2, r3, r4, r5, r6]
t_r = sum(r['rp'] for r in all_res)
t_f = sum(r['fp'] for r in all_res)

m1, m2, m3 = st.columns(3)
m1.metric("Total Room Wealth", f"{currency} {t_r:,.2f}")
m2.metric("Total FB Allocation", f"{currency} {t_f:,.2f}")
m3.metric("Combined Property Wealth", f"{currency} {(t_r + t_f):,.2f}")

st.write("✅ Audit System Ready - All Segments Active")
