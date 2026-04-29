import streamlit as st
from datetime import date

# --- STYLING & CONFIG ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium Master Engine")

st.markdown("""<style>
.block-container{padding-top:1rem!important}
.main-title{font-size:2.5rem!important;font-weight:900;color:#1e3799;text-align:center;margin-top:-10px}
.sub-header{font-size:1rem;text-align:center;color:#4a69bd;font-weight:600;margin-bottom:15px}
.pillar-box{background:#fff;padding:12px;border-radius:10px;border-top:4px solid #1e3799;text-align:center;box-shadow:0 4px 10px rgba(0,0,0,0.05);min-height:100px}
.pillar-box h4{color:#1e3799;font-size:0.9rem;margin:0}
.card{padding:12px;border-radius:10px;margin-bottom:10px;border-left:10px solid;font-weight:bold;background:#fcfcfc}
.pricing-row{background:#f1f4f9;padding:10px;border-radius:8px;margin-top:8px;border:1px solid #1e3799}
.pricing-header{background:#1e3799;color:white;padding:3px 10px;border-radius:5px 5px 0 0;font-size:0.8rem;font-weight:bold;margin-bottom:5px}
.status-box{padding:12px;border-radius:12px;text-align:center;font-size:1.3rem;font-weight:bold;color:white;margin-bottom:8px}
.exposure-bar{padding:8px;border-radius:6px;font-weight:bold;text-align:center;color:#1e3799;background:#ffc107;margin-top:6px;font-size:0.85rem}
.sentinel-box{background:#1e3799; color:white; padding:20px; border-radius:10px; margin-bottom:20px; border-left:10px solid #ffc107; box-shadow: 0 4px 15px rgba(0,0,0,0.1);}
[data-testid="stSidebar"]{background:#f1f4f9;border-right:2px solid #3498db}
</style>""", unsafe_allow_html=True)

# --- AUTHENTICATION ---
if "auth" not in st.session_state:
    st.session_state["auth"] = False

if not st.session_state["auth"]:
    st.markdown("<h1 class='main-title'>EQUILIBRIUM ENGINE</h1>", unsafe_allow_html=True)
    with st.form("login"):
        pwd = st.text_input("Access Key", type="password")
        if st.form_submit_button("Unlock"):
            if pwd == "Gayan2026":
                st.session_state["auth"] = True
                st.rerun()
            else:
                st.error("Denied")
    st.stop()

# --- SIDEBAR: CONTROL CENTER ---
with st.sidebar:
    st.markdown("<p style='font-size:1.2rem;font-weight:800;color:#1e3799;margin:0;'>Gayan Nugawela</p><p style='font-size:0.8rem;margin:0;'>Strategic Revenue Architect</p>", unsafe_allow_html=True)
    st.divider()
    
    if st.button("🔒 Sign Out"):
        st.session_state["auth"] = False
        st.rerun()
        
    st.divider()
    hotel = st.text_input("📍 Property (Target)", "Wyndham Garden Salalah")
    h_tot = st.number_input("Inventory Count", 1, 5000, 237)
    
    st.write("### 📅 Stay Intelligence")
    today = date.today()
    d1 = st.date_input("Check-In", today)
    d2 = st.date_input("Check-Out", today)
    stay_n = (d2 - d1).days if (d2 - d1).days > 0 else 1
    st.info(f"Stay Duration: {stay_n} Nights")

    st.write("### 📈 Velocity Valve (P03)")
    otb_occ = st.slider("Current OTB %", 0, 100, 40)
    hist_occ = st.slider("Historical Avg %", 0, 100, 45)
    v_delta = otb_occ - hist_occ
    
    # P03 Logic
    v_mult = 1.25 if v_delta > 10 else 1.10 if v_delta > 0 else 0.95 if v_delta > -10 else 0.80

    st.divider()
    cu = st.selectbox("Currency", ["OMR","AED","SAR","USD","EUR"])
    tx = st.number_input("Tax Divisor", 1.2327, format="%.4f")
    ota_p = st.slider("OTA Commission %", 0, 50, 18) / 100

    st.write("### 🍽️ Meal Cost Base")
    m_bb = st.number_input("BB Cost", 0.0)
    m_hb = st.number_input("HB Cost", 0.0)
    m_fb = st.number_input("FB Cost", 0.0)
    m_sai = st.number_input("SAI Cost", 5.0)
    m_ai = st.number_input("AI Cost", 5.0)
    m_m = {"RO": 0.0, "BB": m_bb, "HB": m_hb, "FB": m_fb, "SAI": m_sai, "AI": m_ai}

# --- CALCULATIONS ---
def calc_w(rms, adr, n, meals, comm, fl):
    tot_r = sum(rms)
    if tot_r <= 0: return None
    px_r = (rms[0]*1 + rms[1]*2 + rms[2]*3) / tot_r
    u_n = adr / tx
    m_c = sum((qty/tot_r) * m_m[p] * px_r for p, qty in meals.items() if qty > 0)
    unit_w = (u_n - m_c - ((u_n - m_c) * comm))
    total_w = (unit_w * tot_r * n)
    d_u = total_w / (tot_r * n)
    
    hrd = fl * 1.25 if (tot_r / h_tot) >= 0.2 else fl
    if d_u < (hrd * 0.95): l, b = ("DILUTIVE", "#e74c3c")
    elif d_u < hrd: l, b = ("MARGINAL", "#ff9800")
    else: l, b = ("OPTIMIZED", "#27ae60")
    return {"u": d_u, "l": l, "b": b, "tot": total_w, "rn": tot_r * n}

# --- MAIN DASHBOARD ---
st.markdown("<h1 class='main-title'>YIELD EQUILIBRIUM MASTER</h1>", unsafe_allow_html=True)

# THE SENTINEL (Simulated Market Review)
market_status = st.select_slider("🤖 MARKET SENTINEL: Manual Peer Review Override", 
                                options=["Low Demand", "Fair", "High Demand", "Sold Out Set"], value="High Demand")
m_map = {"Low Demand": 0.85, "Fair": 1.0, "High Demand": 1.15, "Sold Out Set": 1.40}
m_heat = m_map[market_status]

st.markdown(f"""<div class='sentinel-box'>
    <h3 style='margin:0; color:#ffc107;'>🤖 PILLAR 02: MARKET SENTINEL</h3>
    <p style='margin:5px 0;'>Deep Scrape Analysis for: <b>{hotel}</b></p>
    <div style='display:flex; justify-content:space-around; align-items:center;'>
        <div><b>Market Intensity:</b> {market_status} ({m_heat}x)</div>
        <div><b>Booking Velocity:</b> {v_delta}% ({v_mult}x)</div>
    </div>
</div>""", unsafe_allow_html=True)

c_p1, c_p2, c_p3 = st.columns(3)
with c_p1: st.markdown("<div class='pillar-box'><h4>1. Wealth Stripping</h4><p style='font-size:0.75rem;'>Removing tax/cost overheads.</p></div>", unsafe_allow_html=True)
with c_p2: st.markdown("<div class='pillar-box'><h4>2. Market Sentinel</h4><p style='font-size:0.75rem;'>Automated peer hotel review.</p></div>", unsafe_allow_html=True)
with c_p3: st.markdown("<div class='pillar-box'><h4>3. Velocity Valve</h4><p style='font-size:0.75rem;'>Pace-driven price triggers.</p></div>", unsafe_allow_html=True)

def draw_s(title, key, d_adr, d_fl, color, is_o=False):
    st.markdown(f"<div class='card' style='border-left-color:{color}'>{title}</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.8, 1.2])
