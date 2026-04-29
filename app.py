import streamlit as st
from datetime import date

# --- 1. STYLING ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium Master Engine")
st.markdown("""<style>
.main-title{font-size:2.2rem!important;font-weight:900;color:#1e3799;text-align:center;margin-bottom:20px}
.card{padding:15px;border-radius:10px;margin-bottom:10px;border-left:10px solid;font-weight:bold;background:#fcfcfc}
.pricing-row{background:#f1f4f9;padding:12px;border-radius:8px;margin-top:8px;border:1px solid #1e3799}
.pricing-header{background:#1e3799;color:white;padding:5px 10px;border-radius:5px 5px 0 0;font-size:0.9rem;font-weight:bold}
.status-box{padding:10px;border-radius:10px;text-align:center;font-size:1.1rem;font-weight:bold;color:white}
.sentinel-box{background:#1e3799; color:white; padding:20px; border-radius:10px; margin-bottom:25px; border-left:10px solid #ffc107;}
[data-testid="stSidebar"]{background:#f8f9fa; border-right:1px solid #dee2e6}
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

# --- 3. SIDEBAR MASTER CONTROL ---
with st.sidebar:
    st.markdown("### 👤 Strategic Architect\n**Gayan Nugawela**")
    if st.button("🔒 Sign Out"):
        st.session_state["auth"] = False
        st.rerun()
    st.divider()
    
    hotel = st.text_input("Property (Google Sync)", "Wyndham Garden Salalah")
    inventory = st.number_input("Total Rooms", 1, 1000, 237)
    
    st.markdown("### 📅 Stay Intelligence")
    d1 = st.date_input("Check-In", date.today())
    d2 = st.date_input("Check-Out", date.today())
    m_nights = (d2 - d1).days if (d2 - d1).days > 0 else 1
    st.info(f"Stay Duration: {m_nights} Nights")

    st.markdown("### 🌐 Market Sentinel")
    is_khareef = "Salalah" in hotel and (6 <= d1.month <= 9)
    m_state = st.radio("Demand Status", ["Crisis", "Stagnant", "Recovering", "Peak"], index=(3 if is_khareef else 0))
    m_heat = {"Crisis": 0.65, "Stagnant": 0.85, "Recovering": 1.0, "Peak": 1.35}[m_state]

    st.markdown("### 📈 Velocity (P03)")
    otb = st.slider("OTB %", 0, 100, (70 if is_khareef else 15))
    hist = st.slider("History %", 0, 100, 45)
    v_mult = 1.25 if (otb-hist) > 10 else 0.85 if (otb-hist) < -10 else 1.0

    st.divider()
    cu = st.selectbox("Currency", ["OMR", "AED", "USD"])
    tx = st.number_input("Tax Divisor", 1.0, 2.0, 1.2327)
    ota_comm = st.slider("OTA Comm %", 0, 50, 18) / 100
    
    st.markdown("### 🍽️ Unit Pax Costs")
    c_bb = st.number_input("BB Cost", 0.0); c_hb = st.number_input("HB Cost", 0.0); c_fb = st.number_input("FB Cost", 0.0)
    c_sai = st.number_input("SAI Cost", 5.0); c_ai = st.number_input("AI Cost", 5.0)
    costs = {"RO": 0, "BB": c_bb, "HB": c_hb, "FB": c_fb, "SAI": c_sai, "AI": c_ai}

# --- 4. CALCULATION ENGINE ---
def run_yield(rms, adr, n, meals, comm, fl, mice=0, trans=0):
    tr = sum(rms)
    if tr <= 0: return None
    px = (rms[0]*1 + rms[1]*2 + rms[2]*3) / tr
    net_adr = adr / tx
    m_cost_unit = sum((qty/tr) * costs.get(m, 0) * px for m, qty in meals.items() if qty > 0)
    unit_w = (net_adr - m_cost_unit - ((net_adr - m_cost_unit) * comm)) + ((mice * px)/(n * tx))
    total_w = (unit_w * tr * n) + (trans / tx)
    dy = total_w / (tr * n)
    hrd = fl * 1.25 if (tr/inventory) >= 0.2 else fl
    l, b = ("OPTIMIZED", "#27ae60") if dy >= hrd else ("DILUTIVE", "#e74c3c")
    return {"u": dy, "l": l, "b": b, "tot": total_w, "rn": tr * n}

# --- 5. MAIN DASHBOARD ---
st.markdown("<h1 class='main-title'>YIELD EQUILIBRIUM MASTER</h1>", unsafe_allow_html=True)

st.markdown(f"""<div class='sentinel-box'>
    <h3 style='margin:0; color:#ffc107;'>🤖 PILLAR 02: MARKET SENTINEL</h3>
    <div style='display:flex; justify-content:space-between; margin-top:10px;'>
        <span><b>Market Heat:</b> {m_state} ({m_heat}x)</span>
        <span><b>Velocity Multiplier:</b> {v_mult}x</span>
        <span><b>Master Stay:</b> {m_nights} Nights</span>
    </div>
</div>""", unsafe_allow_html=True)

# Helper for segments to avoid syntax errors
def draw_segment(title, key, base_r, floor, color, is_ota=False, is_group=False):
    st.markdown(f"<div class='card' style='border-left-color:{color}'>{title}</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.8, 1.2])
    suggested = (base_r * m_heat) * v_mult
    
    with c1:
        s = st.number_input("SGL", 0, key=key+"s")
        d = st.number_input("DBL", 0, key=key+"d")
        n = st.number_input("Nights", value=m_nights, key=key+"n")
    with c2:
        st.markdown(f"<div class='pricing-row'><div class='pricing-header'>SUGGESTED: {cu} {suggested:,.2f}</div>", unsafe_allow_html=True)
        adr = st.number_input("Applied Rate", value=float(suggested), key=key+"a")
        fl = st.number_input("Floor", float(floor), key=key+"f")
        mc = st.columns(3)
        m_ro = mc[0].number_input("RO Pax", 0, key=key+"ro")
        m_bb = mc[0].number_input("BB Pax", 0, key=key+"bb")
        m_hb = mc[1].number_input("HB Pax", 0, key=key+"hb")
        m_fb = mc[1].number_input("FB Pax", 0, key=key+"fb")
        m_sai = mc[2].number_input("SAI Pax", 0, key=key+"sai")
        m_ai = mc[2].number_input("AI Pax", 0, key=key+"ai")
        mx = {"RO": m_ro, "BB": m_bb, "HB": m_hb, "FB": m_fb, "SAI": m_sai, "AI": m_ai}
        
        mi, tr = 0.0, 0.0
        if is_group:
            gc = st.columns(2)
            mi = gc[0].number_input("MICE Revenue", 0.0, key=key+"mi")
            tr = gc[1].number_input("Trans. Total", 0.0, key=key+"tr")
        st.markdown("</div>", unsafe_allow_html=True)
        
    res = run_yield([s, d, 0], adr, n, mx, (ota_comm if is_ota else 0), fl, mi, tr)
    if res:
        with c3:
            st.metric("Net Yield", f"{cu} {res['u']:,.2f}")
            st.markdown(f"<div class='status-box' style='background:{res['b']}'>{res['l']}</div>", unsafe_allow_html=True)
            st.write(f"Wealth: {res['tot']:,.2f}")
            return res['tot']
    return 0

# DRAWING THE 5 PILLARS OF THE PORTFOLIO
t_fit = draw_segment("1. DIRECT / FIT", "fit", 65, 40, "#3498db")
st.divider()
t_ota = draw_segment("2. OTA CHANNELS", "ota", 60, 35, "#2ecc71", is_ota=True)
st.divider()
t_corp = draw_segment("3. CORPORATE / GOV", "corp", 55, 38, "#34495e")
st.divider()
t_cgrp = draw_segment("4. CORPORATE GROUPS", "cgrp", 50, 30, "#9b59b6", is_group=True)
st.divider()
t_tnt = draw_segment("5. GROUP TOUR & TRAVEL", "tnt", 45, 25, "#e67e22", is_group=True)

# PORTFOLIO TOTAL
st.divider()
total_p = t_fit + t_ota + t_corp + t_cgrp + t_tnt
st.markdown(f"<div style='background:#1e3799;padding:20px;border-radius:12px;text-align:center;color:white;'><h3>Portfolio Wealth Total: {cu} {total_p:,.2f}</h3></div>", unsafe_allow_html=True)
