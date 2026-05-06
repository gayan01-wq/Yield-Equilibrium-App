import streamlit as st
import google.generativeai as genai

# --- 1. STYLING (The Global Executive Aesthetic) ---
st.set_page_config(layout="wide", page_title="Displacement Analyzer | Yield Equilibrium")
st.markdown("""<style>
.block-container{padding-top:1rem!important;}
.main-title { font-size: 2.2rem!important; font-weight: 900; color: #1e3799; text-align: center!important; margin-top: -10px; text-transform: uppercase; letter-spacing: 2px; display: block; width: 100%; }
.card{padding:10px;border-radius:10px;margin-bottom:8px;border-left:10px solid;background:#ffffff;box-shadow: 0 2px 4px rgba(0,0,0,0.1)}
.pricing-row{background:#f8faff;padding:12px;border-radius:10px;border:1px solid #d1d9e6; margin-top:5px;}
.status-indicator{padding:12px; border-radius:10px; text-align:center; font-weight:900; font-size:1.1rem; color:white; margin-top:10px;}
.reason-box{background:#fff9c4; border:1px solid #fbc02d; padding:10px; border-radius:8px; margin-top:5px; text-align:left; font-weight:500; color:#5f4300; font-size:0.8rem;}
.ai-badge {background: #4285f4; color: white; padding: 4px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 800; margin-bottom: 5px; display: inline-block;}
</style>""", unsafe_allow_html=True)

# --- 2. AUTHENTICATION & CACHE ---
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

# --- 3. SIDEBAR (Pillar 01: Governance Controls) ---
with st.sidebar:
    st.markdown("### 👤 System Developer\nGayan Nugawela")
    if st.button("🧹 Clear Global Cache"):
        st.session_state["reset_key"] += 1
        st.rerun()
    st.divider()
    rk = str(st.session_state["reset_key"]) 
    
    cur_sym = "﷼"
    inventory = st.number_input("Total Capacity", 1, 1000, 237, key="inv_c_"+rk)
    
    st.divider()
    st.markdown("### 📊 Market Velocity")
    otb_occ = st.slider("OTB %", 0, 100, 15, key="otb_s_"+rk)
    avg_hist = st.slider("Hist. Benchmark %", 0, 100, 45, key="hst_s_"+rk)
    v_mult = 1.35 if otb_occ > avg_hist else 0.85 if otb_occ < (avg_hist - 15) else 1.0

    tx_div = st.number_input("Tax Divisor", value=1.2327, format="%.4f", key="tx_v_"+rk)
    ota_comm = st.slider("OTA Commission %", 0, 40, 15, key="ota_v_"+rk)
    p01_fee = st.number_input(f"P01 Fee ({cur_sym})", 0.0, value=6.90, key="p01_v_"+rk)

    st.markdown("#### 🍲 Meal Basis Costs")
    m_costs = {
        "BB": st.number_input("BB Cost", value=5.0, key="bb_mc_"+rk),
        "HB": st.number_input("HB Cost", value=10.0, key="hb_mc_"+rk),
        "FB": st.number_input("FB Cost", value=15.0, key="fb_mc_"+rk),
        "SAI": st.number_input("SAI Cost", value=20.0, key="sai_mc_"+rk),
        "AI": st.number_input("AI Cost", value=25.0, key="ai_mc_"+rk)
    }

