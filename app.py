import streamlit as st
from datetime import date

# --- 1. STYLING (Executive Centering & Status Colors) ---
st.set_page_config(layout="wide", page_title="Displacement Analyzer | Yield Equilibrium")
st.markdown("""<style>
.block-container{padding-top:1rem!important;}
.main-title{font-size:2.2rem!important;font-weight:900;color:#1e3799;text-align:center;width:100%;display:block;text-transform:uppercase;margin-bottom:0px;}
.main-subtitle{font-size:1.1rem!important;font-weight:600;color:#4b6584;text-align:center;width:100%;display:block;margin-top:5px;margin-bottom:25px;}
.card{padding:12px;border-radius:10px;margin-bottom:10px;border-left:12px solid #1e3799;background:#ffffff;box-shadow: 0 2px 5px rgba(0,0,0,0.1)}
.pricing-row{background:#f8faff;padding:15px;border-radius:10px;border:1px solid #d1d9e6;}
.status-indicator{padding:10px;border-radius:8px;text-align:center;font-weight:900;color:white;margin-top:10px;font-size:1.1rem;}
.theory-box{background:#f1f4f9;padding:20px;border-radius:12px;border:1px solid #1e3799;margin-top:20px;}
[data-testid="stSidebar"]{background:#f1f4f9;}
.contact-section{background:#1e3799;padding:25px;border-radius:15px;margin-top:30px;color:white;}
</style>""", unsafe_allow_html=True)

# --- 2. AUTHENTICATION ---
if "auth" not in st.session_state: st.session_state["auth"] = False
if not st.session_state["auth"]:
    st.markdown("<h1 class='main-title'>EQUILIBRIUM ENGINE</h1>", unsafe_allow_html=True)
    with st.form("login"):
        if st.text_input("Access Key", type="password") == "Gayan2026" and st.form_submit_button("Unlock"):
            st.session_state["auth"] = True; st.rerun()
    st.stop()

# --- 3. SIDEBAR (STRATEGIC GLOBAL INPUTS) ---
with st.sidebar:
    st.markdown("### 👤 System Developer\nGayan Nugawela")
    if st.button("🧹 Reset System Cache"): st.rerun()
    st.divider()
    
    cur = st.selectbox("Base Currency", ["OMR (﷼)", "LKR (රු)", "THB (฿)", "AED (د.إ)", "SAR (﷼)", "INR (₹)", "USD ($)", "EUR (€)", "GBP (£)"])
    cur_sym = cur.split('(')[1].replace(')', '')
    city = st.text_input("Analysis City", "Salalah")
    
    col_d1, col_d2 = st.columns(2)
    d1 = col_d1.date_input("Check-In", date.today())
    d2 = col_d2.date_input("Check-Out", date.today())
    m_nts = (d2 - d1).days if (d2 - d1).days > 0 else 1
    st.info(f"📅 **Stay Duration: {m_nts} Nights**")
    
    st.divider()
    otb, hst = st.slider("OTB %", 0, 100, 15), st.slider("Hist. %", 0, 100, 45)
    v_mult = 1.35 if otb > hst else 0.85 if otb < (hst - 15) else 1.0
    tx_div = st.number_input("Tax Divisor", 1.2327, format="%.4f")
    ota_p = st.slider("OTA Commission %", 0, 40, 15)
    p01_f = st.number_input(f"P01 Fee ({cur_sym})", value=6.90)
    
    mc = {p: st.number_input(f"{p} Cost", v) for p, v in {"BB":2.5, "LN":4.5, "DN":5.5, "SAI":8.5, "AI":10.5}.items()}

