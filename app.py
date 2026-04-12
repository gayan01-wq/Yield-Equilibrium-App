import streamlit as st

# --- BRANDING & VIBRANT UI ---
st.set_page_config(page_title="Yield Equilibrium Auditor", layout="wide")
st.markdown("""
<style>
    .stMetric { background-color: #ffffff; border: 2px solid #f0f2f6; padding: 15px; border-radius: 15px; box-shadow: 2px 2px 10px rgba(0,0,0,0.05); }
    .seg-card { padding: 20px; border-radius: 15px; margin-bottom: 20px; border-left: 10px solid; color: #1e1e1e; }
    .desc-box { font-size: 0.85rem; margin-top: 10px; padding: 8px; border-radius: 5px; background: rgba(255,255,255,0.5); }
</style>
""", unsafe_allow_html=True)

st.title("🏨 Yield Equilibrium: Executive Command Center")
st.caption("Developed by Gayan Nugawela | Surgical Wealth Retention Analysis")

# --- SIDEBAR: GLOBAL SETTINGS ---
with st.sidebar:
    st.header("🍽️ Meal Net Costs")
    # UNLOCKED: Range 0 to 1000
    b = st.number_input("Breakfast", 0.0, 1000.0, 5.0)
    l = st.number_input("Lunch", 0.0, 1000.0, 7.0)
    d = st.number_input("Dinner", 0.0, 1000.0, 10.0)
    s = st.number_input("SAI Supplement", 0.0, 1000.0, 8.0)
    a = st.number_input("AI Supplement", 0.0, 1000.0, 15.0)
    
    meals = {"RO":0, "BB":b, "HB":b+d, "FB":b+l+d, "SAI":b+l+d+s, "AI":b+l+d+s+a}

    st.header("⚙️ Global Fees")
    p01 = st.number_input("Maint. Fee (P01)", 0.0, 500.0, 10.0)
    tax = st.number_input("Tax Divisor", 1.0, 2.0, 1.2327, format="%.4f")
    cur = st.selectbox("Currency", ["OMR", "USD", "AED", "THB"])

# --- ENGINE ---
def run_audit(rooms, adr, m_mix, comm_pct, floor):
    tot = sum(rooms)
    if tot <= 0: return None
    
    pax_ratio = (rooms[0]*1 + rooms[1]*2 + rooms[2]*3) / tot
    gross_net = (adr * tot) / tax
    fb_total = sum(qty * meals[p] * pax_ratio for p, qty in m_mix.items())
    
    comm_amt = (gross_net - fb_total) * comm_pct
    maint_total = p01 * tot
    profit = (gross_net - fb_total - comm_amt) - maint_total
    unit = profit / tot
    
    if unit >= (floor + 15): 
        stat, col, desc = "OPTIMIZED", "#27ae60", "Strong wealth retention. Exceeding floor targets."
    elif unit >= floor: 
        stat, col, desc = "MARGINAL", "#f39c12", "Acceptable yield. Minimal wealth leakage detected."
    else: 
        stat, col, desc = "DILUTIVE", "#e74c3c", "Wealth leakage! Revise pricing or reduce costs."
    
    return {"p":profit, "u":unit, "s":stat, "c":col, "d":desc, "cm":comm_amt, "fb":fb_total}

# --- UI COMPONENT ---
def segment(name, color, bg, kp, adr_def, floor_def, comm_pct):
    st.markdown(f"<div class='seg-card' style='background-color:{bg}; border-left-color:{color};'><h2>{name}</h2></div>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns([1.2, 2, 1.2, 1.5])
    
    with c1:
        s, db, t = st.number_input("SGL", 0, key=kp+"s"), st.number_input("DBL", 0, key=kp+"db"), st.number_input("TPL", 0, key=kp+"t")
    with c2:
        tot = s+db+t
        q_bb = st.number_input("BB Qty", 0, tot, key=kp+"bb")
        q_hb = st.number_input("HB Qty", 0, tot, key=kp+"hb")
        q_ai = st.number_input("AI Qty", 0, tot, key=kp+"ai")
        mix = {"BB":q_bb, "HB":q_hb, "AI":q_ai, "RO":max(0, tot-(q_bb+q_hb+q_ai))}
    with c3:
        adr = st.number_input("ADR", 0.0, 5000.0, float(adr_def), key=kp+"a")
        flr = st.number_input("Floor", 0.0, 2000.0, float(floor_def), key=kp+"f")
    
    res = run_audit([s,db,t], adr, mix, comm_pct, flr)
    with c4:
        if res:
            st.metric("Net Wealth / Room", f"{cur} {res['u']:.2f}")
            st.markdown(f"<b style='color:{res['c']}'>{res['s']}</b>", unsafe_allow_html=True)
            st.markdown(f"<div class='desc-box'>{res['d']}</div>", unsafe_allow_html=True)
            st.caption(f"Comm: {res['cm']:.2f} | F&B: {res['fb']:.2f}")
        else:
            st.info("Enter rooms to audit.")
    return res

# --- DASHBOARD RENDER ---
r1 = segment("✈️ Wholesale", "#e67e22", "#fff3e0", "wh", 45, 25, 0.20)
r2 = segment("🌍 Group Tour", "#d354
