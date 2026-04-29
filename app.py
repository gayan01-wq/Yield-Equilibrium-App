import streamlit as st
from datetime import date

# --- 1. STYLING ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium Master")
st.markdown("""<style>
.main-title{font-size:2.2rem!important;font-weight:900;color:#1e3799;text-align:center;margin-bottom:20px}
.card{padding:15px;border-radius:10px;margin-bottom:10px;border-left:10px solid;font-weight:bold;background:#fcfcfc}
.pricing-row{background:#f1f4f9;padding:12px;border-radius:8px;margin-top:8px;border:1px solid #1e3799}
.pricing-header{background:#1e3799;color:white;padding:5px 10px;border-radius:5px 5px 0 0;font-size:0.9rem;font-weight:bold}
.status-box{padding:10px;border-radius:10px;text-align:center;font-size:1.1rem;font-weight:bold;color:white}
.sentinel-box{background:#1e3799; color:white; padding:20px; border-radius:10px; margin-bottom:25px; border-left:10px solid #ffc107;}
</style>""", unsafe_allow_html=True)

# --- 2. AUTHENTICATION ---
if "auth" not in st.session_state:
    st.session_state["auth"] = False

if not st.session_state["auth"]:
    st.markdown("<h1 class='main-title'>EQUILIBRIUM ENGINE</h1>", unsafe_allow_html=True)
    with st.container():
        pwd = st.text_input("Access Key", type="password")
        if st.button("Unlock Engine"):
            if pwd == "Gayan2026":
                st.session_state["auth"] = True
                st.rerun()
            else:
                st.error("Access Denied")
    st.stop()

# --- 3. THE MAIN APP (ONLY SHOWS IF AUTH IS TRUE) ---
# SIDEBAR MASTER INPUTS
with st.sidebar:
    st.markdown("### 👤 Gayan Nugawela")
    if st.button("🔒 Sign Out"):
        st.session_state["auth"] = False
        st.rerun()
    st.divider()
    
    hotel = st.text_input("🏨 Property", "Wyndham Garden Salalah")
    inventory = st.number_input("Inventory", 1, 1000, 237)
    
    st.write("### 📅 Stay Intelligence")
    d1 = st.date_input("Check-In", date.today())
    d2 = st.date_input("Check-Out", date.today())
    m_nights = (d2 - d1).days if (d2 - d1).days > 0 else 1
    st.info(f"Analysis Period: {m_nights} Nights")

    st.write("### 🌐 Market Sentinel")
    is_khareef = "Salalah" in hotel and (6 <= d1.month <= 9)
    m_state = st.radio("Market Heat", ["Crisis", "Stagnant", "Recovering", "Peak"], index=(3 if is_khareef else 0))
    m_heat = {"Crisis": 0.65, "Stagnant": 0.85, "Recovering": 1.0, "Peak": 1.35}[m_state]

    st.write("### 📈 Velocity (P03)")
    otb = st.slider("OTB %", 0, 100, (70 if is_khareef else 15))
    hist = st.slider("History %", 0, 100, 45)
    v_mult = 1.25 if (otb-hist) > 10 else 0.85 if (otb-hist) < -10 else 1.0

    st.divider()
    cu = st.selectbox("Currency", ["OMR", "AED", "USD"])
    tx = st.number_input("Tax Divisor", 1.2327)
    ota_comm = st.slider("OTA Comm %", 0, 50, 18) / 100
    
    st.write("### 🍽️ Meal Costs")
    c_bb = st.number_input("BB Cost", 0.0)
    c_sai = st.number_input("SAI Cost", 5.0)
    c_ai = st.number_input("AI Cost", 5.0)
    # Master Cost Dictionary
    m_costs = {"RO": 0, "BB": c_bb, "SAI": c_sai, "AI": c_ai, "HB": c_bb + 3.0, "FB": c_bb + 6.0}

# --- CALCULATION ENGINE ---
def run_yield(rms, adr, n, meals, comm, fl, mice=0, trans=0):
    tr = sum(rms)
    if tr <= 0: return None
    px_ratio = (rms[0]*1 + rms[1]*2) / tr 
    net_adr = adr / tx
    m_cost_unit = sum((qty/tr) * m_costs.get(m, 0) * px_ratio for m, qty in meals.items() if qty > 0)
    unit_w = (net_adr - m_cost_unit - ((net_adr - m_cost_unit) * comm)) + ((mice * px_ratio)/(n * tx))
    total_w = (unit_w * tr * n) + (trans / tx)
    dy = total_w / (tr * n)
    hrd = fl * 1.25 if (tr/inventory) >= 0.2 else fl
    l, b = ("OPTIMIZED", "#27ae60") if dy >= hrd else ("DILUTIVE", "#e74c3c")
    return {"u": dy, "l": l, "b": b, "tot": total_w, "rn": tr * n}

# --- 4. MAIN INTERFACE RENDER ---
st.markdown("<h1 class='main-title'>YIELD EQUILIBRIUM MASTER</h1>", unsafe_allow_html=True)

st.markdown(f"""<div class='sentinel-box'>
    <h3 style='margin:0; color:#ffc107;'>🤖 PILLAR 02: MARKET SENTINEL</h3>
    <div style='display:flex; justify-content:space-between; margin-top:10px;'>
        <span><b>Strength:</b> {m_state} ({m_heat}x)</span>
        <span><b>Velocity:</b> {otb-hist}%</span>
        <span><b>Master Nights:</b> {m_nights}</span>
    </div>
</div>""", unsafe_allow_html=True)

if is_khareef: st.success(f"⛈️ KHAREEF AUTOMATION ACTIVE for {hotel}")

# SEGMENT 1: FIT
st.markdown("<div class='card' style='border-left-color:#3498db'>1. DIRECT / FIT</div>", unsafe_allow_html=True)
f1, f2, f3 = st.columns([1, 1.8, 1.2])
with f1:
    fs = st.number_input("SGL Rooms", 0, key="fs")
    fd = st.number_input("DBL Rooms", 0, key="fd")
    fn = st.number_input("Stay Nights", value=m_nights, key="fn")
with f2:
    f_sug = (65 * m_heat) * v_mult
    st.markdown(f"<div class='pricing-row'><div class='pricing-header'>SUGGESTED: {cu} {f_sug:,.2f}</div>", unsafe_allow_html=True)
    fa = st.number_input("Final Rate", value=float(f_sug), key="fa")
    ff = st.number_input("Min Floor", 40.0, key="ff")
    f_mx = {"RO": st.number_input("RO Qty", 0, key="fro"), "BB": st.number_input("BB Qty", 0, key="fbb")}
    st.markdown("</div>", unsafe_allow_html=True)
rf = run_yield([fs, fd], fa, fn, f_mx, 0, ff)
if rf:
    with f3:
        st.metric("Net Yield", f"{cu} {rf['u']:,.2f}")
        st.markdown(f"<div class='status-box' style='background:{rf['b']}'>{rf['l']}</div>", unsafe_allow_html=True)

# SEGMENT 2: OTA
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
    of = st.number_input("Min Floor", 35.0, key="of")
    o_mx = {"BB": st.number_input("BB
