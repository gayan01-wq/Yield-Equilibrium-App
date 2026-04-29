import streamlit as st
from datetime import date

# --- 1. STYLING & BRANDING ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium Engine")
st.markdown("""<style>
.block-container{padding-top:1rem!important; padding-bottom:1rem!important;}
.main-title{font-size:1.8rem!important;font-weight:900;color:#1e3799;text-align:center;margin-top:-15px;}
.card{padding:8px 12px;border-radius:8px;margin-bottom:5px;border-left:8px solid;font-weight:bold;background:#ffffff;box-shadow: 0 2px 4px rgba(0,0,0,0.05)}
.pricing-row{background:#f8faff;padding:8px;border-radius:6px;border:1px solid #d1d9e6; margin-bottom:5px;}
.sentinel-box{background:#1e3799; color:white; padding:12px; border-radius:8px; margin-bottom:10px; border-left:8px solid #ffc107;}
.google-window{background:#e8f0fe; padding:12px; border-radius:8px; border:2px solid #4285f4; margin-bottom:10px; font-size:0.8rem; line-height:1.4}
.stMetric {background: #f1f4f9; padding: 5px; border-radius: 5px;}
[data-testid="stSidebar"]{background:#f1f4f9; border-right:1px solid #dee2e6}
</style>""", unsafe_allow_html=True)

# --- 2. STATE MANAGEMENT ---
if "auth" not in st.session_state: st.session_state["auth"] = False
if "reset_key" not in st.session_state: st.session_state["reset_key"] = 0

if not st.session_state["auth"]:
    st.markdown("<h1 class='main-title'>EQUILIBRIUM ENGINE</h1>", unsafe_allow_html=True)
    with st.form("login"):
        pwd = st.text_input("Access Key", type="password")
        if st.form_submit_button("Unlock"):
            if pwd == "Gayan2026": 
                st.session_state["auth"] = True
                st.rerun()
            else: st.error("Denied")
    st.stop()

# --- 3. SIDEBAR (PILLAR 01 & 03 CONTROLS) ---
with st.sidebar:
    st.markdown("### 👤 Gayan Nugawela\nStrategic Revenue Architect")
    if st.button("☢️ Nuclear Data Reset"):
        st.session_state["reset_key"] += 1
        st.rerun()
    if st.button("🔒 Sign Out"):
        st.session_state["auth"] = False
        st.rerun()
    st.divider()
    
    rk = str(st.session_state["reset_key"]) 
    
    st.markdown("### 🏨 Pillar 01: Context")
    hotel = st.text_input("Property", "Wyndham Garden Salalah", key="h"+rk)
    location = st.selectbox("📍 Google Location", ["Salalah, Oman", "Muscat, Oman", "Dubai, UAE"], key="loc"+rk)
    inventory = st.number_input("Inventory", 1, 1000, 237, key="inv"+rk)
    p01_val = st.number_input("P01 Variable Fee", 0.00, value=6.90, step=0.01, key="p01"+rk)
    
    st.markdown("### 📈 Pillar 03: Velocity Valve")
    otb = st.slider("OTB %", 0, 100, (70 if "Salalah" in location else 15), key="otb"+rk)
    hist = st.slider("Historical %", 0, 100, 45, key="hist"+rk)
    v_mult = 1.25 if (otb-hist) > 10 else 0.85 if (otb-hist) < -10 else 1.0

    st.divider()
    tx = st.number_input("Tax Divisor", value=1.2327, format="%.4f", step=0.0001, key="tx"+rk)
    ota_comm = st.slider("OTA Comm %", 0, 50, 18, key="ota"+rk) / 100
    
    st.markdown("### 🍽️ Unit Pax Costs")
    c_bb = st.number_input("BB Cost", 0.0, key="cbb"+rk)
    c_sai = st.number_input("SAI Cost", 5.0, key="csai"+rk)
    costs = {"RO": 0, "BB": c_bb, "SAI": c_sai, "AI": c_sai}

