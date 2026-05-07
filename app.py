import streamlit as st
from datetime import date

# --- 1. SETTINGS & STYLING ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium")

st.markdown("""<style>
.block-container{padding-top:1rem!important; padding-bottom:0rem!important;}
.main-title { font-size: 2.2rem!important; font-weight: 900; color: #1e3799; text-align: center; text-transform: uppercase; margin-bottom: -5px; }
.card{padding:10px; border-radius:10px; margin-bottom:5px; border-left:10px solid; background:#ffffff; box-shadow: 0 2px 4px rgba(0,0,0,0.05)}
.pricing-row{background:#f8faff; padding:15px; border-radius:12px; border:1px solid #d1d9e6; margin-top:2px;}
.google-window{background:#e8f0fe; padding:15px; border-radius:12px; border:2px solid #4285f4; margin-bottom:15px; font-size:0.88rem; line-height:1.5;}
.status-indicator{padding:12px; border-radius:8px; text-align:center; font-weight:900; font-size:1.1rem; color:white; margin-top:10px; display:block;}
.reason-box{background:#fff9c4; border:1px solid #fbc02d; padding:10px; border-radius:8px; margin-top:8px; text-align:left; font-weight:500; color:#5f4300; font-size:0.8rem;}
.noi-badge{background:#1e3799; color:white; padding:8px 12px; border-radius:8px; font-weight:700; font-size:1rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1);}
.theory-box { background-color: #f1f4f9; padding: 25px; border-radius: 15px; border: 1px solid #d1d9e6; margin-top: 35px; }
.pillar-header { color: #1e3799; font-weight: 800; font-size: 1rem; text-transform: uppercase; margin-bottom: 5px; display: block; }
</style>""", unsafe_allow_html=True)

# --- 2. AUTHENTICATION ---
if "auth" not in st.session_state: st.session_state["auth"] = False
if not st.session_state["auth"]:
    st.markdown("<h1 class='main-title'>EQUILIBRIUM ENGINE</h1>", unsafe_allow_html=True)
    with st.form("login"):
        if st.text_input("Access Key", type="password") == "Gayan2026":
            if st.form_submit_button("Unlock"):
                st.session_state["auth"] = True
                st.rerun()
    st.stop()

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown("### 🏨 Property Profile")
    h_name = st.text_input("Hotel Name", "Wyndham Garden Salalah")
    h_cap = st.number_input("Total Capacity", min_value=1, value=237)
    city_search = st.text_input("📍 Market Location", "Salalah")
    
    st.divider()
    d1 = st.date_input("Check-In", date.today())
    d2 = st.date_input("Check-Out", date(2026, 5, 8))
    m_nights = (d2 - d1).days if (d2 - d1).days > 0 else 1
    st.info(f"Stay Duration: {m_nights} Nights")

    st.divider()
    cur_sym = st.selectbox("Currency", ["OMR", "AED", "SAR", "USD"])
    tx_div = st.number_input("Tax Divisor", value=1.2327, format="%.4f")
    p01_fee = st.number_input("P01 Fee", value=6.00)

    st.markdown("### 🍽️ Meal costs (PP)")
    m_costs = {
        "BF": st.number_input("Breakfast", value=2.0),
        "LN": st.number_input("Lunch", value=0.0),
        "DN": st.number_input("Dinner", value=0.0),
        "SAI": st.number_input("SAI", value=0.0),
        "AI": st.number_input("AI", value=0.0)
    }

# --- 4. ENGINE LOGIC ---
def run_yield(adr, meal_qty, hurdle, demand, is_group, rooms, mice=0.0, laund=0.0, trans=0.0):
    v_mult = {"Compression (Peak)": 1.25, "High Flow": 1.10, "Standard": 1.0, "Distressed": 0.85}.get(demand, 1.0)
    
    # Basis Logic
    bf, ln, dn, sai, ai = meal_qty.get("BF",0), meal_qty.get("LN",0), meal_qty.get("DN",0), meal_qty.get("SAI",0), meal_qty.get("AI",0)
    if ai > 0: mp = "AI"
    elif sai > 0: mp = "SAI"
    elif bf > 0 and ln > 0 and dn > 0: mp = "FB"
    elif bf > 0 and dn > 0: mp = "HB"
    elif bf > 0: mp = "BB"
    else: mp = "RO"

    net_adr = (adr * v_mult) / tx_div
    meal_tot = sum(qty * m_costs.get(p, 0) for p, qty in meal_qty.items())
    
    div = max(rooms, 10) if is_group else max(rooms, 1)
    grp_rev = (mice / tx_div) + ((trans / tx_div) / div) if is_group else 0
    unit_w = (net_adr + grp_rev - meal_tot) - p01_fee - laund
    
    dyn_h = hurdle * {"Compression (Peak)": 2.5, "High Flow": 1.5, "Standard": 1.0, "Distressed": 0.7}.get(demand, 1.0)
    
    stt = "ACCEPT: OPTIMIZED" if unit_w >= dyn_h else "REJECT: DILUTIVE"
    clr = "#27ae60" if unit_w >= dyn_h else "#e74c3c"
    
    return {"w": unit_w, "st": stt,
