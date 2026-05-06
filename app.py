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
.noi-badge{background:#1e3799; color:white; padding:4px 8px; border-radius:5px; font-weight:700; font-size:0.9rem;}
.theory-box { background-color: #f1f4f9; padding: 25px; border-radius: 15px; border: 1px solid #d1d9e6; margin-top: 35px; }
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
    st.markdown("### 🏨 Property Profile")
    h_name = st.text_input("Hotel Name", "Wyndham Garden Salalah", key="h_nm_"+rk)
    h_cap = st.number_input("Total Capacity", min_value=1, value=237, step=1, key="cap_"+rk)
    city_search = st.text_input("📍 Market Location", "Salalah", key="city_"+rk)
    
    st.divider()
    st.markdown("### 📅 Stay Period")
    d1 = st.date_input("Check-In", date.today(), key="d_in_"+rk)
    d2 = st.date_input("Check-Out", date.today(), key="d_out_"+rk)
    m_nights = (d2 - d1).days if (d2 - d1).days > 0 else 1
    st.info(f"Stay Duration: {m_nights} Nights")

    st.divider()
    currencies = {"OMR (﷼)": "﷼", "AED (د.إ)": "د.إ", "SAR (﷼)": "﷼", "LKR (රු)": "රු", "INR (₹)": "₹", "USD ($)": "$"}
    cur_sym = currencies[st.selectbox("Select Currency", list(currencies.keys()), key="c_sel_"+rk)]

    st.divider()
    tx_div = st.number_input("Tax Divisor", value=1.2327, format="%.4f", key="tx_v_"+rk)
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
    velocity_map = {"Compression (Peak)": 1.25, "High Flow": 1.10, "Standard": 1.0, "Distressed": 0.85}
    v_mult = velocity_map.get(demand_type, 1.0)
    
    hurdle_multiplier = {"Compression (Peak)": 2.5, "High Flow": 1.5, "Standard": 1.0, "Distressed": 0.7}
    dynamic_hurdle = base_hurdle * hurdle_multiplier.get(demand_type, 1.0)
    
    net_adr = (adr * v_mult) / tx_div
    total_meal_cost = sum(qty * meal_costs.get(p, 0) for p, qty in meal_qty.items())
    
    divisor = max(total_rooms, 10) if is_group else max(total_rooms, 1)
    group_rev = (mice / tx_div) + ((transport / tx_div) / divisor) if is_group else 0
    
    unit_w = (net_adr + group_rev - total_meal_cost - (net_adr * (comm_rate/100))) - p01_fee - laundry
    
    if unit_w < dynamic_hurdle: stt, clr, rsn = "REJECT: DILUTIVE", "#e74c3c", "Displaced by Dynamic Peak Hurdle."
    elif unit_w < (dynamic_hurdle + 5.0): stt, clr, rsn = "REVIEW: MARGINAL", "#f39c12", "At equilibrium window."
    else: stt, clr, rsn = "ACCEPT: OPTIMIZED", "#27ae60", "Wealth targets achieved."
        
    total_noi = unit_w * divisor * m_nights
    return {"w": unit_w, "st": stt, "cl": clr, "rsn": rsn, "vm": v_mult, "dh": dynamic_hurdle, "noi": total_noi}

# --- 5. TOP DASHBOARD ---
st.markdown(f"<h1 class='main-title'>{h_name.upper()}</h1>", unsafe_allow_html=True)
st.markdown("<div class='main-subtitle'>Yield Equilibrium Strategic Intelligence Engine</div>", unsafe_allow_html=True)

# --- 6. SEGMENT AUDITS ---
segments = [
    {"label": "1. DIRECT / FIT", "key": "fit", "color": "#3498db", "ota": False, "hurdle": 45.0, "group": False},
    {"label": "2. OTA CHANNELS", "key": "ota", "color": "#2ecc71", "ota": True, "hurdle": 35.0, "group": False},
    {"label": "3. CORPORATE / MICE GROUPS", "key": "mice", "color": "#34495e", "ota": False, "hurdle": 32.0, "group": True},
    {"label": "4. GROUP TOUR & TRAVEL", "key": "tnt", "color": "#e67e22", "ota": False, "hurdle": 12.0, "group": True}
]

wealth_results = {}

for seg in segments:
    if st.checkbox(f"Activate {seg['label']}", value=(seg['key'] in ['fit', 'tnt']), key=f"act_{seg['key']}_{rk}"):
        st.markdown(f"<div class='card' style='border-left-color:{seg['color']}'>{seg['label']}</div>", unsafe_allow_html=True)
        with st.container():
            st.markdown("<div class='pricing-row'>", unsafe_allow_html=True)
            
            # OTA COMMISSION SLIDER (ONLY IN OTA SEGMENT)
            c_ota = 0.0
            if seg['ota']:
                c_ota = st.slider("OTA Commission %", 0, 40, 15, key=f"comm_{seg['key']}_{rk}")
            
            r1 = st.columns([1, 0.6, 0.6, 0.6, 0.6, 1.2, 1.2])
            g_rate = r1[0].number_input(f"Gross Rate", value=29.0 if seg['key']=='tnt' else 75.0, step=0.5, key=f"adr_{seg['key']}_{rk}")
            min_v = 10 if seg['group'] else 1
            sgl, dbl, tpl, qrpl = r1[1].number_input("SGL", 0, key=f"s_{seg['key']}_{rk}"), r1[2].number_input("DBL", min_v if seg['key']=='tnt' else 0, key=f"d_{seg['key']}_{rk}"), r1[3].number_input("TPL", 0, key=f"t_{seg['key']}_{rk}"), r1[4].number_input("QRPL", 0, key=f"q_{seg['key']}_{rk}")
            rooms_total = sgl + dbl + tpl + qrpl
            demand_sel = r1[5].selectbox("Market Demand", ["Compression (Peak)", "High Flow", "Standard", "Distressed"], key=f"dm_{seg['key']}_{rk}")
            h_base = r1[6].number_input("Base Hurdle", value=seg['hurdle'], step=1.0, key=f"hrd_{seg['key']}_{rk}")

            r2 = st.columns([0.6,0.6,0.6,0.6,0.6, 1.1, 1.1, 1.1])
            bf, ln, dn, sai, ai = r2[0].number_input("BF", 0, key=f"bf_in_{seg['key']}_{rk}"), r2[1].number_input("LN", 0, key=f"ln_in_{seg['key']}_{rk}"), r2[2].number_input("DN", 0, key=f"dn_in_{seg['key']}_{rk}"), r2[3].number_input("SAI", 0, key=f"sai_in_{seg['key']}_{rk}"), r2[4].number_input("AI", 0, key=f"ai_in_{seg['key']}_{rk}")
            m_pp, l_pp, t_f = r2[5].number_input("Events", 0.0, key=f"m_{seg['key']}_{rk}") if seg['group'] else 0.0, r2[6].number_input("Laundry", 0.0, key=f"l_{seg['key']}_{rk}") if seg['group'] else 0.0, r2[7].number_input("Transport", 0.0, key=f"tr_{seg['key']}_{rk}") if seg['group'] else 0.0

            res = run_segment_yield(g_rate, {"BF":bf,"LN":ln,"DN":dn,"SAI":sai,"AI":ai}, h_base, demand_sel, seg['group'], rooms_total, c_ota, m_pp, l_pp, t_f)
            
            v_cols = st.columns([1, 1.5, 1])
            v_cols[0].metric("Net Wealth", f"{cur_sym} {res['w']:,.2f}", delta=f"{res['vm']}x Velocity")
            v_cols[1].markdown(f"<div class='status-indicator' style='background:{res['cl']}'>{res['st']}</div>", unsafe_allow_html=True)
            v_cols[2].markdown(f"<div style='text-align:right;'><span class='noi-badge'>Segment NOI: {cur_sym} {res['noi']:,.2f}</span></div>", unsafe_allow_html=True)
            
            st.markdown(f"<div class='reason-box'>💡 <b>Strategic Reasoning:</b> {res['rsn']} | <b>Effective Hurdle:</b> {cur_sym}{res['dh']:,.2f}</div>", unsafe_allow_html=True)
            wealth_results[seg['key']] = {"w": res['w'], "rooms": max(rooms_total, min_v), "noi": res['noi']}
            st.markdown("</div>", unsafe_allow_html=True)

# --- 7. NOI SUMMARY & PILLARS ---
st.divider()
e_keys = list(wealth_results.keys())
if len(e_keys) >= 2:
    sa, sb = wealth_results[e_keys[0]], wealth_results[e_keys[1]]
    total_gain = (sa['w'] - sb['w']) * sb['rooms'] * m_nights
    total_potential_wealth = sa['w'] * h_cap * m_nights
    eff = (total_gain / total_potential_wealth * 100) if total_potential_wealth != 0 else 0
    m_cols = st.columns(4)
    m_cols[0].metric("Wealth Gap", f"{cur_sym} {sa['w'] - sb['w']:,.2f}")
    m_cols[1].metric("Total NOI Gain", f"{cur_sym} {total_gain:,.2f}")
    m_cols[2].metric("NOI Improvement", f"{((sa['w']-sb['w'])/sb['w']*100 if sb['w']!=0 else 0):.2f}%")
    m_cols[3].metric("Asset Efficiency", f"{eff:.2f}%")

st.markdown("<div class='theory-box'><h3 style='color:#1e3799; margin-top:0;'>THE YIELD EQUILIBRIUM STRATEGIC FRAMEWORK</h3><div style='display:flex; justify-content:space-between;'><div style='width:30%;'><span class='pillar-header'>🏛️ Pillar 01: Internal Wealth Stripping</span><p style='font-size:0.85rem; color:#4b6584;'>Strips statutory taxes (1.2327 divisor), commissions, and meal costs to isolate <b>Net-Core Wealth</b>.</p></div><div style='width:30%;'><span class='pillar-header'>⚖️ Pillar 02: Dynamic Hurdle Equilibrium</span><p style='font-size:0.85rem; color:#4b6584;'>Protects inventory by scaling hurdles up to 2.5x during peak cycles to ensure high-value pickup.</p></div><div style='width:30%;'><span class='pillar-header'>🌐 Pillar 03: External Velocity</span><p style='font-size:0.85rem; color:#4b6584;'>Integrates market pulse data to apply demand multipliers based on real-time market flow.</p></div></div></div>", unsafe_allow_html=True)