# --- 4. ENGINE LOGIC ---
def run_yield(rms_list, adr, hurdle, demand_type, meals, is_ota=False):
    tr = sum(rms_list)
    if tr <= 0: return None
    demand_adj = {"Compression (Peak)": 15.0, "High Flow": 5.0, "Standard": 0.0, "Distressed": -5.0}
    eff_hurdle = hurdle + demand_adj.get(demand_type, 0)
    net_adr = adr / tx_div
    comm = (net_adr * (ota_comm/100)) if is_ota else 0
    total_meal_cost = sum(meals[k]*m_costs[k] for k in meals)
    avg_meal_unit = total_meal_cost / tr
    unit_w = (net_adr - avg_meal_unit - comm) - p01_fee
    
    if unit_w < eff_hurdle: stt, clr, rsn = "REJECT: DILUTIVE", "#e74c3c", f"Yield < {cur_sym}{eff_hurdle} hurdle."
    else: stt, clr, rsn = "ACCEPT: OPTIMIZED", "#27ae60", "Wealth targets met."
    return {"w": unit_w, "st": stt, "cl": clr, "rsn": rsn, "data": locals()}

def ask_ai_equilibrium(user_query, context_data):
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"]) 
        model = genai.GenerativeModel('gemini-1.5-flash') 
        response = model.generate_content(f"Audit this: {context_data}. Prompt: {user_query}")
        return response.text
    except Exception as e: return f"System Note: {str(e)}"

# --- 5. DASHBOARD ---
st.markdown("<h1 class='main-title'>DISPLACEMENT ANALYZER</h1>", unsafe_allow_html=True)

def draw_seg(label, key, suggest_adr, floor_def, color, is_ota=False):
    st.markdown(f"<div class='card' style='border-left-color:{color}'>{label}</div>", unsafe_allow_html=True)
    c_in, c_res = st.columns([2.6, 1])
    with c_in:
        st.markdown("<div class='pricing-row'>", unsafe_allow_html=True)
        r1, r2, r3, r4 = st.columns([1,1,1,1.5])
        sgl = r1.number_input("SGL", 0, key=f"s_{key}_{rk}")
        dbl = r2.number_input("DBL", 0, key=f"d_{key}_{rk}")
        tpl = r3.number_input("TPL", 0, key=f"t_{key}_{rk}")
        rate = r4.number_input(f"Applied Rate ({cur_sym})", value=float(suggest_adr * v_mult), key=f"a_{key}_{rk}")
        m_row = st.columns([1,1,1,1,1,1.5])
        m_bb = m_row[0].number_input("BB", 0, key=f"mbb_{key}_{rk}")
        m_hb = m_row[1].number_input("HB", 0, key=f"mhb_{key}_{rk}")
        m_fb = m_row[2].number_input("FB", 0, key=f"mfb_{key}_{rk}")
        m_sai = m_row[3].number_input("SAI", 0, key=f"msai_{key}_{rk}")
        m_ai = m_row[4].number_input("AI", 0, key=f"mai_{key}_{rk}")
        demand = m_row[5].selectbox("Demand", ["Compression (Peak)", "High Flow", "Standard", "Distressed"], key=f"dm_{key}_{rk}")
        hurdle = st.number_input("Base Hurdle", value=float(floor_def), key=f"hrd_{key}_{rk}")
        st.markdown("</div>", unsafe_allow_html=True)

    meals = {"BB":m_bb, "HB":m_hb, "FB":m_fb, "SAI":m_sai, "AI":m_ai}
    res = run_yield([sgl, dbl, tpl], rate, hurdle, demand, meals, is_ota)
    with c_res:
        if res:
            st.metric("Net Wealth", f"{cur_sym} {res['w']:,.2f}")
            st.markdown(f"<div class='status-indicator' style='background:{res['cl']}'>{res['st']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='reason-box'>💡 <b>Verdict:</b> {res['rsn']}</div>", unsafe_allow_html=True)
            if st.button("Ask Theory Audit", key=f"ai_btn_{key}"):
                st.info(ask_ai_equilibrium("Provide audit.", res['data']))
        else: st.info("Input room count.")

draw_seg("1. DIRECT / FIT", "fit", 65, 40, "#3498db")
draw_seg("2. OTA CHANNELS", "ota", 60, 35, "#2ecc71", is_ota=True)
draw_seg("3. CORPORATE GROUPS", "corp", 55, 32, "#34495e")
