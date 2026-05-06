import streamlit as st
from datetime import date

# --- 1. SETTINGS & STYLING ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium Displacement Analyzer")

st.markdown("""<style>
.block-container{padding-top:1rem!important; padding-bottom:0rem!important;}
.main-title { font-size: 2rem!important; font-weight: 900; color: #1e3799; text-align: center; text-transform: uppercase; margin-bottom: -5px; }
.main-subtitle { font-size: 1rem!important; font-weight: 600; color: #4b6584; text-align: center; margin-bottom: 15px; }
.card{padding:8px; border-radius:8px; margin-bottom:5px; border-left:10px solid; background:#ffffff; box-shadow: 0 2px 4px rgba(0,0,0,0.05)}
.pricing-row{background:#f8faff; padding:10px; border-radius:10px; border:1px solid #d1d9e6; margin-top:2px;}
.google-window{background:#e8f0fe; padding:12px; border-radius:10px; border:2px solid #4285f4; margin-bottom:10px; font-size:0.85rem; line-height:1.4;}
.status-indicator{padding:10px; border-radius:8px; text-align:center; font-weight:900; font-size:1rem; color:white;}
.reason-box{background:#fff9c4; border:1px solid #fbc02d; padding:8px; border-radius:8px; margin-top:5px; text-align:left; font-weight:500; color:#5f4300; font-size:0.75rem;}
.theory-box { background-color: #f1f4f9; padding: 25px; border-radius: 15px; border: 1px solid #d1d9e6; margin-top: 30px; }
.pillar-header { color: #1e3799; font-weight: 800; font-size: 0.95rem; text-transform: uppercase; margin-bottom: 5px; display: block; }
.pillar-desc { font-size: 0.88rem; color: #4b6584; line-height: 1.5; margin-bottom: 15px; }
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

# --- 3. SIDEBAR (EXPANDED CURRENCIES & INPUTS) ---
rk = str(st.session_state["reset_key"])
with st.sidebar:
    st.markdown("### 🏨 Property Profile")
    h_name = st.text_input("Hotel", "Wyndham Garden Salalah", key="h_nm_"+rk)
    city_search = st.text_input("📍 Location", "Salalah", key="city_"+rk)
    
    st.divider()
    st.markdown("### 📊 Pillar 01: Simulation")
    sim_rooms = st.slider("Inventory Shift", 5, 10000, 40, key="sim_s_"+rk)
    
    st.divider()
    st.markdown("### 🌍 Global Currency Suite")
    # Expanded for Middle East, Asia, and Europe
    currencies = {
        "OMR (﷼)": "﷼", "AED (د.إ)": "د.إ", "SAR (﷼)": "﷼", "QAR (﷼)": "﷼", # Middle East
        "LKR (රු)": "රු", "THB (฿)": "฿", "SGD ($)": "$", "MYR (RM)": "RM", "INR (₹)": "₹", # Asia
        "EUR (€)": "€", "GBP (£)": "£", "CHF (Fr)": "Fr", # Europe
        "USD ($)": "$"
    }
    cur_choice = st.selectbox("Select Base Currency", list(currencies.keys()), key="c_sel_"+rk)
    cur_sym = currencies[cur_choice]

    st.divider()
    st.markdown("### 🏛️ Statutory Deflators")
    tx_div = st.number_input("Tax Divisor", value=1.2327, format="%.4f", key="tx_v_"+rk)
    ota_comm = st.slider("OTA Comm %", 0, 40, 15, key="ota_v_"+rk)
    p01_fee = st.number_input(f"P01 Fee ({cur_sym})", 0.0, value=6.90, key="p01_v_"+rk)

# --- 4. ENGINE LOGIC ---
def run_segment_yield(adr, hurdle, demand_type, comm_rate=0.0):
    velocity_adj = {"Compression (Peak)": 1.25, "High Flow": 1.10, "Standard": 1.0, "Distressed": 0.85}
    v_mult = velocity_adj.get(demand_type, 1.0)
    net_adr = (adr * v_mult) / tx_div
    unit_w = (net_adr - (net_adr * comm_rate)) - p01_fee
    
    if unit_w < hurdle: stt, clr, rsn = "REJECT: DILUTIVE", "#e74c3c", f"Yield below {cur_sym}{hurdle} hurdle floor."
    elif unit_w < (hurdle + 5.0): stt, clr, rsn = "REVIEW: MARGINAL", "#f39c12", "Yield at equilibrium window."
    else: stt, clr, rsn = "ACCEPT: OPTIMIZED", "#27ae60", "Wealth protection targets met."
        
    return {"w": unit_w, "st": stt, "cl": clr, "rsn": rsn, "vm": v_mult}

# --- 5. TOP DASHBOARD ---
st.markdown(f"<h1 class='main-title'>{h_name.upper()}</h1>", unsafe_allow_html=True)
st.markdown("<div class='main-subtitle'>Yield Equilibrium Strategic Intelligence Engine</div>", unsafe_allow_html=True)

# --- 6. SEGMENT AUDITS (COMPACT VIEW) ---
segments = [
    {"label": "1. DIRECT / FIT", "key": "fit", "color": "#3498db", "ota": False, "hurdle": 45.0},
    {"label": "2. OTA CHANNELS", "key": "ota", "color": "#2ecc71", "ota": True, "hurdle": 35.0}
]

wealth_results = {}

for seg in segments:
    st.markdown(f"<div class='card' style='border-left-color:{seg['color']}'>{seg['label']}</div>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='pricing-row'>", unsafe_allow_html=True)
        c = st.columns([1.2, 1.2, 1, 1, 1.2])
        g_rate = c[0].number_input(f"Gross Rate", value=75.0, key=f"adr_{seg['key']}_{rk}")
        demand_sel = c[1].selectbox("Demand", ["Compression (Peak)", "High Flow", "Standard", "Distressed"], key=f"dm_{seg['key']}_{rk}")
        res = run_segment_yield(g_rate, seg['hurdle'], demand_sel, (ota_comm/100 if seg['ota'] else 0.0))
        
        c[2].metric("Net Wealth", f"{cur_sym} {res['w']:,.2f}")
        c[3].markdown(f"<div class='status-indicator' style='background:{res['cl']}'>{res['st']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='reason-box'>💡 <b>Strategic Reasoning:</b> {res['rsn']}</div>", unsafe_allow_html=True)
        wealth_results[seg['key']] = res['w']
        st.markdown("</div>", unsafe_allow_html=True)

# --- 7. SUMMARY & EXPANDED PILLARS ---
st.divider()
net_a, net_b = wealth_results['fit'], wealth_results['ota']
imp_val = (net_a - net_b) * sim_rooms
imp_pct = ((net_a - net_b) / net_b * 100) if net_b != 0 else 0

m1, m2, m3 = st.columns(3)
with m1: st.metric("Wealth Gap", f"{cur_sym} {net_a - net_b:,.2f}")
with m2: st.metric("Total NOI Gain", f"{cur_sym} {imp_val:,.2f}")
with m3: st.metric("NOI Improvement", f"{imp_pct:.2f}%")

# THE UPGRADED THEORY BOX
st.markdown("<div class='theory-box'>", unsafe_allow_html=True)
st.markdown("<h3 style='color:#1e3799; margin-top:0;'>THE YIELD EQUILIBRIUM STRATEGIC FRAMEWORK</h3>", unsafe_allow_html=True)

col_a, col_b, col_c = st.columns(3)

with col_a:
    st.markdown("<span class='pillar-header'>🏛️ Pillar 01: Internal Wealth Stripping</span>", unsafe_allow_html=True)
    st.markdown(f"<p class='pillar-desc'>Gross revenue is a market illusion. This engine deconstructs the rate by stripping statutory taxes ({tx_div}), channel commissions, and marginal costs to isolate the <b>Net-Core Wealth</b>.</p>", unsafe_allow_html=True)

with col_b:
    st.markdown("<span class='pillar-header'>⚖️ Pillar 02: Hurdle Equilibrium</span>", unsafe_allow_html=True)
    st.markdown("<p class='pillar-desc'>Protects high-value inventory by establishing a dynamic <b>Marginal Floor</b>. It ensures that lower-tier business does not displace premium segments during high-velocity cycles.</p>", unsafe_allow_html=True)

with col_c:
    st.markdown("<span class='pillar-header'>🌐 Pillar 03: External Velocity</span>", unsafe_allow_html=True)
    st.markdown("<p class='pillar-desc'>Integrates <b>Market Pulse</b> data including Aviation rotations and Area Demand. It applies a mathematical multiplier to wealth targets based on real-time compression indicators.</p>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
