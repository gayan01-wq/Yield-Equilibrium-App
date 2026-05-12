import streamlit as st
from datetime import date

# --- 1. SETTINGS & STYLING ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium Displacement Analyzer")

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

# --- 2. AUTHENTICATION & RESET ---
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

# --- 3. SIDEBAR (MASTER COSTS & CONFIG) ---
rk = str(st.session_state["reset_key"])
with st.sidebar:
    st.markdown("### 🏨 Property Profile")
    h_name = st.text_input("Hotel Name", value="", placeholder="e.g. Wyndham Garden Salalah", key="h_nm_"+rk)
    h_cap = st.number_input("Total Capacity", min_value=1, value=237, step=1, key="cap_"+rk)
    city_search = st.text_input("📍 Market Location", value="", placeholder="e.g. Salalah", key="city_"+rk)
    
    st.divider()
    st.markdown("### 📅 Stay Period")
    d1 = st.date_input("Check-In", date.today(), key="d_in_"+rk)
    d2 = st.date_input("Check-Out", date.today(), key="d_out_"+rk)
    m_nights = (d2 - d1).days if (d2 - d1).days > 0 else 1
    st.info(f"Stay Duration: {m_nights} Night(s)")

    st.divider()
    st.markdown("### 🏛️ Pillars Setup")
    tx_div = st.number_input("Tax Divisor", value=1.2327, format="%.4f", key="tx_v_"+rk)
    p01_fee = st.number_input("P01 Fee", value=6.00, step=0.1, key="p01_v_"+rk)

    st.markdown("### 🍽️ Meal Plan Cost (PP)")
    c_bf = st.number_input("BF Cost (PP)", min_value=0.0, value=2.00, key="bf_mc_"+rk)
    c_ln = st.number_input("LN Cost (PP)", min_value=0.0, value=3.00, key="ln_mc_"+rk)
    c_dn = st.number_input("DN Cost (PP)", min_value=0.0, value=5.00, key="dn_mc_"+rk)
    c_sai = st.number_input("SAI Cost (PP)", min_value=0.0, value=12.00, key="sai_mc_"+rk)
    c_ai = st.number_input("AI Cost (PP)", min_value=0.0, value=15.00, key="ai_mc_"+rk)

    if st.button("🗑️ Reset Protocol Data", use_container_width=True, type="primary"):
        clear_protocol_data()
        st.rerun()

# --- 4. MARKET INTEL ENGINE ---
intel_db = {
    "salalah": {"ev": "Khareef Festival Season", "fl": "OmanAir/SalamAir Peak", "news": "Monsoon Tourism Surge expected.", "demand": "Compression"},
    "muscat": {"ev": "Business Summit", "fl": "International Hub Stable", "news": "MICE demand up 15%.", "demand": "High Flow"}
}
active_intel = intel_db.get(city_search.lower(), {"ev": "Market Rotation", "fl": "Standard Flights", "news": "Standard flow stable.", "demand": "Standard"})

# --- 5. CALCULATION ENGINE ---
def run_segment_yield(adr, room_counts, base_hurdle, demand_type, total_rooms, comm_rate=0.0, laundry=0.0, ancillary_prpn=0.0):
    v_mult = {"Compression (Peak)": 1.25, "High Flow": 1.10, "Standard": 1.0, "Distressed": 0.85}.get(demand_type, 1.0)
    d_hurdle = base_hurdle * {"Compression (Peak)": 2.5, "High Flow": 1.5, "Standard": 1.0, "Distressed": 0.7}.get(demand_type, 1.0)
    
    net_adr = (adr * v_mult) / tx_div
    total_meal_cost = (
        (room_counts['BB'] * c_bf) +
        (room_counts['HB'] * (c_bf + c_dn)) +
        (room_counts['FB'] * (c_bf + c_ln + c_dn)) +
        (room_counts['SAI'] * c_sai) +
        (room_counts['AI'] * c_ai)
    )
    meal_per_room = total_meal_cost / max(total_rooms, 1)
    
    ancillary_net = ancillary_prpn / tx_div # Per room per night charge
    comm_outflow = net_adr * (comm_rate / 100)
    
    unit_w = (net_adr + ancillary_net) - (meal_per_room + comm_outflow + p01_fee + laundry)
    
    stt, clr = ("ACCEPT: OPTIMIZED", "#27ae60") if unit_w >= d_hurdle else ("REJECT: DILUTIVE", "#e74c3c")
    if d_hurdle <= unit_w < (d_hurdle + 5): stt, clr = ("REVIEW: MARGINAL", "#f39c12")
    
    # Basis Logic
    mp_basis = "RO"
    for plan in ["AI", "SAI", "FB", "HB", "BB"]:
        if room_counts.get(plan, 0) > 0:
            mp_basis = plan
            break

    return {"w": unit_w, "st": stt, "cl": clr, "dh": d_hurdle, "noi": unit_w * total_rooms * m_nights, "mp": mp_basis, "vm": v_mult}

# --- 6. DASHBOARD TOP ---
display_title = h_name if h_name else "New Property Analysis"
st.markdown(f"<h1 class='main-title'>{display_title.upper()}</h1>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center; color:#4b6584; font-weight:700; margin-bottom:20px;'>Yield Equilibrium Strategic Intelligence Engine</div>", unsafe_allow_html=True)

st.markdown(f"""
<div class='google-window'>
    <b>🌐 Market Intelligence: {city_search if city_search else 'Location Pending'} | {date.today().strftime('%B %Y')}</b><br>
    • <b>Aviation Situation:</b> {active_intel['fl']} | <b>Special Events:</b> {active_intel['ev']}<br>
    • <b>Special News Feed:</b> {active_intel['news']} | <b>Market Pulse:</b> {active_intel['demand']} Logic Applied.
</div>
""", unsafe_allow_html=True)

