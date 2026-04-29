import streamlit as st
from datetime import date

# --- 1. STYLING & BRANDING ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium Engine | Research Edition")
st.markdown("""<style>
.main-title{font-size:2.5rem!important;font-weight:900;color:#1e3799;text-align:center;margin-bottom:10px}
.sub-header{font-size:1.1rem; color:#555; text-align:center; margin-bottom:30px}
.card{padding:18px;border-radius:12px;margin-bottom:15px;border-left:12px solid;font-weight:bold;background:#ffffff;box-shadow: 0 4px 6px rgba(0,0,0,0.1)}
.pricing-row{background:#f8faff;padding:15px;border-radius:10px;margin-top:10px;border:1px solid #d1d9e6}
.pricing-header{background:#1e3799;color:white;padding:6px 12px;border-radius:6px 6px 0 0;font-size:1rem;font-weight:bold}
.sentinel-box{background:#1e3799; color:white; padding:25px; border-radius:12px; margin-bottom:30px; border-left:12px solid #ffc107;}
.google-window{background:#e8f0fe; padding:18px; border-radius:12px; border:2px solid #4285f4; margin-bottom:25px; line-height:1.6}
.theory-box{background:#fdfdfd; padding:25px; border-radius:15px; border:1px solid #dee2e6; margin-top:40px}
[data-testid="stSidebar"]{background:#f1f4f9; border-right:2px solid #dee2e6}
</style>""", unsafe_allow_html=True)

# --- 2. STATE MANAGEMENT & CLEAR LOGIC ---
if "auth" not in st.session_state: st.session_state["auth"] = False
if "reset_key" not in st.session_state: st.session_state["reset_key"] = 0

if not st.session_state["auth"]:
    st.markdown("<h1 class='main-title'>EQUILIBRIUM ENGINE</h1>", unsafe_allow_html=True)
    with st.form("login"):
        pwd = st.text_input("Access Key", type="password")
        if st.form_submit_button("Unlock Engine"):
            if pwd == "Gayan2026": 
                st.session_state["auth"] = True
                st.rerun()
            else: st.error("Access Denied")
    st.stop()

# --- 3. SIDEBAR MASTER CONTROLS ---
with st.sidebar:
    st.markdown("### 👤 Gayan Nugawela\nStrategic Revenue Architect")
    
    # NUCLEAR RESET BUTTON
    if st.button("☢️ Nuclear Data Reset"):
        st.session_state["reset_key"] += 1
        st.rerun()
        
    if st.button("🔒 Sign Out"):
        st.session_state["auth"] = False
        st.rerun()
    st.divider()
    
    rk = str(st.session_state["reset_key"]) 
    
    st.markdown("### 🏨 Pillar 01: Cost Parameters")
    hotel = st.text_input("Property Name", "Wyndham Garden Salalah", key="h"+rk)
    location = st.selectbox("📍 Google Location Select", ["Salalah, Oman", "Muscat, Oman", "Dubai, UAE", "London, UK"], key="loc"+rk)
    inventory = st.number_input("Total Inventory", 1, 1000, 237, key="inv"+rk)
    p01_val = st.number_input("P01 Variable Fee (Per Room)", 0.00, value=6.90, step=0.01, key="p01"+rk)
    
    st.markdown("### 📅 Stay Intelligence")
    d1 = st.date_input("Check-In", date.today(), key="d1"+rk)
    d2 = st.date_input("Check-Out", date.today(), key="d2"+rk)
    m_nights = (d2 - d1).days if (d2 - d1).days > 0 else 1
    st.info(f"Stay Window: {m_nights} Nights")

    st.markdown("### 🌐 Pillar 02: Market Sentinel")
    is_khareef = "Salalah" in location and (6 <= d1.month <= 9)
    m_state = st.radio("Demand Scenario", ["Crisis", "Stagnant", "Recovering", "Peak"], index=(3 if is_khareef else 0), key="ms"+rk)
    m_heat = {"Crisis": 0.65, "Stagnant": 0.85, "Recovering": 1.0, "Peak": 1.35}[m_state]

    st.markdown("### 📈 Pillar 03: Velocity Valve")
    otb = st.slider("Current OTB %", 0, 100, (70 if is_khareef else 15), key="otb"+rk)
    hist = st.slider("Historical Avg %", 0, 100, 45, key="hist"+rk)
    v_mult = 1.25 if (otb-hist) > 10 else 0.85 if (otb-hist) < -10 else 1.0

    st.divider()
    cu = st.selectbox("Currency", ["OMR", "AED", "USD", "EUR"], key="cu"+rk)
    tx = st.number_input("Tax Divisor", value=1.2327, format="%.4f", step=0.0001, key="tx"+rk)
    ota_comm = st.slider("OTA Commission %", 0, 50, 18, key="ota"+rk) / 100
    
    st.markdown("### 🍽️ Pillar 01: Unit Pax Costs")
    c_bb = st.number_input("BB Pax Cost", 0.0, key="cbb"+rk)
    c_hb = st.number_input("HB Pax Cost", 0.0, key="chb"+rk)
    c_fb = st.number_input("FB Pax Cost", 0.0, key="cfb"+rk)
    c_sai = st.number_input("SAI Pax Cost", 5.0, key="csai"+rk)
    c_ai = st.number_input("AI Pax Cost", 5.0, key="cai"+rk)
    costs = {"RO": 0, "BB": c_bb, "HB": c_hb, "FB": c_fb, "SAI": c_sai, "AI": c_ai}

