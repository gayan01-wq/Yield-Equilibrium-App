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
    with st.form("login"):
        pwd = st.text_input("Access Key", type="password")
        if st.form_submit_button("Unlock"):
            if pwd == "Gayan2026":
                st.session_state["auth"] = True
                st.rerun()
            else:
                st.error("Denied")
    st.stop()

# --- 3. SIDEBAR (MASTER CONTROLS) ---
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
    # THIS CALCULATES NIGHTS AUTOMATICALLY
    m_nights = (d2 - d1).days if (d2 - d1).days > 0 else 1
    st.info(f"Period: {m_nights} Nights")

    st.write("### 🌐 Market Sentinel")
    is_khareef = "Salalah" in hotel and (6 <= d1.month <= 9)
    m_state = st.radio("Demand Status", ["Crisis", "Stagnant", "Recovering", "Peak"], index=(3 if is_khareef else 0))
    m_heat = {"Crisis": 0.65, "Stagnant": 0.85, "Recovering": 1.0, "Peak": 1.35}[m_state]

    st.write("### 📈 Velocity (P03)")
    otb = st.slider("OTB %", 0, 100, (70 if is_khareef else 15))
    hist = st.slider("History %", 0, 100, 45)
    v_mult = 1.25 if (otb-hist) > 10 else 0.85 if (otb-hist) < -10 else 1.0

    st.divider()
    cu = st.selectbox("Currency", ["OMR", "AED", "USD"])
    tx = st.number_input("Tax Divisor", 1.2327)
    ota_comm = st.slider("OTA Comm %", 0, 50, 18) / 100
    
    st.write("### 🍽️ Pax Costs")
    c_bb = st.number_input("BB Pax Cost", 0.0)
    c_sai = st.number_input("SAI Pax Cost", 5.0)
    c_ai = st.number_input("AI Pax Cost", 5.0)
    costs = {"RO": 0, "BB": c_bb, "SAI": c_sai, "AI": c_ai}

# --- 4. CALCULATION LOGIC ---
def run_yield(rms, adr, n, meals, comm, fl, mice=0, trans=0):
    tr = sum(rms)
    if tr <= 0: return None
    px = (rms[0]*1 + rms[1]*2) / tr # Simple pax ratio
    net_adr = adr / tx
    m_cost = sum((qty/tr) * costs[m] * px for m, qty in meals.items() if qty > 0)
    unit_w = (net_adr - m_cost - ((net_adr - m_cost) * comm)) + ((mice * px)/(n * tx))
    total_w = (unit_w * tr * n) + (trans / tx)
    dy = total_w / (tr * n)
    hrd = fl * 1.25 if (tr/inventory) >= 0.2 else fl
    l, b = ("OPTIMIZED", "#27ae60") if dy >= hrd else ("DILUTIVE", "#e74c3c")
    return {"u": dy, "l": l, "b": b, "tot": total_w, "rn": tr * n}

# ---
