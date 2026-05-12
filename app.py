import streamlit as st
from datetime import date

# --- 1. SETTINGS & STYLING ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium Strategic Intelligence Engine")

st.markdown("""<style>
.block-container{padding-top:1rem!important; padding-bottom:0rem!important;}
.main-title { font-size: 2.2rem!important; font-weight: 900; color: #1e3799; text-align: center; text-transform: uppercase; margin-bottom: -5px; }
.card{padding:10px; border-radius:10px; margin-bottom:5px; border-left:10px solid; background:#ffffff; box-shadow: 0 2px 4px rgba(0,0,0,0.05)}
.pricing-row{background:#f8faff; padding:15px; border-radius:12px; border:1px solid #d1d9e6; margin-top:2px;}
.google-window{background:#e8f0fe; padding:15px; border-radius:12px; border:2px solid #4285f4; margin-bottom:15px; font-size:0.88rem; line-height:1.5;}
.status-indicator{padding:12px; border-radius:8px; text-align:center; font-weight:900; font-size:1.1rem; color:white; margin-top:10px; display:block;}
.reason-box{background:#fff9c4; border:1px solid #fbc02d; padding:10px; border-radius:8px; margin-top:8px; text-align:left; font-weight:500; color:#5f4300; font-size:0.8rem;}
.noi-badge{background:#1e3799; color:white; padding:8px 12px; border-radius:8px; font-weight:700; font-size:1rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1);}
.theory-box { background-color: #f1f4f9; padding: 25px; border-radius: 15px; border: 1px solid #d1d9e6; margin-top: 35px; }
.pillar-header { color: #1e3799; font-weight: 800; font-size: 1rem; text-transform: uppercase; margin-bottom: 5px; display: block; }
</style>""", unsafe_allow_html=True)

# --- 2. AUTHENTICATION ---
if "auth" not in st.session_state: st.session_state["auth"] = False
if "reset_key" not in st.session_state: st.session_state["reset_key"] = 0

if not st.session_state["auth"]:
    st.markdown("<h1 class='main-title'>EQUILIBRIUM ENGINE</h1>", unsafe_allow_html=True)
    with st.form("login_gate"):
        pwd = st.text_input("Access Key", type="password")
        if st.form_submit_button("Unlock"):
            if pwd == "Gayan2026": 
                st.session_state["auth"] = True
                st.rerun()
    st.stop()

def clear_protocol_data():
    st.session_state["reset_key"] += 1
    for key in list(st.session_state.keys()):
        if key not in ["auth", "reset_key"]: del st.session_state[key]

# --- 3. SIDEBAR (COST CENTER) ---
rk = str(st.session_state["reset_key"])
with st.sidebar:
    st.markdown("### 🏨 Property Profile")
    h_name = st.text_input("Hotel Name", value="", placeholder="e.g. Wyndham Garden Salalah", key="h_nm_"+rk)
    city_search = st.text_input("📍 Market Location", value="", placeholder="e.g. Salalah", key="city_"+rk)
    
    st.divider()
    st.markdown("### 📅 Stay Period (LOS)")
    d1 = st.date_input("Check-In", date.today(), key="d_in_"+rk)
    d2 = st.date_input("Check-Out", date.today(), key="d_out_"+rk)
    m_nights = (d2 - d1).days if (d2 - d1).days > 0 else 1
    st.info(f"Length of Stay: {m_nights} Night(s)")

    st.divider()
    st.markdown("### 🏛️ Pillars Setup")
    tx_div = st.number_input("Tax Divisor", value=1.2327, format="%.4f", key="tx_v_"+rk)
    p01_fee = st.number_input("P01 Fee (Per Room)", value=6.00, step=0.1, key="p01_v_"+rk)

    # Reference: image_d3dbba.png & image_d3d496.png
    st.markdown("### 🍽️ Meal Plan Cost (PP)")
    c_bf = st.number_input("BF Cost (PP)", value=2.00, key="bf_mc_"+rk)
    c_ln = st.number_input("LN Cost (PP)", value=3.00, key="ln_mc_"+rk)
    c_dn = st.number_input("DN Cost (PP)", value=5.00, key="dn_mc_"+rk)
    c_sai = st.number_input("SAI Cost (PP)", value=12.00, key="sai_mc_"+rk)
    c_ai = st.number_input("AI Cost (PP)", value=15.00, key="ai_mc_"+rk)

    if st.button("🗑️ Reset Engine", use_container_width=True, type="primary"):
        clear_protocol_data()
        st.rerun()

