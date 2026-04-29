import streamlit as st
from datetime import date

# --- 1. STYLING & BRANDING ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium Engine | Research Edition")
st.markdown("""<style>
.block-container{padding-top:1rem!important; padding-bottom:1rem!important;}
.main-title{font-size:2rem!important;font-weight:900;color:#1e3799;text-align:center;margin-top:-20px;}
.sub-header{font-size:0.9rem; color:#555; text-align:center; margin-bottom:20px}
.card{padding:10px;border-radius:10px;margin-bottom:8px;border-left:10px solid;font-weight:bold;background:#ffffff;box-shadow: 0 2px 4px rgba(0,0,0,0.05)}
.pricing-row{background:#f8faff;padding:10px;border-radius:8px;border:1px solid #d1d9e6}
.pricing-header{background:#1e3799;color:white;padding:3px 8px;border-radius:4px;font-size:0.8rem;font-weight:bold; margin-bottom:5px;}
.sentinel-box{background:#1e3799; color:white; padding:15px; border-radius:10px; margin-bottom:20px; border-left:10px solid #ffc107;}
.google-window{background:#e8f0fe; padding:15px; border-radius:10px; border:2px solid #4285f4; margin-bottom:20px; font-size:0.85rem; line-height:1.5}
[data-testid="stSidebar"]{background:#f1f4f9; border-right:2px solid #dee2e6}
.block-container .element-container {margin-bottom: 0.5rem;}
</style>""", unsafe_allow_html=True)

# --- 2. STATE MANAGEMENT & CLEAR LOGIC ---
if "auth" not in st.session_state: st.session_state["auth"] = False
if "reset_key" not in st.session_state: st.session_state["reset_key"] = 0

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

# --- 3. SIDEBAR MASTER CONTROLS ---
with st.sidebar:
    st.markdown("<p style='font-size:1.1rem;font-weight:700;color:#1e3799;'>👤 Strategic Architect</p><p style='font-size:0.9rem;margin-top:-15px;'>Gayan Nugawela</p>", unsafe_allow_html=True)
    
    # Reset Button
    if st.button("☢️ Nuclear Data Reset"):
        st.session_state["reset_key"] += 1
        st.rerun()
        
    if st.button("🔒 Sign Out"):
        st.session_state["auth"] = False
        st.rerun()
    st.divider()
    
    rk = str(st.session_state["reset_key"]) 
    
    st.markdown("### 🏨 Pillar 01: Context")
    hotel = st.text_input("Property Name", "Wyndham Garden Salalah", key="h"+rk)
    location = st.selectbox("📍 Google Location", ["Salalah, Oman", "Muscat, Oman", "Dubai, UAE", "London, UK"], key="loc"+rk)
    inventory = st.number_input("Total Inventory", 1, 1000, 237, key="inv"+rk)
    p01_val = st.number_input("P01 Variable Fee", 0.00, value=6.90, step=0.01, key="p01"+rk)
    
    st.markdown("### 📅 Stay Intelligence")
    d1 = st.date_input("Check-In", date.today(), key="d1"+rk)
    d2 = st.date_input("Check-Out", date.today(), key="d2"+rk)
    m_nights = (d2 - d1).days if (d2 - d1).days > 0 else 1
    st.info(f"Stay Window: {m_nights} Nights")

    st.markdown("### 🌐 Pillar 02: Market Sentinel")
    is_khareef = "Salalah" in location and (6 <= d1.month <= 9)
    m_state = st.radio("Demand Scenario", ["Crisis", "Stagnant", "Recovering", "Peak"], index=(3 if is_khareef else 0), key="ms"+rk)
    m_heat = {"Crisis": 0.65, "Stagnant": 0.85, "Recovering": 1.0, "Peak": 1.35}[m_state]

    st.markdown("### 📈 Pillar 03: Velocity")
    otb = st.slider("OTB %", 0, 100, (70 if is_khareef else 15), key="otb"+rk)
    hist = st.slider("Historical Avg %", 0, 100, 45, key="hist"+rk)
    v_mult = 1.25 if (otb-hist) > 10 else 0.85 if (otb-hist) < -10 else 1.0

    st.divider()
    cu = st.selectbox("Currency", ["OMR", "AED", "USD", "EUR"], key="cu"+rk)
    # PRECISION TAX DIVISOR
    tx = st.number_input("Tax Divisor", value=1.2327, format="%.4f", step=0.0001, key="tx"+rk)
    ota_comm = st.slider("OTA Commission %", 0, 50, 18, key="ota"+rk) / 100
    
    st.markdown("### 🍽️ Pillar 01: Pax Costs")
    c_bb = st.number_input("BB Pax Cost", 0.0, key="cbb"+rk)
    c_sai = st.number_input("SAI Pax Cost", 5.0, key="csai"+rk)
    costs = {"RO": 0, "BB": c_bb, "SAI": c_sai, "AI": c_sai}