# --- 4. CALCULATION ENGINE ---
def run_yield(rms, adr, n, meals, comm, fl, mice=0, trans=0):
    tr = sum(rms)
    if tr <= 0: return None
    px = (rms[0]*1 + rms[1]*2) / tr 
    net_adr = adr / tx
    m_cost_total = sum((qty/tr) * costs.get(m, 0) * px for m, qty in meals.items() if qty > 0)
    # Wealth Stripping Formula
    unit_w = (net_adr - m_cost_total - ((net_adr - m_cost_total) * comm)) - p01_val + ((mice * px)/(n * tx))
    total_w = (unit_w * tr * n) + (trans / tx)
    dy = total_w / (tr * n)
    hrd = fl * 1.25 if (tr/inventory) >= 0.2 else fl
    l, b = ("OPTIMIZED", "#27ae60") if dy >= hrd else ("DILUTIVE", "#e74c3c")
    return {"u": dy, "l": l, "b": b, "tot": total_w, "rn": tr * n}

# --- 5. MAIN DASHBOARD ---
st.markdown("<h1 class='main-title'>YIELD EQUILIBRIUM MASTER DASHBOARD</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>A Strategic Architecture for High-Yield Revenue Management</p>", unsafe_allow_html=True)

# DYNAMIC GOOGLE INTEL
city_intel = {
    "Salalah, Oman": {"ev": "Salalah Tourism Festival Active", "fl": "+18% Regional Surge", "dem": "High (Khareef)"},
    "Muscat, Oman": {"ev": "Royal Opera Season", "fl": "+5% Steady", "dem": "Moderate"},
    "Dubai, UAE": {"ev": "Gulfood / Shopping Festival", "fl": "+25% Global Surge", "dem": "Peak"},
    "London, UK": {"ev": "Wimbledon / Fashion Week", "fl": "Heavy Congestion", "dem": "Peak"}
}
intel = city_intel.get(location)

st.markdown(f"""<div class='google-window'>
    <b style='color:#4285f4; font-size:1.1rem;'>🌐 Google Intelligence Live Feed: {location}</b><br>
    • <b>Events:</b> {intel['ev']} | <b>Flight Traffic:</b> {intel['fl']} | <b>Live Demand Index:</b> {intel['dem']}
</div>""", unsafe_allow_html=True)

st.markdown(f"""<div class='sentinel-box'>
    <h3 style='margin:0; color:#ffc107;'>🤖 PILLAR 02: MARKET SENTINEL (EXTERNAL ANALYSIS)</h3>
    <div style='display:flex; justify-content:space-between; margin-top:12px;'>
        <span><b>Market State:</b> {m_state} ({m_heat}x)</span>
        <span><b>Velocity Multiplier:</b> {v_mult}x</span>
        <span><b>Sync Nights:</b> {m_nights}</span>
    </div>
</div>""", unsafe_allow_html=True)

def draw_seg(label, key, br, fl_def, col, is_ota=False, is_grp=False):
    rk = str(st.session_state["reset_key"])
    st.markdown(f"<div class='card' style='border-left-color:{col}'>{label}</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.8, 1.2])
    suggested = (br * m_heat) * v_mult
    with c1:
        s = st.number_input("SGL Rooms", 0, key=key+"s"+rk)
        d = st.number_input("DBL Rooms", 0, key=key+"d"+rk)
        n = st.number_input("Nights", value=m_nights, key=key+"n"+rk)
    with c2:
        st.markdown(f"<div class='pricing-row'><div class='pricing-header'>SUGGESTED EQUILIBRIUM ADR: {cu} {suggested:,.2f}</div>", unsafe_allow_html=True)
        adr = st.number_input("Applied Rate", value=float(suggested), key=key+"a"+rk)
        with st.expander("🛠️ Advanced Pillar 01 Settings (Floor/Hurdle)"):
            fl = st.number_input("Floor Rate", float(fl_def), key=key+"f"+rk)
        
        mc = st.columns(3)
        mx = {
            "RO": mc[0].number_input("RO Pax", 0, key=key+"ro"+rk), "BB": mc[0].number_input("BB Pax", 0, key=key+"bb"+rk),
            "HB": mc[1].number_input("HB Pax", 0, key=key+"hb"+rk), "FB": mc[1].number_input("FB Pax", 0, key=key+"fb"+rk),
            "SAI": mc[2].number_input("SAI Pax", 0, key=key+"sai"+rk), "AI": mc[2].number_input("AI Pax", 0, key=key+"ai"+rk)
        }
        mi, tr = 0.0, 0.0
        if is_grp:
            gc = st.columns(2)
            mi = gc[0].number_input("MICE Revenue", 0.0, key=key+"mi"+rk)
            tr = gc[1].number_input("Trans Revenue", 0.0, key=key+"tr"+rk)
        st.markdown("</div>", unsafe_allow_html=True)
    res = run_yield([s, d], adr, n, mx, (ota_comm if is_ota else 0.0), fl, mi, tr)
    if res:
        with c3:
            st.metric("Net Wealth (Unit)", f"{cu} {res['u']:,.2f}")
            st.markdown(f"<div class='status-box' style='background:{res['b']}'>{res['l']}</div>", unsafe_allow_html=True)
            return res['tot']
    return 0

# DRAWING SEGMENTS
w1 = draw_seg("1. DIRECT / FIT", "fit", 65, 40, "#3498db")
w2 = draw_seg("2. OTA CHANNELS", "ota", 60, 35, "#2ecc71", is_ota=True)
w3 = draw_seg("3. CORPORATE / GOV", "corp", 55, 38, "#34495e")
w4 = draw_seg("4. CORPORATE GROUPS", "cgrp", 50, 30, "#9b59b6", is_grp=True)
w5 = draw_seg("5. GROUP TOUR & TRAVEL", "tnt", 45, 25, "#e67e22", is_grp=True)

# PORTFOLIO TOTAL
st.divider()
total_wealth = w1 + w2
