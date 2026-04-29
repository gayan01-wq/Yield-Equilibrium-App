import streamlit as st
from datetime import date

# --- STYLING ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium Master Engine")

st.markdown("""<style>
.block-container{padding-top:1rem!important}
.main-title{font-size:2.5rem!important;font-weight:900;color:#1e3799;text-align:center;margin-top:-10px}
.sub-header{font-size:1rem;text-align:center;color:#4a69bd;font-weight:600;margin-bottom:15px}
.card{padding:12px;border-radius:10px;margin-bottom:10px;border-left:10px solid;font-weight:bold;background:#fcfcfc}
.pricing-row{background:#f1f4f9;padding:10px;border-radius:8px;margin-top:8px;border:1px solid #1e3799}
.pricing-header{background:#1e3799;color:white;padding:3px 10px;border-radius:5px 5px 0 0;font-size:0.8rem;font-weight:bold;margin-bottom:5px}
.status-box{padding:12px;border-radius:12px;text-align:center;font-size:1.3rem;font-weight:bold;color:white;margin-bottom:8px}
.exposure-bar{padding:8px;border-radius:6px;font-weight:bold;text-align:center;color:#1e3799;background:#ffc107;margin-top:6px;font-size:0.85rem}
.sentinel-box{background:#1e3799; color:white; padding:20px; border-radius:10px; margin-bottom:20px; border-left:10px solid #ffc107;}
[data-testid="stSidebar"]{background:#f1f4f9;border-right:2px solid #3498db}
</style>""", unsafe_allow_html=True)

# --- AUTH ---
if "auth" not in st.session_state: st.session_state["auth"] = False
if not st.session_state["auth"]:
    st.markdown("<h1 class='main-title'>EQUILIBRIUM ENGINE</h1>", unsafe_allow_html=True)
    with st.form("login"):
        pwd = st.text_input("Access Key", type="password")
        if st.form_submit_button("Unlock"):
            if pwd == "Gayan2026": st.session_state["auth"] = True; st.rerun()
            else: st.error("Denied")
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<p style='font-size:1.2rem;font-weight:800;color:#1e3799;margin:0;'>Gayan Nugawela</p><p style='font-size:0.8rem;margin:0;'>Strategic Revenue Architect</p>", unsafe_allow_html=True); st.divider()
    if st.button("🔒 Sign Out"): st.session_state["auth"] = False; st.rerun()
    hotel = st.text_input("📍 Targeted Property", "Wyndham Garden Salalah")
    h_tot = st.number_input("Inventory", 1, 5000, 237)
    
    st.write("### 🌐 Deep Market Scrape")
    # This is the "Truth" toggle for your dull market/crisis
    market_state = st.radio("Current Market Condition", ["Global/Local Crisis", "Stagnant", "Recovering", "Peak Season"])
    m_logic = {"Global/Local Crisis": 0.65, "Stagnant": 0.85, "Recovering": 1.0, "Peak Season": 1.35}
    m_heat = m_logic[market_state]
    
    st.write("### 📅 Stay Intelligence")
    today = date.today()
    d1 = st.date_input("Check-In", today)
    d2 = st.date_input("Check-Out", today)
    stay_n = (d2 - d1).days if (d2 - d1).days > 0 else 1
    
    st.write("### 📈 Velocity Valve (P03)")
    otb_occ = st.slider("Current OTB %", 0, 100, 15) # Set low for crisis
    hist_occ = st.slider("Historical Avg %", 0, 100, 45)
    v_delta = otb_occ - hist_occ
    v_mult = 1.25 if v_delta > 10 else 1.10 if v_delta > 0 else 0.85 if v_delta > -10 else 0.70

    st.divider()
    cu = st.selectbox("Currency", ["OMR","AED","SAR","USD"])
    tx = st.number_input("Tax Divisor", 1.2327, format="%.4f")
    ota_p = st.slider("OTA Commission %", 0, 50, 18) / 100
    
    st.write("### 🍽️ Meal Costs")
    m_costs = {"RO": 0.0, "BB": st.number_input("BB", 0.0), "HB": st.number_input("HB", 0.0), 
               "FB": st.number_input("FB", 0.0), "SAI": st.number_input("SAI", 5.0), "AI": st.number_input("AI", 5.0)}

