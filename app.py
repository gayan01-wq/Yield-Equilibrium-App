import streamlit as st
from datetime import date

# --- 1. STYLING ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium Master")
st.markdown("""<style>
.block-container{padding-top:1rem!important;}
.main-title{font-size:1.8rem!important;font-weight:900;color:#1e3799;text-align:center;margin-top:-10px;}
.card{padding:10px;border-radius:10px;margin-bottom:8px;border-left:10px solid;background:#ffffff;box-shadow: 0 2px 4px rgba(0,0,0,0.1)}
.pricing-row{background:#f8faff;padding:12px;border-radius:10px;border:1px solid #d1d9e6; margin-top:5px;}
.google-window{background:#e8f0fe; padding:15px; border-radius:12px; border:2px solid #4285f4; margin-bottom:15px; font-size:0.85rem; line-height:1.6;}
.status-indicator{padding:10px; border-radius:10px; text-align:center; font-weight:900; font-size:1.2rem; color:white; margin-top:10px;}
.audit-box{background:#fff9c4; border:1px solid #fbc02d; padding:10px; border-radius:8px; margin-top:12px; text-align:center; font-weight:bold; color:#5f4300; font-size:0.9rem;}
[data-testid="stSidebar"]{background:#f1f4f9; border-right:1px solid #dee2e6}
</style>""", unsafe_allow_html=True)

# --- 2. SESSION STATE & RESET ---
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

# --- 3. SIDEBAR (STRATEGIC LEVERS) ---
with st.sidebar:
    st.markdown("### 👤 Strategic Architect\nGayan Nugawela")
    if st.button("☢️ Nuclear Data Reset"):
        st.session_state["reset_key"] += 1
        st.rerun()
    st.divider()
    
    rk = str(st.session_state["reset_key"]) 
    
    st.markdown("### 🏨 Pillar 01: Universal Search")
    hotel_name = st.text_input("🏨 Hotel Name", "Wyndham Garden Salalah", key="h"+rk)
    city_name = st.text_input("📍 City/Location", "Salalah, Oman", key="c"+rk)
    
    st.divider()
    d1 = st.date_input("Check-In", date.today(), key="d1"+rk)
    d2 = st.date_input("Check-Out", date.today(), key="d2"+rk)
    m_nights = (d2 - d1).days if (d2 - d1).days > 0 else 1
    st.success(f"**Stay Nights: {m_nights}**")
    
    st.divider()
    st.markdown("### 📊 Market Velocity (P03)")
    otb_occ = st.slider("OTB Occupancy %", 0, 100, 15, key="otb"+rk)
    avg_hist = st.slider("Historical Avg %", 0, 100, 45, key="hist"+rk)
    v_mult = 1.35 if otb_occ > avg_hist else 0.85 if otb_occ < (avg_hist - 20) else 1.0
    
    st.divider()
    tx_div = st.number_input("Tax Divisor", value=1.2327, format="%.4f", key="tx"+rk)
    p01_fee = st.number_input("P01 Variable Fee", 0.0, value=6.90, key="p01"+rk)
    ota_comm = st.slider("OTA Commission %", 0, 40, 18, key="comm"+rk)

    st.markdown("### 🍽️ Unit Pax Costs")
    c_bb = st.number_input("BB Cost", 0.0, key="cbb"+rk)
    c_hb = st.number_input("HB Cost", 2.5, key="chb"+rk)
    c_sai = st.number_input("SAI Cost", 7.5, key="csai"+rk)
    meal_unit_costs = {"RO": 0, "BB": c_bb, "HB": c_hb, "FB": 5.0, "SAI": c_sai, "AI": 10.0}

# --- 4. GOOGLE INTELLIGENCE ENGINE (P02) ---
intel_db = {
    "Salalah": {"ev": "Khareef Tourism Festival", "fl": "+18% Surge (Oman Air/SalamAir)", "basis": "Seasonal Monsoonal Surge"},
    "Dubai": {"ev": "Dubai Shopping Festival / Expo", "fl": "+25% Global via Emirates/FlyDubai", "basis": "Peak Business/Leisure Synergy"},
    "Muscat": {"ev": "Muscat Food Festival / Opera Season", "fl": "+10% Regional Traffic", "basis": "Cultural High Season"},
    "London": {"ev": "Wimbledon / Fashion Week", "fl": "Heathrow Capacity Constraints", "basis": "Global Hub Demand Pressures"}
}
active_intel = next((v for k, v in intel_db.items() if k.lower() in city_name.lower()), 
                   {"ev": "Local Market Dynamics", "fl": "Standard Seasonal Traffic", "basis": "Baseline Market Equilibrium"})

