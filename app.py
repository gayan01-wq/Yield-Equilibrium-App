import streamlit as st

# --- STYLE & CONFIG ---
st.set_page_config(page_title="Yield Auditor", layout="wide")
st.markdown("<style>.stMetric { background-color: #ffffff; border: 2px solid #f0f2f6; padding: 10px; border-radius: 12px; } .card { padding: 10px; border-radius: 10px; margin-bottom: 8px; border-left: 10px solid; font-weight: bold; }</style>", unsafe_allow_html=True)

st.title("🏨 Yield Equilibrium Center")
st.caption("Developed by Gayan Nugawela | Strategic Anchor & Capacity Logic")

# --- SIDEBAR ---
with st.sidebar:
    st.header("🏢 Property")
    h_nm = st.text_input("Hotel", "Wyndham Garden Salalah")
    h_cp = st.number_input("Total Rooms", 1, 1000, 158)
    st.header("🍽️ Costs")
    b, l, d = st.number_input("BB", 0.0, 500.0, 5.0), st.number_input("LN", 0.0, 500.0, 7.0), st.number_input("DN", 0.0, 500.0, 10.0)
    s, a = st.number_input("SAI", 0.0, 500.0, 8.0), st.number_input("AI", 0.0, 500.0, 15.0)
    mls = {"RO":0, "BB":b, "HB":b+d, "FB":b+l+d, "SAI":b+l+d+s, "AI":b+l+d+s+a}
    st.header("⚙️ Global")
    p01 = st.number_input("P01 Fee", 0.0, 100.0, 6.90)
    tax = st.number_input("Tax Div", 1.0, 2.0, 1.2327, format="%.4f")
    ota_p = st.slider("OTA Comm %", 0, 50, 18) / 100
    cur = st.selectbox("Cur", ["OMR", "USD", "AED", "THB"])

# --- ENGINE ---
def run(rms, adr, nts, mix, cp, flr):
    tot = sum(rms)
    if tot <= 0: return None
    px = (rms[0]*1.0 + rms[1]*2.0 + rms[2]*3.0) / tot
    net = (adr * tot) / tax
    fb = sum(qty * mls[p] * px for p, qty in mix.items())
    cm = (net - fb) * cp
    day_p = (net - fb - cm) - (p01 * tot)
    tot_p = day_p * nts
    u = day_p / tot
    # Strategic Metrics
    mrg = (u / adr) * 100 if adr > 0 else 0
    cap = (tot / h_cp) * 100
    pot_p = (flr * h_cp) * nts
    w_con = (tot_p / pot_p) * 100 if pot_p > 0 else 0
    # Yield Logic
    adj_f = flr * 0.75 if nts > 7 else flr
    if u >= (adj_f + 5) or mrg > 55 or w_con > 15 or cap > 20: lbl, col = "OPTIMIZED", "#27ae60"
    elif u >= adj_f: lbl, col = "MARGINAL", "#f39c12"
    else: lbl, col = "DILUTIVE", "#e74c3c"
    return {"u":u, "s":lbl, "c":col, "tp":tot_p, "pct