# --- CALCULATIONS ---
def calc_w(rms, adr, n, meals, comm, fl, mice=0.0, trans=0.0):
    tot_r = sum(rms)
    if tot_r <= 0: return None
    px_r = (rms[0]*1 + rms[1]*2 + rms[2]*3) / tot_r
    u_n = adr / tx
    m_c = sum((qty/tot_r) * m_costs[p] * px_r for p, qty in meals.items() if qty > 0)
    unit_w = (u_n - m_c - ((u_n - m_c) * comm)) + ((mice * px_r) / (n * tx))
    total_w = (unit_w * tot_r * n) + (trans / tx)
    d_u = total_w / (tot_r * n)
    
    hrd = fl * 1.25 if (tot_r / h_tot) >= 0.2 else fl
    if d_u < (hrd * 0.95): l, b, msg = ("DILUTIVE", "#e74c3c", "CRISIS ALERT: Rate below survival floor.")
    elif d_u < hrd: l, b, msg = ("MARGINAL", "#ff9800", "VOLUME PLAY: Accept for cashflow only.")
    else: l, b, msg = ("OPTIMIZED", "#27ae60", "EQUILIBRIUM: Bankable wealth secured.")
    return {"u": d_u, "l": l, "b": b, "tot": total_w, "rn": tot_r * n, "msg": msg}

# --- MAIN ---
st.markdown("<h1 class='main-title'>YIELD EQUILIBRIUM MASTER</h1>", unsafe_allow_html=True)

# SENTINEL OUTPUT
st.markdown(f"""<div class='sentinel-box'>
    <h3 style='margin:0; color:#ffc107;'>🤖 PILLAR 02: MARKET SENTINEL ANALYSIS</h3>
    <p style='margin:5px 0;'>Peer Review for <b>{hotel}</b>: <b style='color:#ffc107;'>{market_state.upper()}</b></p>
    <div style='display:flex; justify-content:space-between;'>
        <span><b>Market Strength Index:</b> {m_heat}x</span>
        <span><b>Booking Velocity:</b> {v_delta}%</span>
        <span><b>Pillar 03 Multiplier:</b> {v_mult}x</span>
    </div>
</div>""", unsafe_allow_html=True)

def draw_s(title, key, d_adr, d_fl, color, is_o=False, is_g=False):
    st.markdown(f"<div class='card' style='border-left-color:{color}'>{title}</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.8, 1.2])
    # The Genius Formula: Corrected for Crisis
    suggested_rate = (d_adr * m_heat) * v_mult
    with c1:
        s, d, t = st.number_input("SGL",0,key=key+"s"), st.number_input("DBL",0,key=key+"d"), st.number_input("TPL",0,key=key+"t")
        n = st.number_input("Nights", value=stay_n, key=key+"n")
    with c2:
        mc = st.columns(3)
        mx = {"RO": mc[0].number_input("RO",0,key=key+"ro"), "BB": mc[0].number_input("BB",0,key=key+"bb"),
              "HB": mc[1].number_input("HB",0,key=key+"hb"), "FB": mc[1].number_input("FB",0,key=key+"fb"),
              "SAI": mc[2].number_input("SAI",0,key=key+"sai"), "AI": mc[2].number_input("AI",0,key=key+"ai")}
        st.markdown(f"<div class='pricing-row'><div class='pricing-header'>SUGGESTED EQUILIBRIUM: {cu} {suggested_rate:,.2f}</div>", unsafe_allow_html=True)
        adr_v = st.number_input("Applied ADR", value=float(suggested_rate), key=key+"a")
        fl_v = st.number_input("Floor", value=float(d_fl), key=key+"f")
        mi, tr = 0.0, 0.0
        if is_g:
            gc1, gc2 = st.columns(2)
            mi, tr = gc1.number_input("MICE(Pax)", 0.0, key=key+"ev"), gc2.number_input("Trans(Total)", 0.0, key=key+"tr")
        st.markdown("</div>", unsafe_allow_html=True)
    res = calc_w([s, d, t], adr_v, n, mx, (ota_p if is_o else 0.0), fl_v, mi, tr)
    if res:
        with c3:
            st.metric("Net Wealth", f"{cu} {res['u']:,.2f}"); st.markdown(f"<div class='status-box' style='background:{res['b']}'>{res['l']}</div>", unsafe_allow_html=True)
            st.caption(res['msg']); st.markdown(f"<div class='exposure-bar'>{res['rn']} RNs | Total: {res['tot']:,.0f}</div>", unsafe_allow_html=True)
            st.session_state[key+"_t"] = res['tot']
    st.divider()

draw_s("1. Direct / FIT", "fit", 65, 40, "#3498db")
draw_s("2. OTA Channels", "ota", 60, 35, "#2ecc71", True)
draw_s("3. Corporate / Gov", "corp", 55, 38, "#34495e")
draw_s("4. Corporate Groups", "cgrp", 50, 30, "#9b59b6", False, True)
draw_s("5. Group Tour & Travel", "tnt", 45, 25, "#e67e22", False, True)

tw = sum(st.session_state.get(k+"_t", 0) for k in ["fit","ota","corp","cgrp","tnt"])
st.markdown(f"<div style='background:#1e3799;padding:20px;border-radius:12px;text-align:center;color:white;'><h3>Portfolio Yield Total: {cu} {tw:,.2f}</h3></div>", unsafe_allow_html=True)
