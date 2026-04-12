import streamlit as st

# --- STYLE & CONFIG ---
st.set_page_config(page_title="Yield Auditor", layout="wide")
st.markdown("<style>.stMetric { background-color: white; border: 1px solid #ddd; padding: 10px; border-radius: 10px; }</style>", unsafe_allow_html=True)

st.title("🏨 Yield Equilibrium: Command Center")
st.caption("Developed by Gayan Nugawela | Total Revenue Strategy")

# --- SIDEBAR: MEAL COSTS ---
with st.sidebar:
    st.header("1. Meal Net Costs")
    b, l, d = st.number_input("BB", 5.0), st.number_input("LH", 7.0), st.number_input("DR", 10.0)
    s, a = st.number_input("SAI Supp", 8.0), st.number_input("AI Supp", 15.0)
    
    meals = {"RO":0, "BB":b, "HB":b+d, "FB":b+l+d, "SAI":b+l+d+s, "AI":b+l+d+s+a}

    st.header("2. Global Fees")
    p01, tax = st.number_input("Maint. Fee", 10.0), st.number_input("Tax Divisor", 1.2327, format="%.4f")
    cur = st.selectbox("Currency", ["OMR", "USD", "AED", "THB"])

# --- ENGINE ---
def run_audit(rooms, adr, meal_counts, comm, floor):
    tot_rooms = sum(rooms)
    if tot_rooms <= 0: return {"prof":0, "unit":0, "status":"WAITING", "color":"gray", "fb":0}
    
    pax = (rooms[0]*1 + rooms[1]*2 + rooms[2]*3) / tot_rooms
    net_val = (adr * tot_rooms) / tax
    fb_val = sum(qty * meals[p] * pax for p, qty in meal_counts.items())
    
    profit = ((net_val - fb_val) * (1.0 - comm)) - (p01 * tot_rooms)
    unit = profit / tot_rooms
    
    if unit >= (floor + 10): stat, col = "OPTIMIZED", "green"
    elif unit >= floor: stat, col = "MARGINAL", "orange"
    else: stat, col = "DILUTIVE", "red"
    
    return {"prof":profit, "unit":unit, "status":stat, "color":col, "fb":fb_val}

# --- SEGMENT UI ---
def draw_seg(name, kp, adr_def, floor_def, comm):
    st.subheader(name)
    c1, c2, c3, c4 = st.columns([1, 2, 1, 1])
    with c1:
        s = st.number_input("SGL", 0, key=kp+"s")
        db = st.number_input("DBL", 0, key=kp+"db")
        t = st.number_input("TPL", 0, key=kp+"t")
    with c2:
        tot = s+db+t
        q_bb = st.number_input("BB Qty", 0, tot, key=kp+"bb")
        q_hb = st.number_input("HB Qty", 0, tot, key=kp+"hb")
        q_ai = st.number_input("AI Qty", 0, tot, key=kp+"ai")
        m_mix = {"BB":q_bb, "HB":q_hb, "AI":q_ai, "RO":max(0, tot-(q_bb+q_hb+q_ai))}
    with c3:
        adr = st.number_input("ADR", 1.0, 5000.0, float(adr_def), key=kp+"a")
        flr = st.number_input("Floor", 1.0, 2000.0, float(floor_def), key=kp+"f")
    
    res = run_audit([s,db,t], adr, m_mix, comm, flr)
    with c4:
        st.metric("Net Wealth", f"{cur} {res['unit']:.2f}")
        st.markdown(f"<b style='color:{res['color']}'>{res['status']}</b>", unsafe_allow_html=True)
    return res

# --- RENDER DASHBOARD ---
r1 = draw_seg("Wholesale", "wh", 45, 25, 0.20)
r2 = draw_seg("Group Tour", "gt", 40, 20, 0.15)
r3 = draw_seg("Group Corp", "gc", 55, 30, 0.0)
r4 = draw_seg("Direct / FIT", "di", 65, 40, 0.0)
r5 = draw_seg("OTA", "ot", 60, 35, 0.18)
r6 = draw_seg("Corporate", "co", 58, 32, 0.0)

# --- TOTALS ---
st.divider()
all_res = [r1, r2, r3, r4, r5, r6]
tp, tf = sum(r['prof'] for r in all_res), sum(r['fb'] for r in all_res)
m1, m2, m3 = st.columns(3)
m1.metric("Total Room Wealth", f"{cur} {tp:,.2f}")
m2.metric("Total F&B Cost", f"{cur} {tf:,.2f}")
m3.metric("Property Grand Total", f"{cur} {(tp+tf):,.2f}")

st.write("---")
st.write("✅ Audit Engine Active. # END SCRIPT")
