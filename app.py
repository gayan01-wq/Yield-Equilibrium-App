import streamlit as st
from datetime import date

# --- 1. STYLING (The Professional Aesthetic) ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium Master")
st.markdown("""<style>
.block-container{padding-top:1rem!important;}
.main-title{font-size:1.8rem!important;font-weight:900;color:#1e3799;text-align:center;margin-top:-10px;}
.card{padding:10px;border-radius:10px;margin-bottom:8px;border-left:10px solid;background:#ffffff;box-shadow: 0 2px 4px rgba(0,0,0,0.1)}
.pricing-row{background:#f8faff;padding:12px;border-radius:10px;border:1px solid #d1d9e6; margin-top:5px;}
.google-window{background:#e8f0fe; padding:15px; border-radius:12px; border:2px solid #4285f4; margin-bottom:15px; font-size:0.85rem; line-height:1.6;}
.status-indicator{padding:10px; border-radius:10px; text-align:center; font-weight:900; font-size:1.2rem; color:white; margin-top:10px;}
.audit-box{background:#fff9c4; border:1px solid #fbc02d; padding:10px; border-radius:8px; margin-top:12px; text-align:center; font-weight:bold; color:#5f4300; font-size:0.9rem;}
.theory-box{background:#fdfdfd; padding:25px; border-radius:15px; border:1px solid #dee2e6; margin-top:40px}
[data-testid="stSidebar"]{background:#f1f4f9; border-right:1px solid #dee2e6}
</style>""", unsafe_allow_html=True)

# --- 2. SECURITY & SESSION ---
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
            else: st.error("Access Denied")
    st.stop()

# --- 3. SIDEBAR (STRATEGIC INPUTS) ---
with st.sidebar:
    st.markdown("### 👤 Strategic Architect\nGayan Nugawela")
    if st.button("☢️ Nuclear Data Reset"):
        st.session_state["reset_key"] += 1
        st.rerun()
    st.divider()
    
    rk = str(st.session_state["reset_key"]) 
    
    st.markdown("### 🏨 Pillar 01: Universal Search")
    hotel_name = st.text_input("🏨 Hotel Name", "Wyndham Garden Salalah", key="h"+rk)
    city_name = st.text_input("📍 City Search", "Salalah, Oman", key="c"+rk)
    
    d1 = st.date_input("Check-In Date", date.today(), key="d1"+rk)
    d2 = st.date_input("Check-Out Date", date.today(), key="d2"+rk)
    m_nights = (d2 - d1).days if (d2 - d1).days > 0 else 1
    st.success(f"**Stay Nights: {m_nights}**")
    
    st.divider()
    st.markdown("### 🌐 Pillar 02: Market Sentinel")
    m_state = st.radio("Demand Category", ["Distressed / Crisis", "Stagnant / Recovery", "Peak / Seasonal", "Compression / Sold Out"], index=1, key="ms"+rk)
    m_heat = {"Distressed / Crisis": 0.65, "Stagnant / Recovery": 1.0, "Peak / Seasonal": 1.35, "Compression / Sold Out": 1.65}[m_state]

    st.markdown("### 📊 Pillar 03: Velocity")
    otb_occ = st.slider("OTB Occupancy %", 0, 100, 15, key="otb"+rk)
    avg_hist = st.slider("Historical Avg %", 0, 100, 45, key="hist"+rk)
    v_mult = 1.25 if otb_occ > avg_hist else 0.85 if otb_occ < (avg_hist - 15) else 1.0

    st.divider()
    tx_div = st.number_input("Tax Divisor", value=1.2327, format="%.4f", key="tx"+rk)
    ota_comm = st.slider("OTA Commission %", 0, 40, 18, key="comm"+rk)
    p01_fee = st.number_input("P01 Variable Fee", 0.0, value=6.90, key="p01"+rk)

    st.markdown("### 🍽️ Unit Costs (Pillar 01)")
    c_bb = st.number_input("BB Unit Cost", 0.0, key="cbb"+rk)
    c_hb = st.number_input("HB Unit Cost", 2.5, key="chb"+rk)
    c_fb = st.number_input("FB Unit Cost", 5.0, key="cfb"+rk)
    c_sai = st.number_input("SAI Unit Cost", 7.5, key="csai"+rk)
    c_ai = st.number_input("AI Unit Cost", 10.0, key="cai"+rk)
    meal_costs = {"RO": 0, "BB": c_bb, "HB": c_hb, "FB": c_fb, "SAI": c_sai, "AI": c_ai}

