import streamlit as st
from datetime import date

# --- 1. STYLING ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium Master")
st.markdown("""<style>
.main-title{font-size:2.2rem!important;font-weight:900;color:#1e3799;text-align:center;margin-bottom:20px}
.card{padding:15px;border-radius:10px;margin-bottom:10px;border-left:10px solid;font-weight:bold;background:#fcfcfc;box-shadow: 2px 2px 5px rgba(0,0,0,0.05)}
.pricing-row{background:#f1f4f9;padding:12px;border-radius:8px;margin-top:8px;border:1px solid #1e3799}
.pricing-header{background:#1e3799;color:white;padding:5px 10px;border-radius:5px 5px 0 0;font-size:0.9rem;font-weight:bold}
.status-box{padding:10px;border-radius:10px;text-align:center;font-size:1.1rem;font-weight:bold;color:white}
.sentinel-box{background:#1e3799; color:white; padding:20px; border-radius:10px; margin-bottom:25px; border-left:10px solid #ffc107;}
[data-testid="stSidebar"]{background:#f8f9fa; border-right:1px solid #dee2e6}
</style>""", unsafe_allow_html=True)

# --- 2. AUTHENTICATION ---
if "auth" not in st.session_state: st.session_state["auth"] = False
if not st.session_state["auth"]:
    st.markdown("<h1 class='main-title'>EQUILIBRIUM ENGINE</h1>", unsafe_allow_html=True)
    with st.form("login"):
        pwd = st.text_input("Access Key", type="password")
        if st.form_submit_button("Unlock"):
            if pwd == "Gayan2026": 
                st.session_state["auth"] = True
                st.rerun()
            else: st.error("Denied")
    st.stop()

# --- 3. SIDEBAR MASTER CONTROL ---
with st.sidebar:
    st.markdown("### 👤 Strategic Architect\n**Gayan Nugawela**")
    if st.button("🔒 Sign Out"):
        st.session_state["auth"] = False
        st.rerun()
    st.divider()
    
    st.markdown("### 🏨 Pillar 01: Cost & Context")
    hotel = st.text_input("Property (Google Sync Enabled)", "Wyndham Garden Salalah")
    inventory = st.number_input("Total Inventory", 1, 1000, 237)
    p01_val = st.number_input("P01 Variable Fee", 0.00, value=6.90, step=0.10)
    
    st.markdown("### 📅 Stay Intelligence")
    d1 = st.date_input("Check-In", date.today())
    d2 = st.date_input("Check-Out", date.today())
    m_nights = (d2 - d1).days if (d2 - d1).days > 0 else 1
    st.info(f"Stay Duration: {m_nights} Nights")

    st.markdown("### 🌐 Pillar 02: Market Sentinel")
    is_khareef = "Salalah" in hotel and (6 <= d1.month <= 9)
    m_state = st.radio("Market Heat", ["Crisis", "Stagnant", "Recovering", "Peak"], index=(3 if is_khareef else 0))
    m_heat = {"Crisis": 0.65, "Stagnant": 0.85, "Recovering": 1.0, "Peak": 1.35}[m_state]

    st.markdown("### 📈 Pillar 03: Velocity Valve")
    otb = st.slider("Current OTB %", 0, 100, (70 if is_khareef else 15))
    hist = st.slider("Historical Avg %", 0, 100, 45)
    v_mult = 1.25 if (otb-hist) > 10 else 0.85 if (otb-hist) < -10 else 1.0

    st.divider()
    cu = st.selectbox("Currency", ["OMR", "AED", "USD", "EUR"])
    # FIXED: Full 4-digit precision for Tax Divisor
    tx = st.number_input("Tax Divisor", value=1.2327, format="%.4f", step=0.0001)
    ota_comm = st.slider("OTA Commission %", 0, 50, 18) / 100
    
    st.markdown("### 🍽️ Unit Pax Costs")
    c_bb = st.number_input("BB Pax Cost", 0.0)
    c_hb = st.number_input("HB Pax Cost", 0.0)
    c_fb = st.number_input("FB Pax Cost", 0.0)
    c_sai = st.number_input("SAI Pax Cost", 5.0)
    c_ai = st.number_input("AI Cost", 5.0)
    costs = {"RO": 0, "BB": c_bb, "HB": c_hb, "FB": c_fb, "SAI": c_sai, "AI": c_ai}

# --- 4. CALCULATION ENGINE ---
def run_yield(rms, adr, n, meals, comm, fl, mice=0, trans=0):
    tr = sum(rms)
    if tr <= 0: return None
    px = (rms[0]*1 + rms[1]*2) / tr 
    net_adr = adr / tx
    m_cost_total = sum((qty/tr) * costs.get(m, 0) * px for m, qty in meals.items() if qty > 0)
    unit_w = (net_adr - m_cost_total - ((net_adr - m_cost_total) * comm)) - p01_val + ((mice * px)/(n * tx))
    total_w = (unit_w * tr * n) + (trans / tx)
    dy = total_w / (tr * n)
    hrd = fl * 1.25 if (tr/inventory) >= 0.2 else fl
    l, b = ("OPTIMIZED", "#27ae60") if dy >= hrd else ("DILUTIVE", "#e74c3c")
    return {"u": dy, "l": l, "b": b, "tot": total_w, "rn": tr * n}

