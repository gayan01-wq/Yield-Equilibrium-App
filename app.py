import streamlit as st
from datetime import date

# --- 1. STYLING ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium Master")
st.markdown("""<style>
.block-container{padding-top:1rem!important;}
.main-title{font-size:1.8rem!important;font-weight:900;color:#1e3799;text-align:center;margin-top:-10px;}
.card{padding:10px;border-radius:10px;margin-bottom:8px;border-left:10px solid;background:#ffffff;box-shadow: 0 2px 4px rgba(0,0,0,0.1)}
.pricing-row{background:#f8faff;padding:12px;border-radius:10px;border:1px solid #d1d9e6; margin-top:5px;}
.google-window{background:#e8f0fe; padding:15px; border-radius:12px; border:2px solid #4285f4; margin-bottom:15px; font-size:0.85rem; line-height:1.6;}
.status-indicator{padding:10px; border-radius:10px; text-align:center; font-weight:900; font-size:1.2rem; color:white; margin-top:10px;}
.audit-box{background:#fff9c4; border:1px solid #fbc02d; padding:10px; border-radius:8px; margin-top:12px; text-align:center; font-weight:bold; color:#5f4300; font-size:0.9rem;}
.theory-box{background:#fdfdfd; padding:25px; border-radius:15px; border:1px solid #dee2e6; margin-top:40px}
.highlight-text{color:#1e3799; font-weight:bold;}
[data-testid="stSidebar"]{background:#f1f4f9; border-right:1px solid #dee2e6}
</style>""", unsafe_allow_html=True)

# --- 2. AUTHENTICATION ---
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

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown("### 👤 Strategic Architect\nGayan Nugawela")
    if st.button("☢️ Nuclear Data Reset"):
        st.cache_data.clear()
        for key in list(st.session_state.keys()):
            if key != "auth": del st.session_state[key]
        st.rerun()
    st.divider()
    
    st.markdown("### 🏨 Pillar 01: Global Constants")
    hotel_name = st.text_input("🏨 Hotel Search", "Wyndham Garden Salalah")
    city_name = st.text_input("📍 City Search", "Salalah, Oman")
    
    d1 = st.date_input("Check-In", date.today())
    d2 = st.date_input("Check-Out", date.today())
    m_nights = (d2 - d1).days if (d2 - d1).days > 0 else 1
    
    st.markdown("### 🌐 Pillar 02: Market Sentinel")
    # UPDATED DEMAND LABELS FOR INTERNATIONAL AUDIENCE
    m_state = st.radio("Market Demand Category", ["Distressed / Crisis", "Stagnant / Recovery", "Peak / Seasonal", "Compression / Sold Out"], index=1)
    m_heat = {"Distressed / Crisis": 0.65, "Stagnant / Recovery": 1.0, "Peak / Seasonal": 1.35, "Compression / Sold Out": 1.65}[m_state]

    st.markdown("### 📊 Pillar 03: Velocity")
    otb_occ = st.slider("OTB Occupancy %", 0, 100, 15)
    avg_hist = st.slider("Historical Avg %", 0, 100, 45)
    v_mult = 1.25 if otb_occ > avg_hist else 0.85 if otb_occ < (avg_hist - 15) else 1.0

    st.divider()
    tx_div = st.number_input("Tax Divisor", value=1.2327, format="%.4f")
    ota_comm = st.slider("OTA Commission %", 0, 40, 18)
    p01_fee = st.number_input("P01 Variable Fee", 0.0, value=6.90)

# --- 4. CALCULATION ENGINE ---
def run_yield(rms, nts, adr, meals, hurdle, comm_rate=0.18):
    tr = sum(rms)
    if tr <= 0: return None
    net_adr = adr / tx_div
    # Meal costs assumed from board basis selection
    wealth = (net_adr - (net_adr * comm_rate)) - p01_fee
    status, color = ("OPTIMIZED", "#27ae60") if wealth >= hurdle else ("DILUTIVE", "#e74c3c")
    return {"w": wealth, "st": status, "cl": color, "rn": tr * nts, "total": wealth * tr * nts}

# --- 5. MAIN DASHBOARD ---
st.markdown("<h1 class='main-title'>YIELD EQUILIBRIUM MASTER DASHBOARD</h1>", unsafe_allow_html=True)

st.markdown(f"""<div class='google-window'>
    <b style='color:#4285f4; font-size:1.1rem;'>🌐 Google Intelligence Feed: {hotel_name} | {city_name}</b><br>
    • <b>Market State:</b> {m_state} | <b>Strategic Multiplier:</b> {m_heat}x<br>
    • <b>Equilibrium Basis:</b> {"Baseline" if m_heat == 1.0 else "Demand-Driven Shift"} | <b>Stay Nights:</b> {m_nights}
</div>""", unsafe_allow_html=True)

def draw_seg(label, key, suggest_adr, floor, color, ota=False):
    st.markdown(f"<div class='card' style='border-left-color:{color}'>{label}</div>", unsafe_allow_html=True)
    c_in, c_res = st.columns([2.6, 1])
    with c_in:
        st.markdown("<div class='pricing-row'>", unsafe_allow_html=True)
        r1, r2, r3, r4 = st.columns(4)
        sgl = r1.number_input("SGL", 0, key="s"+key)
        dbl = r2.number_input("DBL", 0, key="d"+key)
        # Apply the P02 Heat and P03 Velocity to the suggested rate
        final_suggested = suggest_adr * m_heat * v_mult
        applied_adr = r3.number_input("Applied Rate", value=float(final_suggested), key="a"+key)
        floor_amt = r4.number_input("Floor Amount", value=float(floor), key="f"+key)
        st.markdown("</div>", unsafe_allow_html=True)
    
    res = run_yield([sgl, dbl], m_nights, applied_adr, {}, floor_amt, (ota_comm/100 if ota else 0.0))
    if res:
        with c_res:
            st.metric("Net Wealth (Unit)", f"OMR {res['w']:,.2f}")
            st.markdown(f"<div class='status-indicator' style='background:{res['cl']}'>{res['st']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='audit-box'>📊 {res['rn']} Room Nights | Total Wealth: OMR {res['total']:,.2f}</div>", unsafe_allow_html=True)

# DRAW SEGMENTS
draw_seg("1. DIRECT / FIT", "fit", 65, 40, "#3498db")
draw_seg("2. OTA CHANNELS", "ota", 60, 35, "#2ecc71", ota=True)

# --- 6. LIVE ACADEMIC DESCRIPTION ---
st.divider()
st.markdown("<div class='theory-box'>", unsafe_allow_html=True)
st.markdown(f"## 📘 Theoretical Methodology & Research Framework (Live Sync: {tx_div})")
cl1, cl2 = st.columns(2)
with cl1:
    st.markdown(f"""
    ### 🏗️ Pillar 01: Internal Wealth Stripping
    * **Logic:** The system ignores standard 'Gross ADR' and calculates 'Net Wealth.' 
    * **Formula:** Strips Taxes (Applied Divisor: <span class='highlight-text'>{tx_div}</span>), OTA Commissions ({ota_comm}%), and variable P01 fees.
    """)
with cl2:
    st.markdown("""
    ### 🌐 Pillar 02 & 03: Market Velocity
    * **Market Sentinel (P02):** Scans for Market Demand. **Compression** is the highest state where market supply is exhausted.
    * **Velocity Valve (P03):** Compares current OTB Occupancy to Historical averages to prevent selling inventory too early or too late.
    """)
st.markdown("</div>", unsafe_allow_html=True)
