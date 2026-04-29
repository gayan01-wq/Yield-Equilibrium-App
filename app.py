import streamlit as st
from datetime import date

# --- 1. STYLING (The Global Executive Aesthetic) ---
st.set_page_config(layout="wide", page_title="Displacement Analyzer | Yield Equilibrium")
st.markdown("""<style>
.block-container{padding-top:1rem!important;}
.main-title{font-size:2.0rem!important;font-weight:900;color:#1e3799;text-align:center;margin-top:-10px;text-transform:uppercase;letter-spacing:2px;width:100%;display:block;}
.main-subtitle{font-size:1.1rem!important;font-weight:600;color:#4b6584;text-align:center;margin-top:-5px;margin-bottom:25px;letter-spacing:1px;width:100%;display:block;}
.card{padding:10px;border-radius:10px;margin-bottom:8px;border-left:10px solid;background:#ffffff;box-shadow: 0 2px 4px rgba(0,0,0,0.1)}
.pricing-row{background:#f8faff;padding:12px;border-radius:10px;border:1px solid #d1d9e6; margin-top:5px;}
.google-window{background:#e8f0fe; padding:18px; border-radius:12px; border:2px solid #4285f4; margin-bottom:15px; font-size:0.85rem; line-height:1.6;}
.status-indicator{padding:12px; border-radius:10px; text-align:center; font-weight:900; font-size:1.1rem; color:white; margin-top:10px;}
.theory-box{background:#f9f9f9; padding:25px; border-radius:15px; border:1px solid #dee2e6; margin-top:30px}
[data-testid="stSidebar"]{background:#f1f4f9; border-right:1px solid #dee2e6}
.contact-section{background:#1e3799; padding:30px; border-radius:15px; margin-top:40px; color:white;}
</style>""", unsafe_allow_html=True)

# --- 2. AUTHENTICATION ---
if "auth" not in st.session_state: st.session_state["auth"] = False
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

# --- 3. SIDEBAR (STRATEGIC INPUTS) ---
with st.sidebar:
    st.markdown("### 👤 System Developer\nGayan Nugawela")
    if st.button("🧹 Clear Cache"): st.rerun()
    st.divider()
    
    currencies = {"OMR (﷼)": "﷼", "LKR (රු)": "රු", "THB (฿)": "฿", "AED (د.إ)": "د.إ", "SAR (﷼)": "﷼", "INR (₹)": "₹", "USD ($)": "$"}
    cur_choice = st.selectbox("🌍 Base Currency", list(currencies.keys()))
    cur_sym = currencies[cur_choice]
    city = st.text_input("📍 City Search", "Salalah")
    
    d1 = st.date_input("Check-In", date.today())
    d2 = st.date_input("Check-Out", date.today())
    m_nights = (d2 - d1).days if (d2 - d1).days > 0 else 1
    st.info(f"📅 **Stay Duration: {m_nights} Nights**")
    
    st.divider()
    st.markdown("### 📊 Pillar 03: Velocity")
    otb_occ = st.slider("OTB %", 0, 100, 15)
    avg_hist = st.slider("Hist. Benchmark %", 0, 100, 45)
    v_mult = 1.35 if otb_occ > avg_hist else 0.85 if otb_occ < (avg_hist - 15) else 1.0

    st.divider()
    tx_div = st.number_input("Tax Divisor", value=1.2327, format="%.4f")
    ota_comm = st.slider("OTA Commission %", 0, 40, 15)
    p01_fee = st.number_input(f"P01 Fee ({cur_sym})", 0.0, value=6.90)

    st.markdown("### 🍽️ Unit Costs")
    mc = {
        "RO": 0.0, 
        "BB": st.number_input("BB Cost", 2.5),
        "LN": st.number_input("LN Cost", 4.5), 
        "DN": st.number_input("DN Cost", 5.5),
        "SAI": st.number_input("SAI Cost", 8.5), 
        "AI": st.number_input("AI Cost", 10.5)
    }

