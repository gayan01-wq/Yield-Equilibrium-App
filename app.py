import streamlit as st
from datetime import date

# --- 1. SETTINGS ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium")

st.markdown("""<style>
.block-container{padding-top:1rem!important;}
.main-title { font-size: 2rem!important; font-weight: 900; color: #1e3799; text-align: center; text-transform: uppercase; }
.card{padding:10px; border-radius:10px; margin-bottom:5px; border-left:10px solid; background:#fff; box-shadow: 0 2px 4px rgba(0,0,0,0.05)}
.pricing-row{background:#f8faff; padding:15px; border-radius:12px; border:1px solid #d1d9e6;}
.google-window{background:#e8f0fe; padding:15px; border-radius:12px; border:2px solid #4285f4; margin-bottom:15px;}
.status-indicator{padding:12px; border-radius:8px; text-align:center; font-weight:900; color:white; display:block;}
.noi-badge{background:#1e3799; color:white; padding:8px 12px; border-radius:8px; font-weight:700;}
.theory-box { background-color: #f1f4f9; padding: 20px; border-radius: 15px; border: 1px solid #d1d9e6; margin-top: 20px; }
.pillar-header { color: #1e3799; font-weight: 800; text-transform: uppercase; border-bottom: 2px solid #1e3799;}
</style>""", unsafe_allow_html=True)

# --- 2. AUTH ---
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
    st.markdown("### 🏨 Profile")
    h_name = st.text_input("Hotel Name", "Wyndham Garden Salalah")
    h_cap = st.number_input("Total Capacity", min_value=1, value=237)
    city = st.text_input("Location", "Salalah")
    st.divider()
    d1, d2 = st.date_input("In", date.today()), st.date_input("Out", date(2026,5,12))
    m_nights = (d2 - d1).days if (d2 - d1).days > 0 else 1
    st.info(f"Stay: {m_nights} Nights")
    st.divider()
    curr = {"OMR":"﷼", "AED":"د.إ", "SAR":"﷼", "USD":"$", "EUR":"€"}
    cur_sym = curr[st.selectbox("Currency", list(curr.keys()))]
    tax_in = st.text_input("Tax Divisor Formula", value="1.2327")
    try: tx_div = float(eval(tax_in))
    except: tx_div = 1.2327
    p01 = st.number_input("P01 Fee", value=6.0)
    st.markdown("### 🍽️ Meal Costs")
    mc = {"BF":st.number_input("BF",value=2.0),"LN":st.number_input("LN",0.0),
          "DN":st.number_input("DN",0.0),"SAI":st.number_input("SAI",0.0),"AI":st.number_input("AI",0.0)}

# --- 4. ENGINE ---
def run_yield(adr, mq, hrd, dem, grp, rms, ota_c=0.0, mice=0.0, lnd=0.0, trn=0.0):
    vm = {"Compression": 1.25, "High Flow": 1.15, "Standard": 1.0, "Distressed": 0.85}.get(dem, 1.0)
    # Basis Logic
    b, l, d, s, a = mq.get("BF",0), mq.get("LN",0), mq.get("DN",0), mq.get("SAI",0), mq.get("AI",0)
    if a > 0: mp = "AI"
    elif s > 0: mp = "SAI"
    elif b > 0 and l > 0 and d > 0: mp = "FB"
    elif b > 0 and d > 0: mp = "HB"
    elif b > 0: mp = "BB"
    else: mp = "RO"
    
    net = (adr * vm) / tx_div
    comm = net * (ota_c / 100)
    meals = sum(q * mc.get(k, 0) for k, q in mq.items())
    div = max(rms, 10) if grp else max(rms, 1)
    g_rev = (mice / tx_div) + ((trn / tx_div) / div) if grp else 0
    uw = (net + g_rev - meals - comm) - p01 - lnd
    dh = hrd * {"Compression": 2.5, "High Flow": 1.7, "Standard": 1.0, "Distressed": 0.65}.get(dem, 1.0)
    return {"w":uw, "st":"ACCEPT" if uw >= dh else "REJECT", "cl":"#27ae60" if uw >= dh else "#e74c3c", "mp":mp, "dh":dh, "vm":vm, "noi":uw*div*m_nights}

# --- 5. MAIN ---
st.markdown(f"<h1 class='main-title'>{h_name.upper()}</h1>", unsafe_allow_html=True)
intel = {"salalah":{"ev":"Khareef","dm":"Compression"},"muscat":{"ev":"MICE","dm":"High Flow"}}
act_intel = intel.get(city.lower(), {"ev":"Standard","dm":"Standard"})
st.markdown(f"<div class='google-window'>🌐 <b>{city} Intel:</b> {act_intel['ev']} | Logic: {act_intel['dm']}</div>", unsafe_allow_html=True)

segs = [{"n":"1. FIT", "k":"fit", "c":"#3498db", "h":45.0, "g":False, "o":False},
        {"n":"2. OTA", "k":"ota", "c":"#2ecc71", "h":35.0, "g":False, "o":True},
        {"n":"3. MICE", "k":"mice", "c":"#34495e", "h":32.0, "g":True, "o":False},
        {"n":"4. GROUP", "k":"tnt", "c":"#e67e22", "h":12.0, "g":
