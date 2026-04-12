import streamlit as st

# --- STYLE ---
st.set_page_config(page_title="Yield Auditor", layout="wide")
st.markdown("<style>.stMetric { background-color: #ffffff; border: 2px solid #f0f2f6; padding: 10px; border-radius: 12px; } .card { padding: 12px; border-radius: 10px; margin-bottom: 8px; border-left: 10px solid; font-weight: bold; }</style>", unsafe_allow_html=True)

st.title("🏨 Yield Equilibrium Center")
st.caption("Developed by Gayan Nugawela | Full Allocation Logic Active")

# --- SIDEBAR ---
with st.sidebar:
    st.header("🍽️ Meal Costs (0-1000)")
    b, l, d = st.number_input("BB", 0.0, 1000.0, 5.0), st.number_input("LN", 0.0, 1000.0, 7.0), st.number_input("DN", 0.0, 1000.0, 10.0)
    s, a = st.number_input("SAI", 0.0, 1000.0, 8.0), st.number_input("AI", 0.0, 1000.0, 15.0)
    meals = {"RO":0, "BB":b, "HB":b+d, "FB":b+l+d, "SAI":b+l+d+s, "AI":b+l+d+s+a}
    st.header("⚙️ Fees")
    p01, tax = st.number_input("P01 Fee", 10.0), st.number_input("Tax Div", 1.2327, format="%.4f")
    cur = st.selectbox("Currency", ["OMR", "USD", "AED", "THB"])

# --- ENGINE ---
def run_audit(rms, adr, mix, cp, floor):
    tot = sum(rms)
    if tot <= 0: return None
    px = (rms[0]*1.0 + rms[1]*2.0 + rms[2]*3.0) / tot
    net = (adr * tot) / tax
    fb = sum(qty * meals[p] * px for p, qty in mix.items())
    cm = (net - fb) * cp
    pr = (net - fb - cm) - (p01 * tot)
    u = pr / tot
    if u >= (floor + 15): lbl, col, ds = "OPTIMIZED", "#27ae60", "Strong Wealth Retention."
    elif u >= floor: lbl, col, ds = "MARGINAL", "#f39c12", "Minimal Leakage."
    else: lbl, col, ds = "DILUTIVE", "#e74c3c", "Wealth Leakage Detected!"
    return {"u":u, "s":lbl, "c":col, "d":ds, "cm":cm, "fb":fb, "p":pr}

# --- UI ROW ---
def segment(name, color, bg, kp, adr_d, flr_d, cp):
    st.markdown(f"<div class='card' style='background:{bg}; border-left-color:{color};'>{name}</div>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns([1, 2.5, 1, 1.5])
    with c1:
        rms = [st.number_input("SGL",0,key=kp+"s"), st.number_input("DBL",0,key=kp+"d"), st.number_input("TPL",0,key=kp+"t")]
        tot = sum(rms)
    with c2:
        st.write("Meal Plan Allocation")
        ca, cb = st.columns(2)
        q_bb = ca.number_input("BB Qty", 0, tot, key=kp+"b")
        q_hb = ca.number_input("HB Qty", 0, tot, key=kp+"h")
        q_fb = ca.number_input("FB Qty", 0, tot, key=kp+"f")
        q_sa = cb.number_input("SAI Qty", 0, tot, key=kp+"sa")
        q_ai = cb.number_input("AI Qty", 0, tot, key=kp+"ai")
        mix = {"BB":q_bb, "HB":q_hb, "FB":q_fb, "SAI":q_sa, "AI":q_ai, "RO":max(0, tot-(q_bb+q_hb+q_fb+q_sa+q_ai))}
    with c3:
        adr = st.number_input("Rate", 0.0, 5000.0, float(adr_d), key=kp+"a")
        flr = st.number_input("Floor", 0.0, 2000.0, float(flr_d), key=kp+"fl")
    res = run_audit(rms, adr, mix, cp, flr)
    with c4:
        if res:
            st.metric("Net Wealth", f"{cur} {res['u']:.2f}")
            st.markdown(f"<b style='color:{res['c']}'>{res['s']}</b><br><small>{res['d']}</small>", unsafe_allow_html=True)
            st.caption(f"Comm: {res['cm']:.2f} | FB: {res['fb']:.2f}")
    return res

# --- RENDER ---
r1 = segment("Wholesale", "#e67e22", "#fff3e0", "wh", 45, 25, 0.20)
r2 = segment("Group Tour", "#d35400", "#fbe9e7", "gt", 40, 20, 0.15)
r3 = segment("Group Corp", "#2c3e50", "#eceff1", "gc", 55, 30, 0.0)
r4 = segment("Direct/FIT", "#2980b9", "#e3f2fd", "di", 65, 40, 0.0)
r5 = segment("OTA", "#27ae60", "#e8f5e9", "ot", 60, 35, 0.18)
r6 = segment("Corporate", "#8e44ad", "#f3e5f5", "co", 58, 32, 0.0)

st.divider()
all_r = [x for x in [r1,r2,r3,r4,r5,r6] if x]
if all_r:
    tp, tf = sum(x['p'] for x in all_r), sum(x['fb'] for x in all_r)
    m1, m2 = st.columns(2)
    m1.metric("Total Property Wealth", f"{cur} {tp:,.2f}")
    m2.metric("Total F&B Cost", f"{cur} {tf:,.2f}")
st.write("✅ System Active. # DONE")