# --- 4. GOOGLE INTELLIGENCE DATA (PILLAR 02) ---
intel_db = {
    "Salalah": {"ev": "Khareef Festival (Monsoon Season)", "fl": "+18% Surge (Oman Air/SalamAir)", "basis": "Seasonal Demand Shift"},
    "Dubai": {"ev": "Global Village / Shopping Festival", "fl": "+25% Influx via EK/FZ Hubs", "basis": "Peak Regional Synergy"},
    "Muscat": {"ev": "Opera House / Muscat Food Fest", "fl": "+10% Regional Traffic surge", "basis": "Cultural Peak Window"},
    "London": {"ev": "Wimbledon / Fashion Week Season", "fl": "LHR Slots at Critical Capacity", "basis": "Global Hub Supply Scarcity"}
}
# FIXED: Line 77 logic safely terminated and closed
active_intel = intel_db.get(next((k for k in intel_db if k.lower() in city_name.lower()), None), 
                           {"ev": "Standard Market Events", "fl": "Baseline Seasonal Rotation", "basis": "Market Equilibrium"})

# --- 5. CALCULATION ENGINE ---
def run_yield(rms, nts, adr, meals, hurdle, comm_rate=0.18, laundry=0, mice=0, trans=0):
    tr = sum(rms)
    if tr <= 0: return None
    rn = tr * nts
    net_adr = adr / tx_div
    total_m = sum(qty * meal_costs.get(p, 0) for p, qty in meals.items())
    avg_m = (total_m / tr) if tr > 0 else 0
    # The Wealth Stripping Formula
    unit_w = (net_adr - avg_m - (net_adr * comm_rate)) - p01_fee - laundry + (mice / tx_div)
    total_w = (unit_w * rn) + (trans / tx_div)
    status, color = ("OPTIMIZED", "#27ae60") if unit_w >= hurdle else ("DILUTIVE", "#e74c3c")
    return {"w": unit_w, "st": status, "cl": color, "rn": rn, "total": total_w}

# --- 6. MAIN DASHBOARD ---
st.markdown("<h1 class='main-title'>YIELD EQUILIBRIUM MASTER DASHBOARD</h1>", unsafe_allow_html=True)

st.markdown(f"""<div class='google-window'>
    <b style='color:#4285f4; font-size:1.1rem;'>🌐 Google Intelligence Live Feed: {hotel_name} | {city_name}</b><br>
    • <b>Market State:</b> {m_state} | <b>Strategic Multiplier:</b> {m_heat}x<br>
    • <b>Events:</b> {active_intel['ev']} | <b>Flights:</b> {active_intel['fl']} | <b>Basis:</b> {active_intel['basis']}
</div>""", unsafe_allow_html=True)