# --- 4. MARKET INTEL ---
intel_db = {
    "salalah": {"ev": "Khareef Season", "fl": "OmanAir Peak", "news": "Monsoon Surge.", "demand": "Compression"},
    "muscat": {"ev": "Business Summit", "fl": "Hub Stable", "news": "MICE demand up.", "demand": "High Flow"}
}
active_intel = intel_db.get(city_search.lower(), {"ev": "Stable", "fl": "Normal", "news": "Stable.", "demand": "Standard"})

# --- 5. LOGIC ENGINE (STRATEGIC AUDIT) ---
def run_equilibrium_engine(adr, room_counts, base_hurdle, demand, total_rooms, comm_rate=0.0, anc_prpn=0.0, laundry=0.0):
    # Velocity Multiplier is 1.0 to ensure NOI accuracy to input
    vm = 1.0 
    
    # Dynamic Hurdle Scaling (Target Equilibrium)
    # Reference: Strategic Reasoning in image_d3e337.png
    dh = base_hurdle * {"Compression (Peak)": 2.5, "High Flow": 1.5, "Standard": 1.0, "Distressed": 0.7}.get(demand, 1.0)
    
    # Net ADR
    net_adr = adr / tx_div
    
    # Meal Calculation based on Room Selection
    # Logic: Room count * (Individual Cost Component sum)
    meal_sum = (
        (room_counts['BB'] * c_bf) +
        (room_counts['HB'] * (c_bf + c_dn)) +
        (room_counts['FB'] * (c_bf + c_ln + c_dn)) +
        (room_counts['SAI'] * c_sai) +
        (room_counts['AI'] * c_ai)
    )
    # Average meal cost per occupied room
    meal_unit = meal_sum / max(total_rooms, 1)
    
    # Ancillary Revenue (Per Room Per Night)
    anc_net = anc_prpn / tx_div
    
    # Commission (Stripped from Net ADR)
    comm_val = net_adr * (comm_rate / 100)
    
    # UNIT NET WEALTH (Pillar 01)
    # Formula: Core Margin = (Revenue - Direct Variable Costs - Fees)
    unit_w = (net_adr + anc_net) - (meal_unit + comm_val + p01_fee + laundry)
    
    # Acceptance Matrix
    if unit_w < dh: 
        stt, clr, rsn = "REJECT: DILUTIVE", "#e74c3c", "Wealth below market equilibrium."
    elif unit_w < (dh + 5.0): 
        stt, clr, rsn = "REVIEW: MARGINAL", "#f39c12", "At hurdle equilibrium threshold."
    else: 
        stt, clr, rsn = "ACCEPT: OPTIMIZED", "#27ae60", "Wealth targets successfully achieved."
    
    # MP Basis Display Logic
    mp_basis = "RO"
    for p in ["AI", "SAI", "FB", "HB", "BB"]:
        if room_counts.get(p, 0) > 0: mp_basis = p; break

    # NOI: Wealth * Total Rooms * LOS
    total_noi = unit_w * total_rooms * m_nights
    
    return {"w": unit_w, "st": stt, "cl": clr, "dh": dh, "noi": total_noi, "mp": mp_basis, "rsn": rsn}

# --- 6. DASHBOARD MAIN ---
st.markdown(f"<h1 class='main-title'>{h_name.upper() if h_name else 'YIELD ENGINE'}</h1>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center; color:#4b6584; font-weight:700; margin-bottom:20px;'>Yield Equilibrium Strategic Intelligence Engine</div>", unsafe_allow_html=True)

st.markdown(f"""
<div class='google-window'>
    <b>🌐 Market Intelligence: {city_search if city_search else 'Location Pending'} | {date.today().strftime('%B %Y')}</b><br>
    • <b>Aviation Situation:</b> {active_intel['fl']} | <b>Special Events:</b> {active_intel['ev']}<br>
    • <b>Special News Feed:</b> {active_intel['news']} | <b>Market Pulse:</b> {active_intel['demand']} Logic Applied.
</div>
""", unsafe_allow_html=True)

# Define Audited Segments
segments = [
    {"label": "1. DIRECT / FIT", "key": "fit", "color": "#3498db", "hurdle": 45.0, "ota": False, "grp": False},
    {"label": "2. OTA CHANNELS", "key": "ota", "color": "#2ecc71", "hurdle": 35.0, "ota": True, "grp": False},
    {"label": "3. GROUPS / MICE / TOURS", "key": "grp", "color": "#34495e", "hurdle": 25.0, "ota": False, "grp": True}
]