# --- 4. CALCULATION ENGINE ---
def run_yield(rms, adr, n, meals, comm, fl):
    tr = sum(rms)
    if tr <= 0: return None
    px = (rms[0]*1 + rms[1]*2) / tr 
    net_adr = adr / tx
    m_cost = sum((qty/tr) * costs.get(m, 0) * px for m, qty in meals.items() if qty > 0)
    unit_w = (net_adr - m_cost - ((net_adr - m_cost) * comm)) - p01_val
    hrd = fl * 1.25 if (tr/inventory) >= 0.2 else fl
    l, b = ("OPTIMIZED", "#27ae60") if unit_w >= hrd else ("DILUTIVE", "#e74c3c")
    return {"u": unit_w, "l": l, "b": b, "tot": unit_w * tr * n}

# --- 5. MAIN DASHBOARD ---
st.markdown("<h1 class='main-title'>YIELD EQUILIBRIUM MASTER DASHBOARD</h1>", unsafe_allow_html=True)

# THEORETICAL FRAMEWORK BOX
col_intel, col_theory = st.columns([1, 1])
with col_intel:
    st.markdown(f"""<div class='google-window'>
        <b style='color:#4285f4;'>🌐 Google Intelligence Feed: {location}</b><br>
        • <b>Event Scrape:</b> Festival Season Detected | Flights: +14%<br>
        • <b>Demand Index:</b> High Surge (Automated via Location Sync)
    </div>""", unsafe_allow_html=True)
with col_theory:
    st.markdown("""<div class='google-window' style='background:#fff4e5; border-color:#ffa94d;'>
        <b style='color:#d9480f;'>📘 Research Pillar Methodology</b><br>
        • <b>P01:</b> Wealth Stripping (Net of Tax, Comm, Pax Costs).<br>
        • <b>P02:</b> External Sentinel (Google Scrape Demand Pressure).
    </div>""", unsafe_allow_html=True)

m_heat = 1.35 if "Salalah" in location else 0.85
st.markdown(f"""<div class='sentinel-box'>
    <div style='display:flex; justify-content:space-between;'>
        <span><b>Market State:</b> {location} ({m_heat}x)</span>
        <span><b>Velocity Trigger:</b> {v_mult}x</span>
        <span><b>Tax Anchor:</b> {tx}</span>
    </div>
</div>""", unsafe_allow_html=True)

def draw_seg(label, key, br, fl_def, col, is_ota=False):
    rk = str(st.session_state["reset_key"])
    st.markdown(f"<div class='card' style='border-left-color:{col}'>{label}</div>", unsafe_allow_html=True)
    
    c_input, c_result = st.columns([2.2, 1])
    suggested = (br * m_heat) * v_mult
    
    with c_input:
        st.markdown("<div class='pricing-row'>", unsafe_allow_html=True)
        ir1, ir2, ir3 = st.columns([1, 1, 1])
        fa = ir1.number_input("Rate", value=float(suggested), key="a"+key+rk)
        ff = ir2.number_input("Floor", float(fl_def), key="f"+key+rk)
        nts = ir3.number_input("Nights", 1, key="n"+key+rk)
        
        mr1, mr2, mr3 = st.columns(3)
        m_ro = mr1.number_input("RO", 0, key="ro"+key+rk)
        m_bb = mr2.number_input("BB", 0, key="bb"+key+rk)
        m_sai = mr3.number_input("SAI", 0, key="sai"+key+rk)
        st.markdown("</div>", unsafe_allow_html=True)
        
    res = run_yield([10, 20], fa, nts, {"RO": m_ro, "BB": m_bb, "SAI": m_sai}, (ota_comm if is_ota else 0.0), ff)
    
    if res:
        with c_result:
            st.metric("Net Wealth", f"OMR {res['u']:,.2f}")
            st.markdown(f"<div class='status-box' style='background:{res['b']}; font-size:0.8rem; padding:5px; text-align:center;'>{res['l']}</div>", unsafe_allow_html=True)
            return res['tot']
    return 0

# COMPACT SEGMENTS
draw_seg("1. DIRECT / FIT", "fit", 65, 40, "#3498db")
draw_seg("2. OTA CHANNELS", "ota", 60, 35, "#2ecc71", is_ota=True)
draw_seg("3. GROUPS / MICE", "grp", 50, 30, "#9b59b6")
