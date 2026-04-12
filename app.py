import streamlit as st

# --- STYLE ---
st.set_page_config(page_title="Yield Auditor", layout="wide")
st.markdown("<style>.stMetric { background-color: #ffffff; border: 2px solid #f0f2f6; padding: 10px; border-radius: 12px; } .card { padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 10px solid; font-weight: bold; }</style>", unsafe_allow_html=True)

st.title("🏨 Yield Equilibrium: Total Revenue Center")
st.caption("Developed by Gayan Nugawela | Certified Formula Verification")

# --- SIDEBAR ---
with st.sidebar:
    st.header("🍽️ Meal Costs (0-1000)")
    b, l, d = st.number_input("BB", 0.0, 1000.0, 5.0), st.number_input("LN", 0.0, 1000.0, 7.0), st.number_input("DN", 0.0, 1000.0, 10.0)
    s, a = st.number_input("SAI", 0.0, 1000.0, 8.0), st.number_input("AI", 0.0, 1000.0, 15.0)
    
    meals = {"RO":0, "BB":b, "HB":b+d, "FB":b+l+d, "SAI":b+l+d+s, "AI":b+l+d+s+a}
    
    st.header("⚙️ Fees")
    p01, tax = st.number_input("P01 Fee (Maint)", 10.0), st.number_input("Tax Divisor", 1.2327, format="%.4f")
    cur = st.selectbox("Currency", ["OMR", "USD", "AED", "THB"])

# --- FORMULA ENGINE ---
def run_audit(rooms, adr, mix, cp, floor_target):
    tot = sum(rooms)
    if tot <= 0: return None
    
    # 1. Calculate Average Pax per Room
    pax = (rooms[0]*1 + rooms[1]*2 + rooms[2]*3) / tot
    
    # 2. Convert Gross ADR to Net Revenue
    net_rev_total = (adr * tot) / tax
    
    # 3. Calculate Total F&B Cost
    fb_total = sum(qty * meals[p] * pax for p, qty in mix.items())
    
    # 4. Apply Commission to (Revenue minus F&B)
    commission_amt = (net_rev_total - fb_total) * cp
    
    # 5. Final Wealth Calculation
    total_profit = (net_rev_total - fb_total - commission_amt) - (p01 * tot)
    wealth_per_room = total_profit / tot
    
    # 6. Floor Sensitivity Check
    if wealth_per_room >= (floor_target + 15):
        st_label, st_col, st_desc = "OPTIMIZED", "#27ae60", "Strong Wealth Retention."
    elif wealth_per_room >= floor_target:
        st_label, st_col, st_desc = "MARGINAL", "#f39c12", "Minimal Wealth Leakage."
    else:
        st_label, st_col, st_desc = "DILUTIVE", "#e74c3c", "Wealth Leakage Detected!"
        
    return {"u":wealth_per_room, "s":st_label, "c":st_col, "d":st_desc, "cm":commission_amt, "fb":fb_total, "p":total_profit}

# --- UI COMPONENT ---
def segment(name, color, bg, kp, adr_d, flr_d, cp_rate):
    st.markdown(f"<div class='card' style='background:{bg}; border-left-color:{color};'>{name}</div>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns([1, 2.5, 1, 1.5])
    
    with c1:
        s, db, t = st.number_input("SGL",0,key=kp+"s"), st.number_input("DBL",0,key=kp+"d"), st.number_input("TPL",0,key=kp+"t")
        tot = s + db + t
    with c2:
        st.write("Meal Plan Distribution")
        ca, cb = st.columns(2)
        q_bb = ca.number_input("BB Qty", 0, tot, key=kp+"b")
        q_hb = ca.number_input("HB Qty", 0, tot, key=kp+"h")
        q_fb = ca.number_input("FB Qty", 0, tot, key=kp+"f")
        q_sai = cb.number_input("SAI Qty", 0, tot, key=kp+"sa")
        q_ai = cb.number_input("AI Qty", 0, tot, key=kp+"ai")
        mix = {"BB":q_bb, "HB":q_hb, "FB":q_fb, "SAI":q_sai, "AI":q_ai, "RO":max(0, tot-(q_bb+q_hb+q_fb+q_sai+q_ai))}
    with c3:
        adr = st.number_input("ADR", 0.0, 5000.0, float(adr_d), key=kp+"a")
        flr = st.number_input("Floor", 0.0, 2000.0, float(flr_d), key=kp+"fl")
    
    res = run_audit([s,db,t], adr, mix, cp_rate, flr)
    with c4:
        if res:
            st.metric("Net Wealth", f"{cur} {res['u']:.2f}")
            st.markdown(f"<b style='color:{res['c']}'>{res['s']}</b><br><small>{res['d']}</small>", unsafe_allow_html=True)
            st.caption(f"Comm: {res
