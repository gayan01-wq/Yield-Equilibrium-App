import streamlit as st

# --- CONFIG ---
st.set_page_config(page_title="Yield Auditor", layout="wide")
st.markdown("<style>.stMetric { background-color: #ffffff; border: 2px solid #f0f2f6; padding: 10px; border-radius: 12px; } .card { padding: 10px; border-radius: 10px; margin-bottom: 8px; border-left: 10px solid; font-weight: bold; }</style>", unsafe_allow_html=True)

st.title("🏨 Yield Equilibrium Center")
st.caption("Developed by Gayan Nugawela | Strategic Anchor Logic")

# --- SIDEBAR ---
with st.sidebar:
    h_nm = st.text_input("Hotel", "Wyndham Garden Salalah")
    h_cp = st.number_input("Total Rooms", 1, 1000, 158)
    st.header("🍽️ Costs")
    b, l, d = st.number_input("BB", 0.0, 500.0, 5.0), st.number_input("LN", 0.0, 500.0, 7.0), st.number_input("DN", 0.0, 500.0, 10.0)
    s, a = st.number_input("SAI", 0.0, 500.0, 8.0), st.number_input("AI", 0.0, 500.0, 15.0)
    mls = {"RO":0,"BB":b,"HB":b+d,"FB":b+l+d,"SAI":b+l+d+s,"AI":b+l+d+s+a}
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