# --- 4. CALCULATION ENGINE ---
def run_yield(rms, nts, adr, meals, hurdle, demand, is_ota=False, mice=0, lndry=0, trans=0):
    tr = sum(rms)
    if tr <= 0: return None
    demand_adj = {"Compression (Peak)": 15.0, "High Flow": 5.0, "Standard": 0.0, "Distressed": -5.0}
    eff_hurdle = hurdle + demand_adj.get(demand, 0)
    
    net_adr = adr / tx_div
    comm = (net_adr * (ota_comm / 100)) if is_ota else 0
    avg_m = sum(qty * mc.get(p, 0) for p, qty in meals.items()) / tr
    
    unit_w = (net_adr - avg_m - comm) - p01_fee - lndry + (mice / tx_div)
    total_w = (unit_w * tr * nts) + (trans / tx_div)
    
    if unit_w >= (eff_hurdle + 3.0): stt, clr = "ACCEPT: OPTIMIZED", "#27ae60"
    elif unit_w >= eff_hurdle: stt, clr = "ACCEPT: MARGINAL", "#f39c12"
    else: stt, clr = "REJECT: DILUTIVE", "#e74c3c"
    
    return {"w": unit_w, "st": stt, "cl": clr, "total": total_w, "rn": tr * nts}

# --- 5. DASHBOARD HEADER ---
st.markdown("<h1 class='main-title'>DISPLACEMENT ANALYZER</h1>", unsafe_allow_html=True)
st.markdown("<div class='main-subtitle'>Yield Equilibrium Strategic Intelligence Engine</div>", unsafe_allow_html=True)

# --- 6. SEGMENTS ---
def draw_seg(label, key, suggest_adr, floor_def, color, is_ota=False, group=False):
    st.markdown(f"<div class='card' style='border-left-color:{color}'>{label}</div>", unsafe_allow_html=True)
    c1, c2 = st.columns([2.6, 1])
    with c1:
        st.markdown("<div class='pricing-row'>", unsafe_allow_html=True)
        r1, r2, r3, r4, r5 = st.columns([0.8,0.8,0.8,1.3,1.3])
        sgl = r1.number_input("SGL", 0, key="s"+key)
        dbl = r2.number_input("DBL", 0, key="d"+key)
        tpl = r3.number_input("TPL", 0, key="t"+key)
        rate = r4.number_input(f"Rate ({cur_sym})", value=float(suggest_adr * v_mult), key="a"+key)
        floor = r5.number_input(f"Floor", value=float(floor_def), key="f"+key)
        
        m_row = st.columns([1.5, 1, 1, 1, 1, 1, 1])
        dem = m_row[0].selectbox("Demand", ["Standard", "Compression (Peak)", "Distressed"], key="dm"+key)
        p_ro = m_row[1].number_input("RO", 0, key="ro"+key)
        p_bb = m_row[2].number_input("BB", 0, key="bb"+key)
        p_ln = m_row[3].number_input("LN", 0, key="ln"+key)
        p_dn = m_row[4].number_input("DN", 0, key="dn"+key)
        p_sai = m_row[5].number_input("SAI", 0, key="sai"+key)
        p_ai = m_row[6].number_input("AI", 0, key="ai"+key)
        
        mice_v, lnd_v, trns_v = 0, 0, 0
        if group:
            g1, g2, g3 = st.columns(3)
            mice_v = g1.number_input("MICE Revenue", 0.0, key="mi"+key)
            lnd_v = g2.number_input("Laundry Cost", 0.0, key="la"+key)
            trns_v = g3.number_input("Trans. Fixed", 0.0, key="tr"+key)
        st.markdown("</div>", unsafe_allow_html=True)
        
    res = run_yield([sgl, dbl, tpl], m_nights, rate, {"RO":p_ro,"BB":p_bb,"LN":p_ln,"DN":p_dn,"SAI":p_sai,"AI":p_ai}, floor, dem, is_ota, mice_v, lnd_v, trns_v)
    if res:
        with c2:
            st.metric("Net Wealth Yield", f"{cur_sym} {res['w']:,.2f}")
            st.markdown(f"<div class='status-indicator' style='background:{res['cl']}'>{res['st']}</div>", unsafe_allow_html=True)
            st.write(f"Stay Wealth: **{cur_sym} {res['total']:,.2f}**")
            st.caption(f"📊 {res['rn']} Room Nights")

draw_seg("1. DIRECT / FIT", "fit", 65, 40, "#3498db")
draw_seg("2. OTA CHANNELS", "ota", 60, 35, "#2ecc71", is_ota=True)
draw_seg("3. CORPORATE GROUPS", "corp", 55, 32, "#34495e", group=True)
draw_seg("4. MICE GROUPS", "mice", 50, 30, "#9b59b6", group=True)

# --- 7. FOOTER ---
st.markdown("<div class='contact-section'>", unsafe_allow_html=True)
st.subheader("✉️ Contact the System Developer")
st.write("Gayan Nugawela | gayan01@gmail.com")
st.markdown("</div>", unsafe_allow_html=True)