def draw_seg(label, key, suggest_adr, floor_def, color, is_ota=False, group=False):
    rk = str(st.session_state["reset_key"])
    st.markdown(f"<div class='card' style='border-left-color:{color}'>{label}</div>", unsafe_allow_html=True)
    c_in, c_res = st.columns([2.6, 1])
    with c_in:
        st.markdown("<div class='pricing-row'>", unsafe_allow_html=True)
        r1, r2, r3, r4 = st.columns(4)
        sgl = r1.number_input("SGL", 0, key="s"+key+rk); dbl = r2.number_input("DBL", 0, key="d"+key+rk)
        applied_adr = r3.number_input("Applied Rate", value=float(suggest_adr * m_heat * v_mult), key="a"+key+rk)
        floor = r4.number_input("Floor Amount", value=float(floor_def), key="f"+key+rk)
        
        m_row = st.columns(6)
        p_ro = m_row[0].number_input("RO", 0, key="ro"+key+rk); p_bb = m_row[1].number_input("BB", 0, key="bb"+key+rk)
        p_hb = m_row[2].number_input("HB", 0, key="hb"+key+rk); p_fb = m_row[3].number_input("FB", 0, key="fb"+key+rk)
        p_sai = m_row[4].number_input("SAI", 0, key="sai"+key+rk); p_ai = m_row[5].number_input("AI", 0, key="ai"+key+rk)
        
        l_c, m_c, t_c = 0.0, 0.0, 0.0
        if group:
            st.markdown("<p style='font-size:0.8rem; font-weight:bold; color:#1e3799; margin-bottom:-10px;'>Group Ancillary Revenue / Extra Costs</p>", unsafe_allow_html=True)
            g_row = st.columns(3)
            m_c = g_row[0].number_input("MICE/Pax", 0.0, key="mice"+key+rk); t_c = g_row[1].number_input("Trans/Fixed", 0.0, key="tr"+key+rk); l_c = g_row[2].number_input("Laundry/Pax", 0.0, key="ln"+key+rk)
        st.markdown("</div>", unsafe_allow_html=True)
        
    res = run_yield([sgl, dbl], m_nights, applied_adr, {"RO":p_ro,"BB":p_bb,"HB":p_hb,"FB":p_fb,"SAI":p_sai,"AI":p_ai}, floor, (ota_comm/100 if is_ota else 0.0), l_c, m_c, t_c)
    if res:
        with c_res:
            st.metric("Net Wealth (Unit)", f"OMR {res['w']:,.2f}")
            st.markdown(f"<div class='status-indicator' style='background:{res['cl']}'>{res['st']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='audit-box'>📊 {res['rn']} Room Nights | Segment Wealth: OMR {res['total']:,.2f}</div>", unsafe_allow_html=True)

# DRAW SEGMENTS
draw_seg("1. DIRECT / FIT", "fit", 65, 40, "#3498db")
draw_seg("2. OTA CHANNELS", "ota", 60, 35, "#2ecc71", is_ota=True)
draw_seg("3. CORPORATE GROUPS", "corp", 55, 32, "#34495e", group=True)
draw_seg("4. MICE GROUPS", "mice", 50, 30, "#9b59b6", group=True)
draw_seg("5. TOUR & TRAVEL (GROUPS)", "tnt", 45, 25, "#e67e22", group=True)

# --- 7. FINAL DESCRIPTION MANUAL ---
st.divider()
st.markdown("<div class='theory-box'>", unsafe_allow_html=True)
st.markdown(f"## 📘 Theoretical Methodology & Research Framework (Live Tax Basis: {tx_div})")
cl1, cl2 = st.columns(2)
with cl1:
    st.markdown(f"""
    ### 🏗️ Pillar 01: Internal Wealth Stripping
    * **The Logic:** Gross ADR is a 'vanity metric.' We calculate **Net Wealth** to reveal true profitability.
    * **The Formula:** Strips Taxes (Applied Divisor: **{tx_div}**), Distribution Fees ({ota_comm}%), and variable P01 Fees.
    * **Board Basis:** Integrates all 6 meal board bases to ensure food costs are stripped before declaring success.
    """)
with cl2:
    st.markdown(f"""
    ### 🌐 Pillar 02 & 03: External Velocity
    * **Market Sentinel (P02):** Dynamic demand identification. **Compression** allows for maximum inventory capture.
    * **Velocity Valve (P03):** Compares OTB (Current Pace) to History to trigger automated yield protection multipliers.
    """)
st.markdown("</div>", unsafe_allow_html=True)