# --- 5. CALCULATION ENGINE ---
def run_yield(rms, nts, adr, meals, hurdle, comm_rate=0.18, laundry=0, mice=0, trans=0):
    tr = sum(rms)
    if tr <= 0: return None
    rn = tr * nts
    net_adr = adr / tx_div
    total_m = sum(qty * meal_unit_costs.get(plan, 0) for plan, qty in meals.items())
    avg_m = (total_m / tr) if tr > 0 else 0
    # Wealth Stripping Math
    unit_w = (net_adr - avg_m - (net_adr * comm_rate)) - p01_fee - laundry + (mice / tx_div)
    total_w = (unit_w * rn) + (trans / tx_div)
    gross_rev = adr * rn
    status, color = ("OPTIMIZED", "#27ae60") if unit_w >= hurdle else ("DILUTIVE", "#e74c3c")
    return {"w": unit_w, "st": status, "cl": color, "rn": rn, "total": total_w, "gross": gross_rev}

# --- 6. MAIN DASHBOARD ---
st.markdown("<h1 class='main-title'>YIELD EQUILIBRIUM MASTER DASHBOARD</h1>", unsafe_allow_html=True)

st.markdown(f"""<div class='google-window'>
    <b style='color:#4285f4; font-size:1.1rem;'>🌐 Google Intelligence Live Feed: {hotel_name} | {city_name}</b><br>
    • <b>Strategic Events:</b> {active_intel['ev']} | <b>Flight Intel:</b> {active_intel['fl']}<br>
    • <b>Demand Basis:</b> {active_intel['basis']} | <b>Velocity Multiplier:</b> {v_mult}x Applied
</div>""", unsafe_allow_html=True)

def draw_seg(label, key, suggest_adr, floor_def, color, is_ota=False, group=False):
    rk = str(st.session_state["reset_key"])
    st.markdown(f"<div class='card' style='border-left-color:{color}'>{label}</div>", unsafe_allow_html=True)
    c_in, c_res = st.columns([2.6, 1])
    
    with c_in: # FIXED SYNTAX HERE
        st.markdown("<div class='pricing-row'>", unsafe_allow_html=True)
        r1, r2, r3, r4 = st.columns(4)
        sgl = r1.number_input("SGL", 0, key="s"+key+rk)
        dbl = r2.number_input("DBL", 0, key="d"+key+rk)
        applied_adr = r3.number_input("Rate", value=float(suggest_adr * v_mult), key="a"+key+rk)
        floor = r4.number_input("Floor", value=float(floor_def), key="f"+key+rk)
        
        m_row = st.columns(6)
        m_ro = m_row[0].number_input("RO", 0, key="ro"+key+rk); m_bb = m_row[1].number_input("BB", 0, key="bb"+key+rk)
        m_hb = m_row[2].number_input("HB", 0, key="hb"+key+rk); m_fb = m_row[3].number_input("FB", 0, key="fb"+key+rk)
        m_sai = m_row[4].number_input("SAI", 0, key="sai"+key+rk); m_ai = m_row[5].number_input("AI", 0, key="ai"+key+rk)
        
        l_c, m_c, t_c = 0.0, 0.0, 0.0
        if group:
            g_row = st.columns(3)
            m_c = g_row[0].number_input("MICE/Pax", 0.0, key="mice"+key+rk)
            t_c = g_row[1].number_input("Trans/Fixed", 0.0, key="tr"+key+rk)
            l_c = g_row[2].number_input("Laundry/Pax", 0.0, key="ln"+key+rk)
        st.markdown("</div>", unsafe_allow_html=True)
        
    res = run_yield([sgl, dbl], m_nights, applied_adr, {"RO":m_ro,"BB":m_bb,"HB":m_hb,"FB":m_fb,"SAI":m_sai,"AI":m_ai}, 
                    floor, (ota_comm/100 if is_ota else 0.0), l_c, m_c, t_c)
    if res:
        with c_res:
            st.metric("Net Yield (Unit)", f"OMR {res['w']:,.2f}")
            st.markdown(f"<div class='status-indicator' style='background:{res['cl']}'>{res['st']}</div>", unsafe_allow_html=True)
            # YELLOW AUDIT BOX
            st.markdown(f"""<div class='audit-box'>
                📊 Audit: {res['rn']} Room Nights<br>
                💰 Gross: OMR {res['gross']:,.2f}
            </div>""", unsafe_allow_html=True)

# DRAW SEGMENTS
draw_seg("1. DIRECT / FIT", "fit", 65, 40, "#3498db")
draw_seg("2. OTA CHANNELS", "ota", 60, 35, "#2ecc71", is_ota=True)
draw_seg("3. CORPORATE GROUPS", "corp", 55, 32, "#34495e", group=True)
draw_seg("4. MICE GROUPS", "mice", 50, 30, "#9b59b6", group=True)
draw_seg("5. TOUR & TRAVEL", "tnt", 45, 25, "#e67e22", group=True)