# --- 4. CALCULATION ENGINE ---
def run_yield(rms, adr, n, meals, comm, fl, mice=0):
    tr = sum(rms)
    if tr <= 0: return None
    px = (rms[0]*1 + rms[1]*2) / tr 
    net_adr = adr / tx
    m_cost_total = sum((qty/tr) * costs.get(m, 0) * px for m, qty in meals.items() if qty > 0)
    # Wealth Stripping
    unit_w = (net_adr - m_cost_total - ((net_adr - m_cost_total) * comm)) - p01_val + ((mice * px)/(n * tx))
    dy = unit_w # Simplified dy display
    hrd = fl * 1.25 if (tr/inventory) >= 0.2 else fl
    l, b = ("OPTIMIZED", "#27ae60") if dy >= hrd else ("DILUTIVE", "#e74c3c")
    return {"u": dy, "l": l, "b": b, "tot": unit_w * tr * n}

# --- 5. MAIN DASHBOARD ---
st.markdown("<h1 class='main-title'>YIELD EQUILIBRIUM MASTER DASHBOARD</h1>", unsafe_allow_html=True)

# 🌐 INTEGRATED INTEL & PILLAR DESCRIPTIONS
city_intel = {
    "Salalah, Oman": {"ev": "Salalah Tourism Festival", "dem": "High (Khareef)"},
    "Dubai, UAE": {"ev": "Shopping Festival / EXPO", "dem": "Peak"}
}
intel = city_intel.get(location, {"ev": "Moderate", "dem": "Recovering"})

with st.container():
    cl1, cl2 = st.columns([1.5, 1])
    with cl1:
        st.markdown(f"""<div class='google-window'>
            <b style='color:#4285f4; font-size:1rem;'>🌐 Google Intelligence Live Feed: {location}</b><br>
            • <b>Events:</b> {intel['ev']}<br>
            • <b>Live Demand Index:</b> {intel['dem']}<br>
            • <b>Theoretical Frame:</b> Pillar 02 analyzes external market ceil while Pillar 03 analyzes internal pace Valve.
        </div>""", unsafe_allow_html=True)
    with cl2:
        st.markdown(f"""<div class='sentinel-box'>
            <h4 style='margin:0; color:#ffc107; font-size:1rem;'>🤖 Pillar 01: The Cost Foundation</h4>
            <div style='font-size:0.8rem; margin-top:5px;'>
                • <b>Hurdle Rate:</b> The floor after Tax (<b>1.2327</b>), OTA %, P01 variable fee, and Pax Costs.
                • <b>Wealth Stripping:</b> Net Profit > Hurdle Rate = OPTIMIZED.
            </div>
        </div>""", unsafe_allow_html=True)

# REDUCED Vertical Space for segments
def draw_seg(label, key, br, fl_def, col, is_ota=False):
    rk = str(st.session_state["reset_key"])
    st.markdown(f"<div class='card' style='border-left-color:{col}; padding: 8px 10px; margin-bottom: 5px;'>{label}</div>", unsafe_allow_html=True)
    c1, c2 = st.columns([2.5, 1.2])
    suggested = (br * m_heat) * v_mult
    
    with c1:
        st.markdown(f"<div class='pricing-row'>", unsafe_allow_html=True)
        # Compact inputs
        cr1, cr2 = st.columns([2, 1])
        fa = cr1.number_input("Applied Rate", value=float(suggested), key="a"+key+rk)
        ff = cr2.number_input("Floor", float(fl_def), key="f"+key+rk)
        
        # Reduced meal inputs
        m_cols = st.columns(3)
        m_ro = m_cols[0].number_input("RO Pax", 0, key="ro"+key+rk)
        m_bb = m_cols[1].number_input("BB Pax", 0, key="bb"+key+rk)
        m_sai = m_cols[2].number_input("SAI Pax", 0, key="sai"+key+rk
