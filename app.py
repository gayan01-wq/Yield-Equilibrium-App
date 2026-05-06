import streamlit as st
from datetime import date
import google.generativeai as genai

# --- 1. STYLING (The Global Executive Aesthetic) ---
st.set_page_config(layout="wide", page_title="Displacement Analyzer | Yield Equilibrium")
st.markdown("""<style>
.block-container{padding-top:1rem!important;}
.main-title { font-size: 2.2rem!important; font-weight: 900; color: #1e3799; text-align: center!important; margin-top: -10px; text-transform: uppercase; letter-spacing: 2px; display: block; width: 100%; }
.main-subtitle { font-size: 1.15rem!important; font-weight: 600; color: #4b6584; text-align: center!important; margin-top: -10px; margin-bottom: 30px; letter-spacing: 1px; display: block; width: 100%; }
.card{padding:10px;border-radius:10px;margin-bottom:8px;border-left:10px solid;background:#ffffff;box-shadow: 0 2px 4px rgba(0,0,0,0.1)}
.pricing-row{background:#f8faff;padding:12px;border-radius:10px;border:1px solid #d1d9e6; margin-top:5px;}
.google-window{background:#e8f0fe; padding:18px; border-radius:12px; border:2px solid #4285f4; margin-bottom:15px; font-size:0.85rem; line-height:1.6;}
.news-item{background:#ffffff; border-radius:8px; padding:10px; margin-bottom:8px; border-left:4px solid #ff4b4b; box-shadow: 0 1px 3px rgba(0,0,0,0.05);}
.status-indicator{padding:12px; border-radius:10px; text-align:center; font-weight:900; font-size:1.1rem; color:white; margin-top:10px;}
.reason-box{background:#fff9c4; border:1px solid #fbc02d; padding:10px; border-radius:8px; margin-top:5px; text-align:left; font-weight:500; color:#5f4300; font-size:0.8rem;}
.audit-box{font-size:0.85rem; font-weight:700; color:#1e3799; margin-top:5px; border-top: 1px dotted #d1d9e6; padding-top: 5px;}
.ai-badge {background: #4285f4; color: white; padding: 4px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 800; margin-bottom: 5px; display: inline-block;}
.theory-box{background:#f9f9f9; padding:25px; border-radius:15px; border:1px solid #dee2e6; margin-top:30px}
.contact-section{background:#1e3799; padding:30px; border-radius:15px; margin-top:40px; color:white;}
</style>""", unsafe_allow_html=True)

# --- 2. AUTHENTICATION & LEAD CAPTURE ---
if "auth" not in st.session_state: st.session_state["auth"] = False
if "reset_key" not in st.session_state: st.session_state["reset_key"] = 0
if "ai_unlocked" not in st.session_state: st.session_state["ai_unlocked"] = False

if not st.session_state["auth"]:
    st.markdown("<h1 class='main-title'>EQUILIBRIUM ENGINE</h1>", unsafe_allow_html=True)
    with st.form("login_gate"):
        pwd = st.text_input("Access Key", type="password")
        if st.form_submit_button("Unlock"):
            if pwd == "Gayan2026": 
                st.session_state["auth"] = True
                st.rerun()
            else: st.error("Access Denied")
    st.stop()

