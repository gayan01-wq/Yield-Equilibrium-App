import streamlit as st
from datetime import date

# --- 1. STYLING (Executive Centering) ---
st.set_page_config(layout="wide", page_title="Displacement Analyzer | Yield Equilibrium")
st.markdown("""<style>
.block-container{padding-top:1rem!important;}
.main-title{font-size:2.2rem!important; font-weight:900; color:#1e3799; text-align:center; width:100%; display:block; text-transform:uppercase; margin-bottom:0px;}
.main-subtitle{font-size:1.1rem!important; font-weight:600; color:#4b6584; text-align:center; width:100%; display:block; margin-top:5px; margin-bottom:25px;}
.card{padding:10px; border-radius:10px; margin-bottom:8px; border-left:10px solid; background:#ffffff; box-shadow: 0 2px 4px rgba(0,0,0,0.1)}
.pricing-row{background:#f8faff; padding:12px; border-radius:10px; border:1px solid #d1d9e6;}
.status-indicator{padding:12px; border-radius:10px; text-align:center; font-weight:900; color:white; margin-top:10px;}
[data-testid="stSidebar"]{background:#f1f4f9;}
</style>""", unsafe_allow_html=True)

# --- 2. AUTHENTICATION ---
if "auth" not in st.session_state: st.session_state["auth"] = False
if not st.session_state["auth"]:
    st.markdown("<h1 class='main-title'>EQUILIBRIUM ENGINE</h1>", unsafe_allow_html=True)
    with st.form("login"):
        pwd = st.text_input("Access Key", type="password")
        if st.form_submit_button("Unlock"):
            if pwd == "Gayan2026": st.session_state["auth"] = True; st.rerun()
            else: st.error("Denied")
    st.stop()

# --- 3. SIDEBAR (STRATEGIC INPUTS) ---
with st.sidebar:
    st.markdown("### 👤 Developer: Gayan Nugawela")
    if st.button("🧹 Clear Cache"): st.rerun()
    st.divider()
    cur = st.selectbox("Currency", ["﷼", "රු", "฿", "د.إ", "₹", "$"])
    city = st.text_input("City Search", "Salalah")
    d1 = st.date_input("Check-In", date.today()); d2 = st.date_input("Check-Out", date.today())
    m_nts = (d2 - d1).days if (d2 - d1).days > 0 else 1
    st.info(f"📅 {m_nts} Nights Stay")
    
    st.divider()
    otb, hst = st.slider("OTB %", 0, 100, 15), st.slider("Hist. %", 0, 100, 45)
    v_mult = 1.35 if otb > hst else 0.85 if otb < (hst - 15) else 1.0
    tx = st.number_input("Tax Divisor", value=1.2327, format="%.4f")
    ota_c = st.slider("OTA Comm %", 0, 40, 15)
    p01 = st.number_input(f"P01 Fee ({cur})", value=6.90)
    
    st.markdown("### 🍽️ Unit Costs")
    mc = {"RO":0, "BB":st.number_input("BB Cost", 2.5), "LN":st.number_input("LN Cost", 4.5), 
          "DN":st.number_input("DN Cost", 5.5), "SAI":st.number_input("SAI Cost", 8.5), "AI":st.number_input("AI Cost", 10.5)}

# --- 4. ENGINE ---
def run_yield(rms, adr, meals, hurdle, demand, is_ota=False):
    tr = sum(rms)
    if tr <= 0: return None
    d_adj = {"Compression (Peak)":15, "High Flow":5, "Standard":0, "Distressed":-5}
    eff_hurdle = hurdle + d_adj.get(demand, 0)
    net_adr = adr / tx
    avg_m = sum(qty * mc.get(p, 0) for p, qty in meals.items()) / tr
    comm = (net_adr * (ota_c / 100)) if is_ota else 0.0
    unit_w = (net_adr - avg_m - comm) - p01
    status = "ACCEPT" if unit_w >= eff_hurdle else "REJECT"
    color = "#27ae60" if unit_w >= eff_hurdle else "#e74c3c"
    return {"w": unit_w, "st": status, "cl": color, "total": unit_w * tr * m_nts}

# --- 5. DASHBOARD ---
st.markdown("""<div style='text-align: center; width: 100%;'><h1 class='main-title'>DISPLACEMENT ANALYZER</h1>
<div class='main-subtitle'>Yield Equilibrium Strategic Intelligence Engine</div></div>""", unsafe_allow_html=True)

st.success(f"📍 {city} | 📈 Velocity: {v_mult}x | 📅 Length of Stay: {m_nts} Nights")

def draw_seg(label, key, suggest_adr, floor, color, is_ota=False):
    st.markdown(f"<div class='card' style='border-left-color:{color}'>{label}</div>", unsafe_allow_html=True)
    c_in, c_res = st.columns([2.6, 1])
    with c_in:
        st.markdown("<div class='pricing-row'>", unsafe_allow_html=True)
        r1, r2, r3, r4 = st.columns([0.8, 0.8, 0.8, 1.5])
        sgl, dbl, tpl = r1.number_input("SGL",0,key="s"+key), r2.number_input("DBL",0,key="d"+key), r3.number_input("TPL",0,key="t"+key)
        rate = r4.number_input(f"Rate ({cur})", value=