for seg in segments:
    if st.checkbox(f"Activate {seg['label']}", value=True, key=f"act_{seg['key']}"):
        st.markdown(f"<div class='card' style='border-left-color:{seg['color']}'>{seg['label']}</div>", unsafe_allow_html=True)
        with st.container():
            st.markdown("<div class='pricing-row'>", unsafe_allow_html=True)
            
            # Commission Bar (OTA Only)
            c_rate = st.slider("Commission %", 0, 40, 15, key=f"c_{seg['key']}") if seg['ota'] else 0.0

            # Row 1: Rooms, ADR & Hurdle
            r1 = st.columns([1, 0.5, 0.5, 0.5, 0.5, 1.2, 1.2])
            g_adr = r1[0].number_input("Gross Rate", value=75.0, key=f"a_{seg['key']}")
            s, d, t, q = r1[1].number_input("SGL", 0, key=f"s_{seg['key']}"), r1[2].number_input("DBL", 0, key=f"d_{seg['key']}"), r1[3].number_input("TPL", 0, key=f"t_{seg['key']}"), r1[4].number_input("QRPL", 0, key=f"q_{seg['key']}")
            t_rooms = s + d + t + q
            dem = r1[5].selectbox("Market Demand", ["Compression (Peak)", "High Flow", "Standard", "Distressed"], key=f"dm_{seg['key']}")
            h_b = r1[6].number_input("Base Hurdle", value=seg['hurdle'], key=f"h_{seg['key']}")

            # Row 2: Meal Basis & Ancillary (PRPN)
            # Reference: image_d3e337.png Highlighted Row
            r2 = st.columns([0.6, 0.6, 0.6, 0.6, 0.6, 1.1, 1.1, 1.1])
            bb, hb, fb, sai, ai = r2[0].number_input("BB", 0, key=f"bb_{seg['key']}"), r2[1].number_input("HB", 0, key=f"hb_{seg['key']}"), r2[2].number_input("FB", 0, key=f"fb_{seg['key']}"), r2[3].number_input("SAI", 0, key=f"sai_{seg['key']}"), r2[4].number_input("AI", 0, key=f"ai_{seg['key']}")
            
            # Ancillary Revenue (PRPN) for Groups
            anc = r2[5].number_input("Ancillary Revenue (PRPN)", value=0.0, key=f"anc_{seg['key']}") if seg['grp'] else 0.0
            lnd = r2[6].number_input("Laundry/Room", value=0.0, key=f"l_{seg['key']}")
            oth = r2[7].number_input("Other Fees", value=0.0, key=f"o_{seg['key']}")

            # Logic Run
            res = run_equilibrium_engine(g_adr, {"BB":bb,"HB":hb,"FB":fb,"SAI":sai,"AI":ai}, h_b, dem, t_rooms, comm_rate=c_rate, anc_prpn=anc, laundry=lnd+oth)
            
            # Metrics Row
            v = st.columns([1, 1.5, 1])
            v[0].metric("Net Wealth (Pillar 01)", f"﷼ {res['w']:,.2f}")
            v[1].markdown(f"<div class='status-indicator' style='background:{res['cl']}'>{res['st']} ({res['mp']})</div>", unsafe_allow_html=True)
            v[2].markdown(f"<div style='text-align:right;'><span class='noi-badge'>Total NOI: ﷼ {res['noi']:,.2f}</span></div>", unsafe_allow_html=True)
            
            # Reasoning Box
            st.markdown(f"<div class='reason-box'>💡 <b>Strategic Reasoning:</b> {res['rsn']} | <b>Basis:</b> {res['mp']} | <b>Effective Hurdle:</b> ﷼{res['dh']:,.2f}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

# --- 7. PILLARS FRAMEWORK ---
st.divider()
st.markdown("<div class='theory-box'>", unsafe_allow_html=True)
st.markdown("<h3 style='color:#1e3799; margin-top:0;'>THE YIELD EQUILIBRIUM STRATEGIC FRAMEWORK</h3>", unsafe_allow_html=True)
ca, cb, cc = st.columns(3)
with ca:
    st.markdown("<span class='pillar-header'>🏛️ Pillar 01: Internal Wealth Stripping</span>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:0.85rem; color:#4b6584;'>Strips statutory taxes, commissions, and meal costs to isolate <b>Net-Core Wealth</b> per unit.</p>", unsafe_allow_html=True)
with cb:
    st.markdown("<span class='pillar-header'>⚖️ Pillar 02: Dynamic Hurdle Equilibrium</span>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:0.85rem; color:#4b6584;'>Protects inventory by scaling hurdles (up to 2.5x) to ensure optimal asset utilization in Peak cycles.</p>", unsafe_allow_html=True)
with cc:
    st.markdown("<span class='pillar-header'>🌐 Pillar 03: Market Intelligence Integration</span>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:0.85rem; color:#4b6584;'>Cross-references aviation flow and special event data with deal profitability to guide acceptance logic.</p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