# --- 4. CALCULATION ENGINE ---
def run_yield(rms, adr, meals, hurdle, demand, is_ota=False, mice=0, laundry=0, trans=0):
    tr = sum(rms)
    if tr <= 0: return None
    eff_h = hurdle + {"Compression (Peak)": 15, "High Flow": 5, "Standard": 0, "Distressed": -5}.get(demand, 0)
    net_adr = adr / tx_div
    comm = (net_adr * (ota_p / 100)) if is_ota else 0
    avg_m = sum(qty * mc.get(p, 0) for p, qty in meals.items()) / tr
    unit_w = (net_adr - avg_m - comm - p01_f - laundry) + (mice / tx_div)
    total_w = (unit_w * tr * m_nts) + (trans / tx_div)
    
    if unit_w >= (eff_h + 3.0): stt, clr = "ACCEPT: OPTIMIZED", "#27ae60"
    elif unit_w >= eff_h: stt, clr = "ACCEPT: MARGINAL", "#f39c12"
    else: stt, clr = "REJECT: DILUTIVE", "#e74c3c"
    return {"w": unit_w, "st": stt, "cl": clr, "total": total_w, "rn": tr * m_nts}

# --- 5. DASHBOARD HEADER ---
st.markdown("<div class='main-title'>DISPLACEMENT ANALYZER</div>", unsafe_allow_html=True)
st.markdown("<div class='main-subtitle'>Yield Equilibrium Strategic Intelligence Engine</div>", unsafe_allow_html=True)

# --- 6. SEGMENTS ---
def draw_seg(label, key, sadr, floor_def, clr, is_ota=False, is_grp=False):
    st.markdown(f"<div class='card' style='border-left-color:{clr}'>{label}</div>", unsafe_allow_html=True)
    c1, c2 = st.columns([2.8, 1])
    with c1:
        st.markdown("<div class='pricing-row'>", unsafe_allow_html=True)
        r1, r2, r3, r4, r5 = st.columns([0.8,0.8,0.8,1.2,1.2])
        s, d, t = r1.number_input("SGL",0,key="s"+key), r2.number_input("DBL",0,key="d"+key), r3.number_input("TPL",0,key="t"+key)
        rate = r4.number_input(f"Rate", value=float(sadr * v_mult), key="a"+key)
        floor = r5.number_input(f"Floor", value=float(floor_def), key="f"+key)
        
        m_row = st.columns([1.5, 1, 1, 1, 1, 1, 1])
        dem = m_row[0].selectbox("Demand", ["Standard", "Compression (Peak)", "High Flow", "Distressed"], key="dm"+key)
        m_v = {p: m_row[i+1].number_input(p, 0, key=f"{p}{key}") for i, p in enumerate(["BB", "LN", "DN", "SAI", "AI"])}
        
        mi, la, tr = 0, 0, 0
        if is_grp:
            g1, g2, g3 = st.columns(3)
            mi, la, tr = g1.number_input("MICE", 0.0, key="mi"+key), g2.number_input("Laundry", 0.0, key="la"+key), g3.number_input("Trans", 0.0, key="tr"+key)
        st.markdown("</div>", unsafe_allow_html=True)
        
    res = run_yield([s, d, t], rate, m_v, floor, dem, is_ota, mi, la, tr)
    if res:
        with c2:
            st.metric("Net Yield", f"{cur_sym} {res['w']:,.2f}")
            st.markdown(f"<div class='status-indicator' style='background:{res['cl']}'>{res['st']}</div>", unsafe_allow_html=True)
            st.write(f"Stay Wealth: **{cur_sym} {res['total']:,.2f}**")
            st.caption(f"📊 {res['rn']} Room Nights")

draw_seg("1. DIRECT / FIT", "fit", 65, 40, "#3498db")
draw_seg("2. OTA CHANNELS", "ota", 60, 35, "#2ecc71", True)
draw_seg("3. CORPORATE GROUPS", "corp", 55, 32, "#34495e", False, True)
draw_seg("4. MICE GROUPS", "mice", 50, 30, "#9b59b6", False, True)
draw_seg("5. TOUR & TRAVEL", "tnt", 45, 25, "#e67e22", False, True)

# --- 7. METHODOLOGY ---
st.divider()
st.markdown(f"<div class='theory-box'><h4>YIELD EQUILIBRI