# --- 3. SIDEBAR (STRATEGIC INPUTS & SIMULATION) ---
with st.sidebar:
    st.markdown("### 👤 System Developer\nGayan Nugawela")
    if not st.session_state["ai_unlocked"]:
        st.divider()
        st.warning("🔒 AI Assistant Locked")
        with st.expander("Register for Strategic AI"):
            with st.form("lead_gen"):
                u_email = st.text_input("Work Email")
                u_comp = st.text_input("Company")
                if st.form_submit_button("Unlock AI"):
                    if "@" in u_email:
                        st.session_state["ai_unlocked"] = True
                        st.success("AI Analytics Active!")
                        st.rerun()

    if st.button("🧹 Clear Global Cache"):
        st.session_state["reset_key"] += 1
        st.rerun()
    st.divider()
    rk = str(st.session_state["reset_key"]) 
    
    currencies = {"OMR (﷼)": "﷼", "LKR (රු)": "රු", "THB (฿)": "฿", "AED (د.إ)": "د.إ", "SAR (﷼)": "﷼", "INR (₹)": "₹", "USD ($)": "$"}
    cur_choice = st.selectbox("🌍 Base Currency", list(currencies.keys()), key="c_sel_"+rk)
    cur_sym = currencies[cur_choice]

    hotel_name = st.text_input("🏨 Hotel", "Wyndham Garden Salalah", key="h_nm_"+rk)
    city_search = st.text_input("📍 City Search", "Salalah", key="c_nm_"+rk)
    
    st.markdown("### 🧪 Simulation Suite")
    sim_room_count = st.slider("Simulate Group Room Count", 1, 100, 40)

    d1 = st.date_input("Check-In", date.today(), key="d_in_"+rk)
    d2 = st.date_input("Check-Out", date.today(), key="d_out_"+rk)
    m_nights = (d2 - d1).days if (d2 - d1).days > 0 else 1
    inventory = st.number_input("Total Capacity", 1, 1000, 237, key="inv_c_"+rk)
    
    st.divider()
    st.markdown("### 📊 Pillar 03: Velocity")
    otb_occ = st.slider("OTB %", 0, 100, 15, key="otb_s_"+rk)
    avg_hist = st.slider("Hist. Benchmark %", 0, 100, 45, key="hst_s_"+rk)
    v_mult = 1.35 if otb_occ > avg_hist else 0.85 if otb_occ < (avg_hist - 15) else 1.0

    st.divider()
    tx_div = st.number_input("Tax Divisor", value=1.2327, format="%.4f", key="tx_v_"+rk)
    ota_comm = st.slider("OTA Commission %", 0, 40, 15, key="ota_v_"+rk)
    p01_fee = st.number_input(f"P01 Fee ({cur_sym})", 0.0, value=6.90, key="p01_v_"+rk)

    meal_costs = {"RO": 0.0, "BB": st.number_input("BB Cost", 0, key="bb_mc_"+rk), "LN": st.number_input("LN Cost", 0, key="ln_mc_"+rk), "DN": st.number_input("DN Cost", 0, key="dn_mc_"+rk), "SAI": st.number_input("SAI Cost", 0, key="sai_mc_"+rk), "AI": st.number_input("AI Cost", 0, key="ai_mc_"+rk)}

# --- 4. CALCULATION ENGINE ---
def run_yield(rms, nts, adr, meals, hurdle, demand_type, comm_rate=0.0, laundry=0, mice=0, trans=0):
    tr = sum(rms); rn = tr * nts
    if tr <= 0: return None
    demand_adj = {"Compression (Peak)": 15.0, "High Flow": 5.0, "Standard": 0.0, "Distressed": -5.0}
    eff_hurdle = hurdle + demand_adj.get(demand_type, 0)
    net_adr = adr / tx_div
    total_m = sum(qty * meal_costs.get(p, 0) for p, qty in meals.items())
    avg_m = (total_m / tr)
    unit_w = (net_adr - avg_m - (net_adr * comm_rate)) - p01_fee - laundry + (mice / tx_div)
    total_w = (unit_w * rn) + (trans / tx_div)
    
    # NOI Calculation based on your capacity
    noi_impact_pct = (total_w / (eff_hurdle * inventory * 30)) * 100 if eff_hurdle > 0 else 0

    if unit_w < eff_hurdle: stt, clr, rsn = "REJECT: DILUTIVE", "#e74c3c", f"Yield < {cur_sym}{eff_hurdle} hurdle."
    elif unit_w < (eff_hurdle + 3.0): stt, clr, rsn = "REVIEW: MARGINAL", "#f39c12", "Yield at equilibrium window."
    else: stt, clr, rsn = "ACCEPT: OPTIMIZED", "#27ae60", "Wealth targets met."
    
    return {"w": unit_w, "st": stt, "cl": clr, "rsn": rsn, "rn": rn, "total": total_w, "noi_pct": noi_impact_pct, "data": locals()}

# --- 5. AI LOGIC (Stability Update) ---
def ask_ai_equilibrium(user_query, context_data):
    try:
        # Securely retrieve key from Streamlit Secrets
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"]) 
        model = genai.GenerativeModel('gemini-1.5-flash', system_instruction="You are Gayan Nugawela's Yield Equilibrium Assistant. Analyze displacement results using Pillar 01 (Wealth Stripping) and Pillar 02 (Hurdle Equilibrium).")
        response = model.generate_content(f"Data: {context_data}. Question: {user_query}")
        return response.text
    except Exception as e:
        return f"System Note: {str(e)}"

# --- 6. DASHBOARD DRAWING ---
st.markdown("<h1 class='main-title'>DISPLACEMENT ANALYZER</h1>", unsafe_allow_html=True)
st.markdown("<div class='main-subtitle'>Yield Equilibrium Strategic Intelligence Engine</div>", unsafe_allow_html=True)

