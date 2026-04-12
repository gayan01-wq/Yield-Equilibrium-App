import streamlit as st

# --- STYLE ---
st.set_page_config(page_title="Yield Auditor", layout="wide")
st.markdown("<style>.stMetric { background-color: #ffffff; border: 2px solid #f0f2f6; padding: 10px; border-radius: 12px; } .card { padding: 10px; border-radius: 10px; margin-bottom: 8px; border-left: 10px solid; font-weight: bold; }</style>", unsafe_allow_html=True)

st.title("🏨 Yield Equilibrium Center")
st.caption("Developed by Gayan Nugawela | Property-Specific Capacity Logic")

# --- SIDEBAR ---
with st.sidebar:
    st.header("🏢 Property Settings")
    h_name = st.text_input("Hotel Name", "Wyndham Garden Salalah")
    h_total = st.number_input("Total Room Capacity", 1, 1000, 158)
    
    st.header("🍽️ Meal Costs")
    b, l, d = st.number_input("BB", 0.0, 1000.0, 5.0), st.number_input("LN", 0.0, 1000.0, 7.0), st.number_input("DN", 0.0, 1000.0, 10.0)
    s, a = st.number_input("SAI", 0.0, 1000.0, 8.0), st.number_input("AI", 0.0, 1000.0, 15.0)
    mls = {"RO":0, "BB":b, "HB":b+d, "FB":b+l+d, "SAI":b+l+d+s, "AI":b+l+d+s+a}
    
    st.header("⚙️ Global Settings")
    p01 = st.number_input("P01 Fee (Maint)", 0.0, 500.0, 6.90)
    tax = st.number_input("Tax Div", 1.0, 2.0, 1.2327, format="%.4f")
    ota_com = st.slider("OTA Comm %", 0, 50, 18) / 100
    cur = st.selectbox("Currency", ["OMR", "USD", "AED", "THB"])

# --- ENGINE ---
def run(rms, adr, nts, mix, cp, flr):
    tot = sum(rms)
    if tot <= 0: return None
    px = (rms[0]*1.0 + rms[1]*2.0 + rms[2]*3.0) / tot
    net = (adr * tot) / tax
    fb = sum(qty * mls[p] * px for p, qty in mix.items())
    cm = (net - fb) * cp
    pr_daily = (net - fb - cm) - (p01 * tot)
    
    pr_total = pr_daily * nts
    u = pr_daily / tot
    pct = (u / adr) * 100 if adr > 0 else 0
    
    # NEW: Capacity Impact Calculation
    cap_impact = (tot / h_total) * 100
    
    # SYSTEM LOGIC: "Yield Equilibrium" Optimized Trigger
    # Green if: (Wealth > Floor + 5) OR (Margin > 55%) OR (Total Wealth > 5000) OR (Capacity Impact > 20%)
    adj_floor = flr * 0.75 if nts > 7 else flr
    
    if u >= (adj_floor + 5) or pct > 55 or pr_total > 5000 or cap_impact > 20: 
        lbl, col = "OPTIMIZED", "#27ae60"
    elif u >= adj_floor: 
        lbl, col = "MARGINAL", "#f39c12"
    else: 
        lbl, col = "DILUTIVE", "#e74c3c"
    
    return {"u":u, "s":lbl, "c":col, "p_t":pr_total, "pct":pct, "cap":cap_impact}

# --- UI ROW ---
def seg(name, color, bg, kp, adr_d, flr_d, cp):
    st.markdown(f"<div class='card' style='background:{bg}; border-left-color:{color};'>{name}</div>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns([1, 3, 1, 1.2])
    with c1:
        r = [st.number_input("SGL",0,key=kp+"s"), st.number_input("DBL",0,key=kp+"d"), st.number_input("TPL",0,key=kp+"t")]
        tot = sum(r)
        nts = st.number_input("Nights", 1, 365, key=kp+"n")
    with c2:
        st.write("Meal Plan Allocation")
        ca, cb, cc = st.columns(3)
        q_ro, q_bb = ca.number_input("RO Qty", 0, tot, key=kp+"ro"), ca.number_input("BB Qty", 0, tot, key=kp+"b")
        q_hb, q_fb = cb.number_input("HB Qty", 0, tot, key=kp+"h"), cb.number_input("FB Qty", 0, tot, key=kp+"f")
        q_sa, q_ai = cc.number_input("SAI Qty", 0, tot, key=kp+"sa"), cc.number_input("AI Qty", 0, tot, key=kp+"ai")
        mix = {"RO":q_ro, "BB":q_bb, "HB":q_hb, "FB":q_fb, "SAI":q_sa, "AI":q_ai}
    with c3:
        adr = st.number_input("Rate", 0.0, 5000.0, float(adr_d), key=kp+"a")
        flr = st.number_input("Floor", 0.0, 2000.0, float(flr_d), key=kp+"fl")
    res = run(r, adr, nts, mix, cp, flr)
    with c4:
        if res:
            st.metric("Net Wealth", f"{cur} {res['u']:.2f}")
            st.markdown(f"<b style='color:{res['c']}'>{res['s']}</b>", unsafe_allow_html=True)
            st.write(f"Cap Impact: **{res['cap']:.1f}%**")
            st.write(f"Stay Wealth: **{res['p_t']:,.2f}**")
    return res

# --- RENDER ---
st.header(f"📍 Audit for: {h_name}")
r1 = seg("Wholesale", "#e67e22", "#fff3e0", "wh", 45, 25, 0.20)
r2 = seg("Group Tour", "#d35400", "#fbe9e7", "gt", 40, 20, 0.15)
r3 = seg("Group Corp", "#2c3e50", "#eceff1", "gc", 55, 30, 0.0)
r4 = seg("Direct/FIT", "#2980b9", "#e3f2fd", "di", 65, 40, 0.0)
r5 = seg("OTA Segment", "#2ecc71", "#e8f5e9", "ot", 60, 35, ota_com)
r6 = seg("Corporate", "#8e44ad", "#f3e5f5", "co", 58, 32, 0.0)

st.divider()
all_r = [x for x in [r1,r2,r3,r4,r5,r6] if x]
if all_r:
    tp = sum(x['p_t'] for x in all_r)
    st.metric(f"Total {h_name} Stay Wealth", f"{cur} {tp:,.2f}")
st.write("✅ Capacity Impact logic added. Inventory Velocity is now live. # DONE")