# --- 5. MAIN DASHBOARD ---
st.markdown("<h1 class='main-title'>YIELD EQUILIBRIUM MASTER</h1>", unsafe_allow_html=True)

st.markdown(f"""<div class='sentinel-box'>
    <h3 style='margin:0; color:#ffc107;'>🤖 PILLAR 02: MARKET SENTINEL ACTIVE</h3>
    <div style='display:flex; justify-content:space-between; margin-top:10px;'>
        <span><b>Property:</b> {hotel}</span>
        <span><b>Condition:</b> {m_state} ({m_heat}x)</span>
        <span><b>Sync Duration:</b> {m_nights} Nights</span>
    </div>
</div>""", unsafe_allow_html=True)

# --- SEGMENT 1: FIT ---
st.markdown("<div class='card' style='border-left-color:#3498db'>1. DIRECT / FIT</div>", unsafe_allow_html=True)
c1, c2, c3 = st.columns([1, 1.8, 1.2])
with c1:
    fs, fd = st.number_input("SGL", 0, key="fs"), st.number_input("DBL", 0, key="fd")
    fn = st.number_input("Nights", value=m_nights, key="fn")
with c2:
    sug1 = (65 * m_heat) * v_mult
    st.markdown(f"<div class='pricing-row'><div class='pricing-header'>SUGGESTED EQUILIBRIUM: {cu} {sug1:,.2f}</div>", unsafe_allow_html=True)
    fa, ff = st.number_input("Applied ADR", value=float(sug1), key="fa"), st.number_input("Floor", 40.0, key="ff")
    m_cols = st.columns(3)
    mx1 = {"RO": m_cols[0].number_input("RO Pax", 0, key="ro1"), "BB": m_cols[0].number_input("BB Pax", 0, key="bb1"),
           "HB": m_cols[1].number_input("HB Pax", 0, key="hb1"), "FB": m_cols[1].number_input("FB Pax", 0, key="fb1"),
           "SAI": m_cols[2].number_input("SAI Pax", 0, key="sai1"), "AI": m_cols[2].number_input("AI Pax", 0, key="ai1")}
    st.markdown("</div>", unsafe_allow_html=True)
res1 = run_yield([fs, fd], fa, fn, mx1, 0, ff)
if res1:
    with c3:
        st.metric("Net Yield", f"{cu} {res1['u']:,.2f}")
        st.markdown(f"<div class='status-box' style='background:{res1['b']}'>{res1['l']}</div>", unsafe_allow_html=True)
        st.session_state["t1"] = res1['tot']

# --- SEGMENT 2: OTA ---
st.divider()
st.markdown("<div class='card' style='border-left-color:#2ecc71'>2. OTA CHANNELS</div>", unsafe_allow_html=True)
o1, o2, o3 = st.columns([1, 1.8, 1.2])
with o1:
    od2 = st.number_input("DBL Rooms", 0, key="od2")
    on2 = st.number_input("Nights", value=m_nights, key="on2")
with o2:
    sug2 = (60 * m_heat) * v_mult
    st.markdown(f"<div class='pricing-row'><div class='pricing-header'>SUGGESTED EQUILIBRIUM: {cu} {sug2:,.2f}</div>", unsafe_allow_html=True)
    oa2, of2 = st.number_input("Applied ADR", value=float(sug2), key="oa2"), st.number_input("Floor", 35.0, key="of2")
    m_cols_o = st.columns(3)
    mx2 = {"RO": m_cols_o[0].number_input("RO Pax", 0, key="ro2"), "BB": m_cols_o[0].number_input("BB Pax", 0, key="bb2"),
           "HB": m_cols_o[1].number_input("HB Pax", 0, key="hb2"), "FB": m_cols_o[1].number_input("FB Pax", 0, key="fb2"),
           "SAI": m_cols_o[2].number_input("SAI Pax", 0, key="sai2"), "AI": m_cols_o[2].number_input("AI Pax", 0, key="ai2")}
    st.markdown("</div>", unsafe_allow_html=True)
res2 = run_yield([0, od2], oa2, on2, mx2, ota_comm, of2)
if res2:
    with o3:
        st.metric("Net Yield", f"{cu} {res2['u']:,.2f}")
        st.markdown(f"<div class='status-box' style='background:{res2['b']}'>{res2['l']}</div>", unsafe_allow_html=True)
        st.session_state["t2"] = res2['tot']

# --- SEGMENT 3: GROUPS ---
st.divider()
st.markdown("<div class='card' style='border-left-color:#9b59b6'>3. CORPORATE GROUPS / MICE</div>", unsafe_allow_html=True)
g1, g2, g3 = st.columns([1, 1.8, 1.2])
with g1:
    gd3 = st.number_input("Group Rooms", 0, key="gd3")
    gn3 = st.number_input("Nights", value=m_nights, key="gn3")
with g2:
    sug3 = (50 * m_heat) * v_mult
    st.markdown(f"<div class='pricing-row'><div class='pricing-header'>SUGGESTED EQUILIBRIUM: {cu} {sug3:,.2f}</div>", unsafe_allow_html=True)
    ga3, gf3 = st.number_input("Applied Rate", value=float(sug3), key="
