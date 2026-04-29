import streamlit as st
from datetime import date

# --- 1. STYLING ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium Master")
st.markdown("""<style>
.block-container{padding-top:1rem!important;}
.main-title{font-size:1.8rem!important;font-weight:900;color:#1e3799;text-align:center;margin-top:-10px;}
.card{padding:10px;border-radius:8px;margin-bottom:8px;border-left:10px solid;background:#ffffff;box-shadow: 0 2px 4px rgba(0,0,0,0.05)}
.pricing-row{background:#f8faff;padding:10px;border-radius:6px;border:1px solid #d1d9e6;}
.sentinel-box{background:#1e3799; color:white; padding:12px; border-radius:8px; margin-bottom:10px; border-left:8px solid #ffc107;}
.google-window{background:#e8f0fe; padding:10px; border-radius:8px; border:1px solid #4285f4; margin-bottom:10px; font-size:0.8rem;}
.status-indicator{padding:10px; border-radius:8px; text-align:center; font-weight:900; font-size:1.2rem; color:white; margin-top:5px;}
[data-testid="stSidebar"]{background:#f1f4f9; border-right:1px solid #dee2e6}
</style>""", unsafe_allow_html=True)

# --- 2. STATE & RESET ---
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

# --- 3. SIDEBAR (PILLAR 01: COSTS & STAY DATES) ---
with st.sidebar:
    st.markdown("### 👤 Strategic Architect\nGayan Nugawela")
    if st.button("☢️ Nuclear Data Reset"):
        st.session_state["reset_key"] += 1
        st.rerun()
    st.divider()
    
    rk = str(st.session_state["reset_key"]) 
    
    st.markdown("### 🏨 Pillar 01: Context & Costs")
    hotel = st.text_input("Property", "Wyndham Garden Salalah", key="h"+rk)
    location = st.selectbox("📍 Location", ["Salalah", "Muscat", "Dubai"], key="loc"+rk)
    
    # STAY DATES (P01)
    d1 = st.date_input("Check-In", date.today(), key="d1"+rk)
    d2 = st.date_input("Check-Out", date.today(), key="d2"+rk)
    m_nights = (d2 - d1).days if (d2 - d1).days > 0 else 1
    st.info(f"Analysis: {m_nights} Nights")

    inventory = st.number_input("Total Inventory", 1, 1000, 237, key="inv"+rk)
    p01_fee = st.number_input("P01 Variable Fee", 0.0, value=6.90, key="p01"+rk)
    tx = st.number_input("Tax Divisor", value=1.2327, format="%.4f", key="tx"+rk)
    
    st.markdown("### 🍽️ Master Meal Unit Costs")
    c_bb = st.number_input("BB Cost", 0.0, key="cbb"+rk)
    c_hb = st.number_input("HB Cost", 2.5, key="chb"+rk)
    c_fb = st.number_input("FB Cost", 5.0, key="cfb"+rk)
    c_sai = st.number_input("SAI Cost", 7.5, key="csai"+rk)
    c_ai = st.number_input("AI Cost", 10.0, key="cai"+rk)
    meal_costs = {"RO": 0, "BB": c_bb, "HB": c_hb, "FB": c_fb, "SAI": c_sai, "AI": c_ai}

    st.markdown("### 📈 Pillar 03: Velocity")
    otb = st.slider("OTB %", 0, 100, 15, key="otb"+rk)
    v_mult = 1.25 if otb > 60 else 1.0

# --- 4. ENGINE ---
def run_yield(rms, nts, adr, meals, floor, comm=0.18):
    total_rms = sum(rms)
    if total_rms <= 0: return None
    room_nights = total_rms * nts
    net_adr = adr / tx
    avg_meal_cost = sum(qty * meal_costs.get(m, 0) for m, qty in meals.items()) / total_rms
    # Wealth Strip
    wealth = (net_adr - avg_meal_cost - (net_adr * comm)) - p01_fee
    l, b = ("OPTIMIZED", "#27ae60") if wealth >= floor else ("DILUTIVE", "#e74c3c")
    return {"w": wealth, "l": l, "b": b, "rn": room_nights}

# --- 5. DASHBOARD ---
st.markdown("<h1 class='main-title'>YIELD EQUILIBRIUM MASTER DASHBOARD</h1>", unsafe_allow_html=True)

# INTEL WINDOW
st.markdown(f"""<div class='google-window'>
    <b>🌐 Google Intelligence Feed: {location}</b> | Stay Period: {d1} to {d2} ({m_nights} Nights)<br>
    • Scrape Data: Local Events Active | Demand Pressure: Moderate | Tax Anchor: {tx}
</div>""", unsafe_allow_html=True)

def draw_seg(label, key, br, fl, col, is_ota=False):
    rk = str(st.session_state["reset_key"])
    st.markdown(f"<div class='card' style='border-left-color:{col}'>{label}</div>", unsafe_allow_html=True)
    c1, c2 = st.columns([2.5, 1])
    
    with c1:
        st.markdown("<div class='pricing-row'>", unsafe_allow_html=True)
        r1, r2, r3 = st.columns(3)
        sgl = r1.number_input("SGL Rooms", 0, key="s"+key+rk)
        dbl = r2.number_input("DBL Rooms", 0, key="d"+key+rk)
        adr = r3.number_input("Final ADR", value=float(br), key="a"+key+rk)
        
        m1, m2, m3, m4, m5 = st.columns(5)
        mbb = m1.number_input("BB Pax", 0, key="bb"+key+rk)
        mhb = m2.number_input("HB Pax", 0, key="hb"+key+rk)
        mfb = m3.number_input("FB Pax", 0, key="fb"+key+rk)
        msai = m4.number_input("SAI Pax", 0, key="sai"+key+rk)
        mai = m5.number_input("AI Pax", 0, key="ai"+key+rk)
        st.markdown("</div>", unsafe_allow_html=True)
        
    res = run_yield([sgl, dbl], m_nights, adr, {"BB":mbb, "HB":mhb, "FB":mfb, "SAI":msai, "AI":mai}, fl, 0.18 if is_ota else 0.0)
    
    if res:
        with c2:
            st.metric("Net Wealth", f"OMR {res['w']:,.2f}")
            st.write(f"**Total Room Nights:** {res['rn']}")
            st.markdown(f"<div class='status-indicator' style='background:{res['b']}'>{res['l']}</div>", unsafe_allow_html=True)

# SEGMENTS
draw_seg("1. DIRECT / FIT", "fit", 65, 40, "#3498db")
draw_seg("2. OTA CHANNELS", "ota", 60, 35, "#2ecc71", is_ota=True)
draw_seg("3. CORPORATE / GROUPS", "grp", 50, 30, "#9b59b6")