def draw_seg(label, key, suggest_adr, floor_def, color, is_ota=False, group=False):
    st.markdown(f"<div class='card' style='border-left-color:{color}'>{label}</div>", unsafe_allow_html=True)
    c_in, c_res = st.columns([2.6, 1])
    with c_in:
        st.markdown("<div class='pricing-row'>", unsafe_allow_html=True)
        r1, r2, r3, r4, r5 = st.columns([0.8,0.8,0.8,1.3,1.3])
        init_rms = sim_room_count if (group and key != "fit" and key != "ota") else 0
        sgl = r1.number_input("SGL", 0, value=init_rms, key=f"s_{key}_{rk}")
        dbl = r2.number_input("DBL", 0, key=f"d_{key}_{rk}"); tpl = r3.number_input("TPL", 0, key=f"t_{key}_{rk}")
        applied_adr = r4.number_input(f"Rate ({cur_sym})", value=float(suggest_adr * v_mult), key=f"a_{key}_{rk}")
        floor = r5.number_input(f"Base Hurdle", value=float(floor_def), key=f"f_{key}_{rk}")
        
        m_row = st.columns([1.5, 1, 1, 1, 1, 1, 1])
        demand_sel = m_row[0].selectbox("Demand", ["Compression (Peak)", "High Flow", "Standard", "Distressed"], key=f"dm_{key}_{rk}")
        p_ro = m_row[1].number_input("RO", 0, key=f"ro_{key}_{rk}"); p_bb = m_row[2].number_input("BB", 0, key=f"bb_{key}_{rk}"); p_ln = m_row[3].number_input("LN", 0, key=f"ln_{key}_{rk}"); p_dn = m_row[4].number_input("DN", 0, key=f"dn_{key}_{rk}"); p_sai = m_row[5].number_input("SAI", 0, key=f"sai_{key}_{rk}"); p_ai = m_row[6].number_input("AI", 0, key=f"ai_{key}_{rk}")
        l_c, m_c, t_c = 0.0, 0.0, 0.0
        if group:
            g_row = st.columns(3)
            m_c = g_row[0].number_input(f"MICE", 0.0, key=f"mi_{key}_{rk}"); t_c = g_row[1].number_input(f"Trans", 0.0, key=f"tr_{key}_{rk}"); l_c = g_row[2].number_input(f"Laundry", 0.0, key=f"la_{key}_{rk}")
        st.markdown("</div>", unsafe_allow_html=True)
    
    res = run_yield([sgl, dbl, tpl], m_nights, applied_adr, {"RO":p_ro,"BB":p_bb,"LN":p_ln,"DN":p_dn,"SAI":p_sai,"AI":p_ai}, floor, demand_sel, (ota_comm/100 if is_ota else 0.0), l_c, m_c, t_c)
    
    if res:
        with c_res:
            st.metric(f"Net Wealth", f"{cur_sym} {res['w']:,.2f}")
            st.markdown(f"<div class='status-indicator' style='background:{res['cl']}'>{res['st']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='reason-box'>💡 <b>Strategic Verdict:</b><br>{res['rsn']}</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='ai-badge'>🤖 AI-ASSISTED FORECAST</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:0.75rem; color:#4285f4; font-weight:bold;'>Projected 30-Day NOI Impact: +{res['noi_pct']:.2f}%</div>", unsafe_allow_html=True)
            
            if st.session_state["ai_unlocked"]:
                if st.button("Ask Theory Audit", key=f"ai_btn_{key}"):
                    st.info(ask_ai_equilibrium("Provide an audit for this specific segment based on Yield Equilibrium Protocol.", res['data']))
            
            st.markdown(f"<div class='audit-box'>📊 {res['rn']} RN | Total Wealth: {cur_sym} {res['total']:,.2f}</div>", unsafe_allow_html=True)

draw_seg("1. DIRECT / FIT", "fit", 65, 40, "#3498db")
draw_seg("2. OTA CHANNELS", "ota", 60, 35, "#2ecc71", is_ota=True)
draw_seg("3. CORPORATE GROUPS", "corp", 55, 32, "#34495e", group=True)
draw_seg("4. MICE GROUPS", "mice", 50, 30, "#9b59b6", group=True)
draw_seg("5. TOUR & TRAVEL (GROUPS)", "tnt", 45, 25, "#e67e22", group=True)
