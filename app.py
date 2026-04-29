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
    c_bb = st.number_input("BB Cost", 0.0)
    c_hb = st.number_input("HB Cost", 0.0)
    c_fb = st.number_input("FB Cost", 0.0)
    c_sai = st.number_input("SAI Cost", 5.0)
    c_ai = st.number_input("AI Cost", 5.0)
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

# --- SEGMENT 1: FIT ---
st.markdown("<div class='card' style='border-left-color:#3498db'>1. DIRECT / FIT</div>", unsafe_allow_html=True)
f1, f2, f3 = st.columns([1, 1.8, 1.2])
with f1:
    fs = st.number_input("SGL Rooms", 0, key="fs")
    fd = st.number_input("DBL Rooms", 0, key="fd")
    fn = st.number_input("Nights", value=m_nights, key="fn")
with f2:
    f_sug = (65 * m_heat) * v_mult
    st.markdown(f"<div class='pricing-row'><div class='pricing-header'>SUGGESTED: {cu} {f_sug:,.2f}</div>", unsafe_allow_html=True)
    fa = st.number_input("Final Rate", value=float(f_sug), key="fa")
    ff = st.number_input("Floor Rate", 40.0, key="ff")
    fr = st.number_input("RO Pax", 0, key="fro")
    fb = st.number_input("BB Pax", 0, key="fbb")
    f_mx = {"RO": fr, "BB": fb}
    st.markdown("</div>", unsafe_allow_html=True)
res_f = run_yield([fs, fd, 0], fa, fn, f_mx, 0, ff)
if res_f:
    with f3:
        st.metric("Net Yield", f"{cu} {res_f['u']:,.2f}")
        st.markdown(f"<div class='status-box' style='background:{res_f['b']}'>{res_f['l']}</div>", unsafe_allow_html=True)
        st.session_state["ft"] = res_f['tot']

# --- SEGMENT 2: OTA ---
st.divider()
st.markdown("<div class='card' style='border-left-color:#2ecc71'>2. OTA CHANNELS</div>", unsafe_allow_html=True)
o1, o2, o3 = st.columns([1, 1.8, 1.2])
with o1:
    od = st.number_input("DBL Rooms", 0, key="od")
    on = st.number_input("Stay Nights", value=m_nights, key="on")
with o2:
    o_sug = (60 * m_heat) * v_mult
    st.markdown(f"<div class='pricing-row'><div class='pricing-header'>SUGGESTED: {cu} {o_sug:,.2f}</div>", unsafe_allow_html=True)
    oa = st.number_input("Applied Rate", value=float(o_sug), key="oa")
    of = st.number_input("Floor", 35.0, key="of")
    obb = st.number_input("BB Pax", 0, key="obb")
    osai = st.number_input("SAI Pax", 0, key="osai")
    o_mx = {"BB": obb, "SAI": osai}
    st.markdown("</div>", unsafe_allow_html=True)
res_o = run_yield([0, od, 0], oa, on, o_mx, ota_comm, of)
if res_o:
    with o3:
        st.metric("Net Yield", f"{cu} {res_o['u']:,.2f}")
        st.markdown(f"<div class='status-box' style='background:{res_o['b']}'>{res_o['l']}</div>", unsafe_allow_html=True)
        st.session_state["ot"] = res_o['tot']

# --- SEGMENT 3: GROUPS ---
st.divider()
st.markdown("<div class='card' style='border-left-color:#9b59b6'>3. CORPORATE GROUPS / MICE</div>", unsafe_allow_html=True)
g1, g2, g3 = st.columns([1, 1.8, 1.2])
with g1:
    gd = st.number_input("Group Rooms", 0, key="gd")
    gn = st.number_input("Group Nights", value=m_nights, key="gn")
with g2:
    g_sug = (50 * m_heat) * v_mult
    st.markdown(f"<div class='pricing-row'><div class='pricing-header'>SUGGESTED: {cu} {g_sug:,.2f}</div>", unsafe_allow_html=True)
    ga = st.number_input("Group Rate", value=float(g_sug), key="ga")
    gf = st.number_input("Floor", 30.0, key="gf")
    gai = st.number_input("AI Pax", 0, key="gai")
    gfb = st.number_input("FB Pax", 0, key="gfb")
    g_mx = {"AI": gai, "FB": gfb}
    gmice = st.number_input("MICE Revenue (Pax)", 0.0, key="gmice")
    st.markdown("</div>", unsafe_allow_html=True)
res_g = run_yield([0, gd, 0], ga, gn, g_mx, 0, gf, mice=gmice)
if res_g:
    with g3:
        st.metric("Net Yield", f"{cu} {res_g['u']:,.2f}")
        st.markdown(f"<div class='status-box' style='background:{res_g['b']}'>{res_g['l']}</div>", unsafe_allow_html=True)
        st.session_state["gt"] = res_g['tot']

# --- PORTFOLIO TOTAL ---
st.divider()
total_wealth = st.session_state.get("ft",0) + st.session_state.get("ot",0) + st.session_state.get("gt",0)
st.markdown(f"<div style='background:#1e3799;padding:20px;border-radius:12px;text-align:center;color:white;'><h3>Portfolio Wealth Total: {cu} {total_wealth:,.2f}</h3></div>", unsafe_allow_html=True)