# --- 7. SEGMENT AUDITS ---
segments = [
    {"label": "1. DIRECT / FIT", "key": "fit", "color": "#3498db", "hurdle": 45.0, "ota": False, "group": False},
    {"label": "2. OTA CHANNELS", "key": "ota", "color": "#2ecc71", "hurdle": 35.0, "ota": True, "group": False},
    {"label": "3. GROUPS / MICE / TOURS", "key": "group", "color": "#34495e", "hurdle": 25.0, "ota": False, "group": True}
]

for seg in segments:
    if st.checkbox(f"Activate {seg['label']}", value=True, key=f"act_{seg['key']}_{rk}"):
        st.markdown(f"<div class='card' style='border-left-color:{seg['color']}'>{seg['label']}</div>", unsafe_allow_html=True)
        with st.container():
            st.markdown("<div class='pricing-row'>", unsafe_allow_html=True)
            
            c_ota = st.slider("OTA Commission %", 0, 40, 15, key=f"c_{seg['key']}_{rk}") if seg['ota'] else 0.0

            r1 = st.columns([1, 0.5, 0.5, 0.5, 0.5, 1.2, 1.2])
            g_rate = r1[0].number_input("Gross Rate", value=75.0, key=f"adr_{seg['key']}_{rk}")
            sgl, dbl, tpl, qrpl = r1[1].number_input("SGL", 0, key=f"s_{seg['key']}_{rk}"), r1[2].number_input("DBL", 0, key=f"d_{seg['key']}_{rk}"), r1[3].number_input("TPL", 0, key=f"t_{seg['key']}_{rk}"), r1[4].number_input("QRPL", 0, key=f"q_{seg['key']}_{rk}")
            total_rooms = sgl + dbl + tpl + qrpl
            demand_sel = r1[5].selectbox("Market Demand", ["Compression (Peak)", "High Flow", "Standard", "Distressed"], key=f"dm_{seg['key']}_{rk}")
            h_base = r1[6].number_input("Base Hurdle", value=seg['hurdle'], key=f"hrd_{seg['key']}_{rk}")

            r2 = st.columns([0.6, 0.6, 0.6, 0.6, 0.6, 1.1, 1.1, 1.1])
            bb_r, hb_r, fb_r, sai_r, ai_r = r2[0].number_input("BB", 0, key=f"bb_{seg['key']}_{rk}"), r2[1].number_input("HB", 0, key=f"hb_{seg['key']}_{rk}"), r2[2].number_input("FB", 0, key=f"fb_{seg['key']}_{rk}"), r2[3].number_input("SAI", 0, key=f"sai_{seg['key']}_{rk}"), r2[4].number_input("AI", 0, key=f"ai_{seg['key']}_{rk}")
            
            # Ancillary Revenue logic (PRPN)
            anc_rev = r2[5].number_input("Ancillary Revenue (PRPN)", value=0.0, key=f"anc_{seg['key']}_{rk}") if seg['group'] else 0.0
            laundry = r2[6].number_input("Laundry Cost", value=0.0, key=f"lnd_{seg['key']}_{rk}")
            other = r2[7].number_input("Other Fees", value=0.0, key=f"oth_{seg['key']}_{rk}")

            res = run_segment_yield(g_rate, {"BB":bb_r,"HB":hb_r,"FB":fb_r,"SAI":sai_r,"AI":ai_r}, h_base, demand_sel, total_rooms, comm_rate=c_ota, laundry=laundry+other, ancillary_prpn=anc_rev)
            
            v_cols = st.columns([1, 1.5, 1])
            v_cols[0].metric("Net Wealth (Unit)", f"﷼ {res['w']:,.2f}", delta=f"{res['vm']}x Velocity")
            v_cols[1].markdown(f"<div class='status-indicator' style='background:{res['cl']}'>{res['st']} ({res['mp']})</div>", unsafe_allow_html=True)
            v_cols[2].markdown(f"<div style='text-align:right;'><span class='noi-badge'>Total NOI: ﷼ {res['noi']:,.2f}</span></div>", unsafe_allow_html=True)
            
            st.markdown(f"<div class='reason-box'>💡 <b>Strategic Reasoning:</b> Basis: {res['mp']} | Eff. Hurdle: ﷼{res['dh']:,.2f} | Night Count: {m_nights}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

# --- 8. PILLARS FRAMEWORK ---
st.divider()
st.markdown("<div class='theory-box'>", unsafe_allow_html=True)
st.markdown("<h3 style='color:#1e3799; margin-top:0;'>THE YIELD EQUILIBRIUM STRATEGIC FRAMEWORK</h3>", unsafe_allow_html=True)
c_a, c_b, c_c = st.columns(3)
with c_a:
    st.markdown("<span class='pillar-header'>🏛️ Pillar 01: Internal Wealth Stripping</span>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:0.85rem; color:#4b6584;'>Strips statutory taxes (1.2327), commissions, and incremental meal costs to isolate <b>Net-Core Wealth</b> per room.</p>", unsafe_allow_html=True)
with c_b:
    st.markdown("<span class='pillar-header'>⚖️ Pillar 02: Dynamic Hurdle Equilibrium</span>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:0.85rem; color:#4b6584;'>Protects high-demand inventory by scaling hurdles up to 2.5x during Peak cycles to ensure optimal asset utilization.</p>", unsafe_allow_html=True)
with c_c:
    st.markdown("<span class='pillar-header'>🌐 Pillar 03: External Velocity</span>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:0.85rem; color:#4b6584;'>Integrates local aviation flow and special events data to apply real-time demand multipliers to the gross rate.</p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
