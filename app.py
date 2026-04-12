import streamlit as st

# --- STYLE ---
st.set_page_config(page_title="Yield Auditor", layout="wide")
st.markdown("<style>.stMetric { background-color: #ffffff; border: 2px solid #f0f2f6; padding: 10px; border-radius: 12px; } .card { padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 10px solid; font-weight: bold; }</style>", unsafe_allow_html=True)

st.title("🏨 Yield Equilibrium Center")
st.caption("Developed by Gayan Nugawela | Full Allocation Logic")

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
    px = (rms[0]*1 + rms[1]*2 + rms[2]*3) / tot
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
    c1, c2, c3, c4 = st.columns([1, 2.5, 1
