import streamlit as st
from datetime import date

# --- 1. SETTINGS & STYLING ---
st.set_page_config(layout="wide", page_title="Universal Yield Equilibrium Engine")

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
.pillar-header { color: #1e3799; font-weight: 800; font-size: 1.1rem; text-transform: uppercase; margin-bottom: 8px; display: block; border-bottom: 2px solid #1e3799; padding-bottom: 4px;}
.alert-box { background-color: #ffeded; border: 1px solid #ff4b4b; color: #ff4b4b; padding: 15px; border-radius: 8px; font-weight: bold; margin-bottom: 15px; border-left: 10px solid #ff4b4b;}
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

# --- 3. SIDEBAR (CONTEXTUAL DATA) ---
rk = str(st.session_state["reset_key"])
with st.sidebar:
    st.markdown("### 🏨 Hotel Profile")
    h_name = st.text_input("Hotel Name", "Wyndham Garden Salalah", key="h_nm_"+rk)
    h_cap = st.number_input("Total Capacity", min_value=1, value=237, step=1, key="cap_"+rk)
    city_search = st.text_input("📍 Market Location", "Salalah", key="city_"+rk)
    
    st.divider()
    st.markdown("### 📅 Stay Period")
    d1 = st.date_input("Check-In", date.today(), key="d_in_"+rk)
    d2 = st.date_input("Check-Out", date(2026, 5, 12), key="d_out_"+rk)
    m_nights = (d2 - d1).days if (d2 - d1).days > 0 else 1
    los_type = "Long Stay (5+ Nights)" if m_nights >= 5 else "Short Stay"
    st.info(f"Stay Duration: {m_nights} Nights | {los_type}")

    st.divider()
    st.markdown("### 🌍 Global Currency Suite")
    currencies = {
        "OMR (﷼)": "﷼", "AED (د.إ)": "د.إ", "SAR (﷼)": "﷼", "QAR (﷼)": "﷼", "BHD (.د)": ".د", "KWD (د.ك)": "د.ك",
        "USD ($)": "$", "EUR (€)": "€", "GBP (£)": "£", "LKR (රු)": "රු", "INR (₹)": "₹", "CHF (CHF)": "CHF"
    }
    cur_sym = currencies[st.selectbox("Select Currency", list(currencies.keys()), key="c_sel_"+rk)]

    st.divider()
    st.markdown("### 🏛️ Pillars Setup")
    tax_input = st.text_input("Tax Divisor Formula", value="1.2327", key="tx_v_"+rk)
    try:
        current_tax_divisor = float(eval(tax_formula)) if tax_input else 1.2327
    except:
        current_tax_divisor = 1.2327
    
    p01_fee = st.number_input(f"P01 Fee ({cur_sym})", value=6.00, step=0.1, key="p01_v_"+rk)

    st.markdown("### 🍽️ Meal Plan Cost (PP)")
    meal_costs = {
        "BF": st.number_input("Breakfast (BF)", value=2.00, step=0.5, key="bf_mc_"+rk),
        "LN": st.number_input("Lunch (LN)", value=0.0, step=0.5, key="ln_mc_"+rk),
        "DN": st.number_input("Dinner (DN)", value=0.0, step=0.5, key="dn_mc_"+rk),
        "SAI": st.number_input("Soft All-In (SAI)", value=0.0, step=0.5, key="sai_mc_"+rk),
        "AI": st.number_input("All-Inclusive (AI)", value=0.0, step=0.5, key="ai_mc_"+rk)
    }

# --- 4. ENGINE LOGIC ---
def run_segment_yield(adr, meal_qty, base_hurdle, demand_type, is_group, total_rooms, comm_rate=0.0, mice=0.0, laundry=0.0, transport=0.0):
    v_mult = {"Compression (Peak)": 1.25, "High Flow": 1.15, "Standard": 1.0, "Distressed": 0.85}.get(demand_type, 1.0)
    
    # Identify Meal Basis
    bf, ln, dn, sai, ai = meal_qty.get("BF", 0), meal_qty.get("LN", 0), meal_qty.get("DN", 0), meal_qty.get("SAI", 0), meal_qty.get("AI", 0)
    if ai > 0: mp_basis = "AI"
    elif sai > 0: mp_basis = "SAI"
    elif bf > 0 and ln > 0 and dn > 0: mp_basis = "FB"
    elif bf > 0 and dn > 0: mp_basis = "HB"
    elif bf > 0: mp_basis = "BB"
    else: mp_basis = "RO"

    dynamic_hurdle = base_hurdle * {"Compression (Peak)": 2.5, "High Flow": 1.7, "Standard": 1.0, "Distressed": 0.65}.get(demand_type, 1.0)
    
    net_adr = (adr * v_mult) / current_tax_divisor
    total_meal_cost = sum(qty * meal_costs.get(p, 0) for p, qty in meal_qty.items())
    
    divisor = max(total_rooms, 10) if is_group else max(total_rooms, 1)
    group_rev = (mice / current_tax_divisor) + ((transport / current_tax_divisor) / divisor) if is_group else 0
    
    unit_w = (net_adr + group_rev - total_meal_cost - (net_adr * (comm_rate/100))) - p01_fee - laundry
    
    if unit_w < dynamic_hurdle: stt, clr = "REJECT: DILUTIVE", "#e74c3c"
    elif unit_w < (dynamic_hurdle + 5.0): stt, clr = "REVIEW: MARGINAL", "#f39c12"
    else: stt, clr = "ACCEPT: OPTIMIZED", "#27ae60"
        
    total_noi = unit_w * divisor * m_nights
    return {"w": unit_w, "st": stt, "cl": clr, "vm": v_mult, "dh": dynamic_hurdle, "noi": total_noi, "basis": mp_basis}

# --- 5. TOP DASHBOARD ---
st.markdown(f"<h1 class='main-title'>{h_name.upper()}</h1>", unsafe_allow_html=True)
intel_db = {"salalah": {"ev": "Khareef Season", "fl": "OmanAir Peak", "dm": "Compression"}, "muscat": {"ev": "Business Summit", "fl": "Hub Stable", "dm": "High Flow"}}
intel = intel_db.get(city_search.lower(), {"ev": "Standard Rotation", "fl": "Stable", "dm": "Standard"})

st.markdown(f"""<div class='google-window'><b>🌐 Market Intelligence: {city_search} | {date.today().strftime('%B %Y')}</b><br>
• <b>Events:</b> {intel['ev']} | <b>Market Pulse:</b> {intel['dm']} Logic Applied.</div>""", unsafe_allow_html=True)

# --- 6. SEGMENT AUDITS ---
segments = [
    {"label": "1. DIRECT / FIT", "key": "fit", "color": "#3498db", "ota": False, "hurdle": 45.0, "group": False},
    {"label": "2. OTA CHANNELS", "key": "ota", "color": "#2ecc71", "ota": True, "hurdle": 35.0, "group": False},
    {"label": "3. CORPORATE / MICE GROUPS", "key": "mice", "color": "#34495e", "ota": False, "hurdle": 32.0, "group": True},
    {"label": "4. GROUP TOUR & TRAVEL", "key": "tnt", "color": "#e67e22", "ota": False, "hurdle": 12.0, "group": True}
]

total_simulated_rooms = 0
for seg in segments:
    if st.checkbox(f"Activate {seg['label']}", value=True, key=f"act_{seg['key']}_{rk}"):
        st.markdown(f"<div class='card' style='border-left-color:{seg['color']}'>{seg['label']}</div>", unsafe_allow_html=True)
        with st.container():
            st.markdown("<div class='pricing-row'>", unsafe_allow_html=True)
            r1 = st.columns([1, 1, 0.8, 1, 1.2])
            g_rate = r1[0].number_input(f"Gross Rate", value=75.0, key=f"adr_{seg['key']}_{rk}")
            rooms_total = r1[1].number_input("Rooms Requested", 1, key=f"rms_{seg['key']}_{rk}")
            total_simulated_rooms += rooms_total
            demand_sel = r1[2].selectbox("Market Demand", ["Standard", "High Flow", "Compression (Peak)", "Distressed"], key=f"dm_{seg['key']}_{rk}")
            h_base = r1[3].number_input("Base Hurdle", value=seg['hurdle'], key=f"hrd_{seg['key']}_{rk}")
            c_ota = r1[4].slider("OTA Commission %", 0, 35, 15, key=f"comm_{seg['key']}_{rk}") if seg['ota'] else 0.0

            r2 = st.columns([0.6,0.6,0.6,0.6,0.6, 1.1, 1.1, 1.1])
            bf = r2[0].number_input("BB", 0, key=f"bf_in_{seg['key']}_{rk}")
            ln = r2[1].number_input("LN", 0, key=f"ln_in_{seg['key']}_{rk}")
            dn = r2[2].number_input("DN", 0, key=f"dn_in_{seg['key']}_{rk}")
            sai = r2[3].number_input("SAI", 0, key=f"sai_in_{seg['key']}_{rk}")
            ai = r2[4].number_input("AI", 0, key=f"ai_in_{seg['key']}_{rk}")
            m_pp = r2[5].number_input("Group Rev", 0.0, key=f"m_{seg['key']}_{rk}") if seg['group'] else 0.0
            l_pp = r2[6].number_input("Laundry", 0.0, key=f"l_{seg['key']}_{rk}")
            t_f = r2[7].number_input("Transport", 0.0, key=f"tr_{seg['key']}_{rk}")

            res = run_segment_yield(g_rate, {"BF":bf,"LN":ln,"DN":dn,"SAI":sai,"AI":ai}, h_base, demand_sel, seg['group'], rooms_total, c_ota, m_pp, l_pp, t_f)
            
            v_cols = st.columns([1, 1.5, 1])
            v_cols[0].metric("Net Wealth", f"{cur_sym} {res['w']:,.2f}", delta=f"{res['vm']}x Velocity")
            v_cols[1].markdown(f"<div class='status-indicator' style='background:{res['cl']}'>{res['st']} ({res['basis']})</div>", unsafe_allow_html=True)
            v_cols[2].markdown(f"<div style='text-align:right;'><span class='noi-badge'>Total NOI: {cur_sym} {res['noi']:,.2f}</span></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='reason-box'>💡 <b>Strategic Logic:</b> {los_type} | <b>Effective Hurdle:</b> {cur_sym}{res['dh']:,.2f}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

# --- 7. OCCUPANCY SEGMENTATION ALERT ---
occ_perc = (total_simulated_rooms / h_cap) * 100
if occ_perc >= 50:
    st.markdown(f"<div class='alert-box'>⚠️ HIGH OCCUPANCY WARNING: Simulation represents {occ_perc:.1f}% inventory. Displacement risk is CRITICAL. Increase hurdles to protect remaining yield.</div>", unsafe_allow_html=True)

# --- 8. PILLARS EXPLANATION ---
st.divider()
st.markdown("<div class='theory-box'><h2 style='color:#1e3799; text-align:center;'>THE YIELD EQUILIBRIUM STRATEGIC FRAMEWORK</h2>", unsafe_allow_html=True)
p1, p2, p3 = st.columns(3)
with p1:
    st.markdown("<span class='pillar-header'>🏛️ Pillar 01: Internal Wealth Stripping</span>", unsafe_allow_html=True)
    st.markdown("Isolates 'Pure Profit' by removing statutory taxes, channel commissions, and incremental costs (Meals/Laundry). It ensures volume does not hide losses.")
with p2:
    st.markdown("<span class='pillar-header'>⚖️ Pillar 02: Dynamic Hurdle Equilibrium</span>", unsafe_allow_html=True)
    st.markdown("Acts as the inventory gatekeeper. It scales entry price requirements based on demand compression to protect high-value last-minute demand.")
with p3:
    st.markdown("<span class='pillar-header'>🌐 Pillar 03: External Velocity</span>", unsafe_allow_html=True)
    st.markdown("Integrates real-time city-wide flow. Fast market pickup (Compression) increases the value of remaining rooms exponentially, requiring higher acceptance thresholds.")
st.markdown("</div>", unsafe_allow_html=True)
