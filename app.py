import streamlit as st
from datetime import date

# --- CONFIG & STYLE ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium Master Engine")
st.markdown("""<style>
.main-title{font-size:2.2rem!important;font-weight:900;color:#1e3799;text-align:center;margin-bottom:20px}
.card{padding:15px;border-radius:10px;margin-bottom:10px;border-left:10px solid;font-weight:bold;background:#fcfcfc;box-shadow: 2px 2px 5px rgba(0,0,0,0.05)}
.pricing-row{background:#f1f4f9;padding:12px;border-radius:8px;margin-top:8px;border:1px solid #1e3799}
.pricing-header{background:#1e3799;color:white;padding:5px 10px;border-radius:5px 5px 0 0;font-size:0.9rem;font-weight:bold}
.status-box{padding:10px;border-radius:10px;text-align:center;font-size:1.1rem;font-weight:bold;color:white}
.sentinel-box{background:#1e3799; color:white; padding:20px; border-radius:10px; margin-bottom:25px; border-left:10px solid #ffc107;}
[data-testid="stSidebar"]{background:#f8f9fa; border-right:1px solid #dee2e6}
</style>""", unsafe_allow_html=True)

# --- AUTH ---
if "auth" not in st.session_state: st.session_state["auth"] = False
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

# --- SIDEBAR & MASTER INPUTS ---
with st.sidebar:
    st.markdown("### 👤 Strategic Architect\n**Gayan Nugawela**")
    if st.button("🔒 Sign Out"):
        st.session_state["auth"] = False
        st.rerun()
    st.divider()
    
    hotel_name = st.text_input("🏨 Property Search", "Wyndham Garden Salalah")
    inventory = st.number_input("Total Inventory", 1, 1000, 237)
    
    st.markdown("### 📅 Stay Intelligence")
    d1 = st.date_input("Check-In", date.today())
    d2 = st.date_input("Check-Out", date.today())
    # MASTER NIGHT CALCULATION
    master_nights = (d2 - d1).days if (d2 - d1).days > 0 else 1
    st.info(f"Stay Duration: {master_nights} Nights")

    st.markdown("### 🌐 Market Condition")
    # Khareef Detection
    is_khareef = "Salalah" in hotel_name and (6 <= d1.month <= 9)
    m_state = st.radio("Market Sentinel Status", ["Crisis", "Stagnant", "Recovering", "Peak"], index=(3 if is_khareef else 0))
    m_heat = {"Crisis": 0.65, "Stagnant": 0.85, "Recovering": 1.0, "Peak": 1.35}[m_state]

    st.markdown("### 📈 Velocity (P03)")
    otb = st.slider("Current OTB %", 0, 100, (70 if is_khareef else 15))
    hist = st.slider("Historical Avg %", 0, 100, 45)
    v_mult = 1.25 if (otb-hist) > 10 else 0.85 if (otb-hist) < -10 else 1.0

    st.divider()
    cu = st.selectbox("Currency", ["OMR", "AED", "USD"])
    tx = st.number_input("Tax Divisor", 1.0, 2.0, 1.2327)
    ota_comm = st.slider("OTA %", 0, 50, 18) / 100

    st.markdown("### 🍽️ Pax Costs")
    c_bb = st.number_input("BB Cost", 0.0); c_hb = st.number_input("HB Cost", 0.0); c_fb = st.number_input("FB Cost", 0.0)
    c_sai = st.number_input("SAI Cost", 5.0); c_ai = st.number_input("AI Cost", 5.0)
    costs = {"RO":0, "BB":c_bb, "HB":c_hb, "FB":c_fb, "SAI":c_sai, "AI":c_ai}

# --- CALCULATION ENGINE ---
def run_yield(rms, adr, n, meals, comm, fl, mice=0, trans=0):
    tr = sum(rms)
    if tr <= 0: return None
    px = (rms[0]*1 + rms[1]*2 + rms[2]*3) / tr
    net_adr = adr / tx
    m_cost = sum((qty/tr) * costs[m] * px for m, qty in meals.items() if qty > 0)
    unit_w = (net_adr - m_cost - ((net_adr - m_cost) * comm)) + ((mice * px)/(n * tx))
    total_w = (unit_w * tr * n) + (trans / tx)
    dy = total_w / (tr * n)
    hrd = fl * 1.25 if (tr/inventory) >= 0.2 else fl
    l, b = ("OPTIMIZED","#27ae60") if dy >= hrd else ("DILUTIVE","#e74c3c")
    return {"u": dy, "l": l, "b": b, "tot": total_w, "rn": tr * n}

# --- MAIN DASHBOARD ---
st.markdown("<h1 class='main-title'>YIELD EQUILIBRIUM MASTER</h1>", unsafe_allow_html=True)

if is_khareef: st.success(f"🌦️ Khareef Seasonal Demand logic applied for {hotel_name}")

st.markdown(f"""<div class='sentinel-box'>
    <h3 style='margin:0; color:#ffc107;'>🤖 PILLAR 02: MARKET SENTINEL</h3>
    <div style='display:flex; justify-content:space-between; margin-top:10px;'>
        <span><b>Strength:</b> {m_state} ({m_heat}x)</span>
        <span><b>Velocity:</b> {(otb-hist)}% (x{v_mult})</span>
        <span><b>Global Period:</b> {master_nights} Nights</span>
    </div>
</div>""", unsafe_allow_html=True)

# THE 5 SEGMENTS
segments = [
    ("1. DIRECT / FIT", "fit", 65, 40, "#3498db", False, False),
    ("2. OTA CHANNELS", "ota", 60, 35, "#2ecc71", True, False),
    ("3. CORPORATE / GOV", "corp", 55, 38, "#34495e", False, False),
    ("4. CORPORATE GROUPS", "cgrp", 50, 30, "#9b59b6", False, True),
    ("5. GROUP TOUR & TRAVEL", "tnt", 45, 25, "#e67e22", False, True)
]

total_portfolio_wealth = 0.0

for title, key, base_r, floor, color, is_ota, is_group in segments:
    st.markdown(f"<div class='card' style='border-left-color:{color}'>{title}</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.8, 1.2])
    
    suggested = (base_r * m_heat) * v_mult
    
    with c1:
        s = st.number_input("SGL", 0, key=key+"s")
        d = st.number_input("DBL", 0, key=key+"d")
        n = st.number_input("Nights", value=master_nights, key=key+"n")
    with c2:
        st.markdown(f"<div class='pricing-row'><div class='pricing-
