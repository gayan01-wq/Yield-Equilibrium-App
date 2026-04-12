import streamlit as st

# --- BRANDING & VIBRANT UI ---
st.set_page_config(page_title="Yield Auditor", layout="wide")
st.markdown("<style>.stMetric { background-color: #ffffff; border: 2px solid #f0f2f6; padding: 15px; border-radius: 15px; } .seg-card { padding: 15px; border-radius: 12px; margin-bottom: 10px; border-left: 8px solid; color: #1e1e1e; font-weight: bold; }</style>", unsafe_allow_html=True)

st.title("🏨 Yield Equilibrium: Executive Command Center")
st.caption("Developed by Gayan Nugawela | Surgical Wealth Retention Analysis")

# --- SIDEBAR: GLOBAL SETTINGS ---
with st.sidebar:
    st.header("🍽️ Meal Net Costs")
    b = st.number_input("Breakfast", 0.0, 1000.0, 5.0)
    l = st.number_input("Lunch", 0.0, 1000.0, 7.0)
    d = st.number_input("Dinner", 0.0, 1000.0, 10.0)
    s = st.number_input("SAI Supp", 0.0, 1000.0, 8.0)
    a = st.number_input("AI Supp", 0.0, 1000.0, 15.0)
    
    meals = {"RO":0, "BB":b, "HB":b+d, "FB":b+l+d, "SAI":b+l+d+s, "AI":b+l+d+s+a}

    st.header("⚙️ Global Fees")
    p01 = st.number_input("Maint. Fee (P01)", 0.0, 500.0, 10.0)
    tax = st.number_input("Tax Divisor", 1.0, 2.0, 1.2327, format="%.4f")
    cur = st.selectbox("Currency", ["OMR", "USD", "AED", "THB"])

# --- CALCULATION ENGINE ---
def run_audit(rooms, adr, m_mix, comm_pct, floor):
    tot = sum(rooms)
    if tot <= 0: return None
    
    pax_ratio = (rooms[0]*1 + rooms[1]*2 + rooms[2]*3) / tot
    gross_net = (adr * tot) / tax
    fb_total = sum(qty * meals[p] * pax_ratio for p, qty in m_mix.items())
    
    comm_amt = (gross_net - fb_total) * comm_pct
    profit = (gross_net - fb_total - comm_amt) - (p01 * tot)
    unit = profit / tot
    
    if unit >= (floor + 15): 
        stat, col, desc = "OPTIMIZED", "#27ae60", "Strong wealth retention. Exceeding floor targets."
    elif unit >= floor: 
        stat, col, desc = "MARGINAL", "#f39c12", "Acceptable yield. Minimal wealth leakage."
    else: 
        stat, col, desc = "DILUTIVE", "#e74c3c", "Wealth leakage detected! Revise pricing/costs."
    
    return {"u":unit, "s":stat, "c":col, "d":desc, "cm":comm_amt, "fb":fb_total, "p":profit}

# --- UI COMPONENT ---
def segment(name, color, bg, kp, adr_def, floor_def, comm_pct):
    st.markdown(f"<div class='seg-card' style='background-color:{bg}; border-left-color:{color};'>{name}</div>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns([1.2, 2, 1.2, 1.5])
    
    with c1:
        s, db, t = st.number_input("SGL", 0, key=kp+"s"), st.number_input("DBL", 0, key=kp+"db"), st.number_input("TPL", 0, key=kp+"t")
    with c2:
        tot = s+db+t
        q_bb = st.number_input("BB Qty", 0, tot, key=kp+"bb")
        q_hb = st.number_input("HB Qty", 0, tot, key=kp+"hb")
        q_ai = st.number_input("AI Qty", 0, tot, key=kp+"ai")
        mix = {"BB
