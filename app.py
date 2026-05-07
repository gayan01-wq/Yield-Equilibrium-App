import streamlit as st
from datetime import date

# --- 1. SETTINGS & STYLING ---
st.set_page_config(layout="wide", page_title="Universal Yield Equilibrium Engine")

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
.pillar-header { color: #1e3799; font-weight: 800; font-size: 1.1rem; text-transform: uppercase; margin-bottom: 8px; display: block; border-bottom: 2px solid #1e3799; padding-bottom: 4px;}
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
    st.markdown("### 🏨 Hotel Profile")
    h_name = st.text_input("Hotel Name", "Wyndham Garden Salalah")
    h_cap = st.number_input("Total Capacity", min_value=1, value=237)
    city_search = st.text_input("📍 Market Location", "Salalah")
    
    st.divider()
    d1 = st.date_input("Check-In", date.today())
    d2 = st.date_input("Check-Out", date(2026, 5, 12))
    m_nights = (d2 - d1).days if (d2 - d1).days > 0 else 1
    st.info(f"Stay Duration: {m_nights} Nights")

    st.divider()
    curr_map = {
        "OMR (﷼)": "﷼", "AED (د.إ)": "د.إ", "SAR (﷼)": "﷼", "QAR (﷼)": "﷼",
        "BHD (.د)": ".د", "KWD (د.ك)": "د.ك", "USD ($)": "$", "EUR (€)": "€",
        "GBP (£)": "£", "LKR (රු)": "රු", "INR (₹)": "₹", "AUD ($)": "$"
    }
    cur_sym = curr_map[st.selectbox("Select Currency", list(curr_map.keys()))]

    # Tax Divisor Logic
    tax_formula = st.text_input("Tax Divisor Formula", value="1.2327")
    try:
        current_tax_divisor = float(eval(tax_formula))
    except:
        current_tax_divisor = 1.2327

    p01_fee = st.number_input(f"P01 Fee ({cur_sym})", min_value=0.0, value=6.0)

    st.markdown("### 🍽️ Meal costs (PP)")
    m_costs = {"BF": st.number_input("BF", 0.0, 2.0), "LN": st.number_input("LN", 0.0), "DN": st.number_input("DN", 0.0), "SAI": st.number_input("SAI Add", 0.0), "AI": st.number_input("AI Add", 0.0)}

# --- 4. ENGINE LOGIC ---
def run_yield(adr, meal_qty, hurdle, demand, is_group, rooms, comm=0.0, mice=0.0, laund=0.0, trans=0.0
