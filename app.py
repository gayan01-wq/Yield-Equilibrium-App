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
    h_cap = st.number_input("Total Rooms", 1, 1000, 158)
    st.header("🍽️ Costs")
    b, l, d = st.number_input("BB",0.,500.,5.), st.number_input("LN",0.,500.,7.), st.number_input("DN",0.,500.,10.)
    s, a = st.number_input("SAI",0.,500.,8.), st.number_input("AI",0.,500.,15.)
    mls = {"RO":0, "BB":b, "HB":b+d, "FB":b+l+d, "SAI":b+l+d+s, "AI":b+l+d+s+a}
    st.header("⚙️ Global")
    p01, tx = st.number_input("P01 Fee",0.,500.,6.9), st.number_input("Tax Div",1.,2.,1.2327,format="%.4f")
    ota_com = st.slider("OTA Comm %", 0, 50, 18) / 100
    cur = st.selectbox("Cur", ["OMR", "USD", "AED", "THB"])

# --- ENGINE ---
def run(rms, adr, nts, mix, cp, flr):
    tot = sum(rms)
    if tot <= 0: return None
    px = (rms[0]*1.0 + rms[1]*2.0 + rms[2]*3.0) / tot
    net = (adr * tot) / tx
    fb = sum(qty * mls[p] * px for p, qty in mix.items())
    cm = (net - fb) * cp
    u = ((net - fb - cm) - (p01 * tot)) / tot
    pr_t = u * tot * nts
    pct = (u / adr) * 100 if adr > 0 else 0
    cap_i = (tot / h_cap) * 100
    # Strategic Trigger: Optimized if Wealth Contribution > 15% or Margin > 55%
    w_con = (pr_t / ((flr * h_cap) * nts)) * 100 if flr > 0 else 0
    adj_f = flr * 0.75 if nts > 7 else flr
    if u >= (adj_f + 5) or pct > 55 or w_con > 15 or cap_i > 20: s, c = "OPTIMIZED", "#27ae60"
    elif u >= adj_f: s, c = "MARGINAL", "#f39c12"
    else: s, c = "DILUTIVE", "#e74c3c"
    return {"u":u, "s":s, "c":c, "pt":pr_t, "pct":pct, "cap":cap_i, "wc":w_con}

# --- UI ROW ---
def seg(nm, clr, bg, kp, ad_d, fl_d, cp):
    st.markdown(f"<div class='card' style='background:{bg}; border-left-color:{clr};'>{nm}</div>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns([1, 3.2, 1, 1.2])
    with c1:
        r = [st.number_input("SGL",0,key=kp+"s"), st.number_input("DBL",0,key=kp+"d"), st.number_input("TPL",0,key=kp+"t")]
        nts = st.number_input("Nights", 1, 365, key=kp+"n")
    with c2:
        st.write("Meals")
        mx1, mx2, mx3 = st
