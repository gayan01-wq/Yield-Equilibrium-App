import streamlit as st
from datetime import date
import google.generativeai as genai

# --- 1. STYLING (Revenue Executive Aesthetic) ---
st.set_page_config(layout="wide", page_title="Displacement Analyzer | Yield Equilibrium")
st.markdown("""<style>
.block-container{padding-top:1rem!important;}
.main-title { font-size: 2.2rem!important; font-weight: 900; color: #1e3799; text-align: center!important; margin-top: -10px; text-transform: uppercase; letter-spacing: 2px; display: block; width: 100%; }
.main-subtitle { font-size: 1.15rem!important; font-weight: 600; color: #4b6584; text-align: center!important; margin-top: -10px; margin-bottom: 30px; letter-spacing: 1px; display: block; width: 100%; }
.card{padding:10px;border-radius:10px;margin-bottom:8px;border-left:10px solid;background:#ffffff;box-shadow: 0 2px 4px rgba(0,0,0,0.1)}
.pricing-row{background:#f8faff;padding:12px;border-radius:10px;border:1px solid #d1d9e6; margin-top:5px;}
.status-indicator{padding:12px; border-radius:10px; text-align:center; font-weight:900; font-size:1.1rem; color:white; margin-top:10px;}
.reason-box{background:#fff9c4; border:1px solid #fbc02d; padding:10px; border-radius:8px; margin-top:5px; text-align:left; font-weight:500; color:#5f4300; font-size:0.8rem;}
.audit-box{font-size:0.85rem; font-weight:700; color:#1e3799; margin-top:5px; border-top: 1px dotted #d1d9e6; padding-top: 5px;}
.ai-badge {background: #4285f4; color: white; padding: 4px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 800; margin-bottom: 5px; display: inline-block;}
</style>""", unsafe_allow_html=True)

# --- 2. AUTHENTICATION ---
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

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown("### 👤 Developer: Gayan Nugawela")
    if not st.session_state["ai_unlocked"]:
        with st.expander("Register for AI Theory Audit"):
            with st.form("lead_gen"):
                u_email = st.text_input("Work Email")
                u_comp = st.text_input("Company")
                if st.form_submit_button("Unlock AI"):
                    if "@" in u_email:
                        st.session_state["ai_unlocked"] = True
                        st.rerun()

    if st.button("🧹 Clear Global Cache"):
        st.session_state["reset_key"] += 1
        st.rerun()
    st.divider()
    rk = str(st.session_state["reset_key"]) 
    
    cur_sym = "﷼"
    hotel_name = st.text_input("🏨 Hotel", "Wyndham Garden Salalah", key="h_nm_"+rk)
    inventory = st.number_input("Total Capacity", 1, 1000, 237, key="inv_c_"+rk)
    
    st.divider()
    tx_div = st.number_input("Tax Divisor", value=1.2327, format="%.4f", key="tx_v_"+rk)
    ota_comm = st.slider("OTA Commission %", 0, 40, 15, key="ota_v_"+rk)
    p01_fee = st.number_input(f"P01 Fee ({cur_sym})", 0.0, value=6.90, key="p01_v_"+rk)

    meal_costs = {"BB": st.number_input("BB Cost", 0, value=5, key="bb_mc_"+rk)}

# --- 4. CALCULATION ENGINE ---
def run_yield(rms, nts, adr, meals, hurdle, demand_type, comm_rate=0.0):
    tr = sum(rms); rn = tr * nts
    if tr <= 0: return None
    demand_adj = {"Compression (Peak)": 15.0, "High Flow": 5.0, "Standard": 0.0, "Distressed": -5.0}
    eff_hurdle = hurdle + demand_adj.get(demand_type, 0)
    net_adr = adr / tx_div
    unit_w = (net_adr - meals.get("BB", 0) - (net_adr * comm_rate)) - p01_fee
    total_w = (unit_w * rn)

    if unit_w < eff_hurdle: stt, clr, rsn = "REJECT: DILUTIVE", "#e74c3c", f"Yield < {cur_sym}{eff_hurdle} hurdle."
    else: stt, clr, rsn = "ACCEPT: OPTIMIZED", "#27ae60", "Wealth targets met."
    
    return {"w": unit_w, "st": stt, "cl": clr, "rsn": rsn, "total": total_w, "data": locals()}

# --- 5. AI LOGIC (Stability Update) ---
def ask_ai_equilibrium(user_query, context_data):
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"]) 
        # Updated model name to resolve 404 error
        model = genai.GenerativeModel('gemini-1.5-flash-latest') 
        response = model.generate_content(f"Data: {context_data}. Question: {user_query}")
        return response.text
    except Exception as e:
        return f"System Note: {str(e)}"

# --- 6. DASHBOARD ---
st.markdown("<h1 class='main-title'>DISPLACEMENT ANALYZER</h1>", unsafe_allow_html=True)

def draw_seg(label, key, suggest_adr, floor_def, color, is_ota=False):
    st.markdown(f"<div class='card' style='border-left-color:{color}'>{label}</div>", unsafe_allow_html=True)
    c_in, c_res = st.columns([2.6, 1])
    with c_in:
        st.markdown("<div class='pricing-row'>", unsafe_allow_html=True)
        r1, r2, r3 = st.columns([1,1,1])
        sgl = r1.number_input("SGL Rooms", 0, key=f"s_{key}_{rk}")
        applied_adr = r2.number_input(f"Rate ({cur_sym})", value=float(suggest_adr), key=f"a_{key}_{rk}")
        floor = r3.number_input(f"Base Hurdle", value=float(floor_def), key=f"f_{key}_{rk}")
        demand_sel = st.selectbox("Demand Type", ["Compression (Peak)", "High Flow", "Standard", "Distressed"], key=f"dm_{key}_{rk}")
        st.markdown("</div>", unsafe_allow_html=True)
    
    res = run_yield([sgl], 1, applied_adr, meal_costs, floor, demand_sel, (ota_comm/100 if is_ota else 0.0))
    
    if res:
        with c_res:
            st.metric(f"Net Wealth", f"{cur_sym} {res['w']:,.2f}")
            st.markdown(f"<div class='status-indicator' style='background:{res['cl']}'>{res['st']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='reason-box'>💡 {res['rsn']}</div>", unsafe_allow_html=True)
            if st.session_state["ai_unlocked"]:
                if st.button("Ask Theory Audit", key=f"ai_btn_{key}"):
                    st.info(ask_ai_equilibrium("Audit this based on Yield Equilibrium pillars.", res['data']))

draw_seg("2. OTA CHANNELS", "ota", 51, 35, "#2ecc71", is_ota=True)
