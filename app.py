import streamlit as st
from datetime import date

# --- 1. STYLING (Executive Centering) ---
st.set_page_config(layout="wide", page_title="Displacement Analyzer")
st.markdown("""<style>
.main-title{font-size:2.2rem!important; font-weight:900; color:#1e3799; text-align:center; width:100%; display:block; text-transform:uppercase; margin-bottom:0px;}
.main-subtitle{font-size:1.1rem!important; font-weight:600; color:#4b6584; text-align:center; width:100%; display:block; margin-top:5px; margin-bottom:25px;}
.card{padding:10px; border-radius:10px; margin-bottom:8px; border-left:10px solid; background:#ffffff; box-shadow: 0 2px 4px rgba(0,0,0,0.1)}
.pricing-row{background:#f8faff; padding:12px; border-radius:10px; border:1px solid #d1d9e6;}
.status-box{padding:12px; border-radius:10px; text-align:center; font-weight:900; color:white; margin-top:10px;}
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

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown("### 👤 Dev: Gayan Nugawela")
    if st.button("🧹 Clear"): st.rerun()
    cur = st.selectbox("Cur", ["﷼", "රු", "฿", "د.إ", "₹", "$"])
    city = st.text_input("City", "Salalah")
    d1, d2 = st.date_input("In", date.today()), st.date_input("Out", date.today())
    m_nts = (d2 - d1).days if (d2 - d1).days > 0 else 1
    st.divider()
    otb, hst = st.slider("OTB %", 0, 100, 15), st.slider("Hist %", 0, 100, 45)
    v_mult = 1.35 if otb > hst else 0.85 if otb < (hst - 15) else 1.0
    tx = st.number_input("Tax", value=1.2327, format="%.4f")
    ota_c = st.slider("OTA %", 0, 40, 15)
    p01 = st.number_input("P01", value=6.90)
    mc = {p: st.number_input(f"{p} Cost", v) for p, v in {"BB":2.5, "LN":4.5, "DN":5.5, "SAI":8.5, "AI":10.5}.items()}

# --- 4. ENGINE ---
def run_yield(tr, adr, meals, hurdle, demand, is_ota=False):
    if tr <= 0: return None
    eff_h = hurdle + {"Compression (Peak)":15, "Standard":0, "Distressed":-5}.get(demand, 0)
    net_adr = adr / tx
    avg_m = sum(qty * mc.get(p, 0) for p, qty in meals.items()) / tr
    comm = (net_adr * (ota_c / 100)) if is_ota else 0.0
    unit_w = (net_adr - avg_m - comm) - p01
    res = "ACCEPT" if unit_w >= eff_h else "REJECT"
    clr = "#27ae60" if unit_w >= eff_h else "#e74c3c"
    return {"w": unit_w, "st": res, "cl": clr, "total": unit_w * tr * m_nts}

# --- 5. DASHBOARD ---
st.markdown("<div class='main-title'>DISPLACEMENT ANALYZER</div>", unsafe_allow_html=True)
st.markdown("<div class='main-subtitle'>Yield Equilibrium Strategic Intelligence Engine</div>", unsafe_allow_html=True)
st.success(f"📍 {city} | 📈 Velocity: {v_mult}x | 📅 Stay: {m_nts} Nights")

segs = [("1. DIRECT / FIT", "fit", 65, 40, "#3498db", False), 
        ("2. OTA CHANNELS", "ota", 60, 35, "#2ecc71", True),
        ("3. CORP GROUPS", "corp", 55, 32, "#34495e", False),
        ("4. MICE GROUPS", "mice", 50, 30, "#9b59b6", False)]

for label, k, sadr, floor, clr, ota in segs:
    st.markdown(f"<div class='card' style='border-left-color:{clr}'>{label}</div>", unsafe_allow_html=True)
    c1, c2 = st.columns([3, 1])
    with c1:
        st.markdown("<div class='pricing-row'>", unsafe_allow_html=True)
        i1, i2, i3, i4 = st.columns([1, 1, 1, 1.5])
        s, d, t = i1.number_input("SGL",0,key="s"+k), i2.number_input("DBL",0,key="d"+k), i3.number_input("TPL",0,key="t"+k)
        rate = i4.number_input(f"Rate ({cur})", value=float(sadr * v_mult), key="a"+k)
        m_row = st.columns([1.5, 1, 1, 1, 1, 1])
        dem = m_row[0].selectbox("Demand", ["Standard", "Compression (Peak)", "Distressed"], key="dm"+k)
        m_vals = {p: m_row[i+1].number_input(p, 0, key=f"{p}{k}") for i, p in enumerate(["BB", "LN", "DN", "SAI", "AI"])}
        st.markdown("</div>", unsafe_allow_html=True)
    res = run_yield(s+d+t, rate, m_vals, floor, dem, ota)
    if res:
        with c2:
            st.metric("Net Yield", f"{cur}{res['w']:,.2f}")
            st.markdown(f"<div class='status-box' style='background:{res['cl']}'>{res['st']}</div>", unsafe_allow_html=True)

st.divider()
st.caption("Developer: Gayan Nugawela | gayan01@gmail.com")
