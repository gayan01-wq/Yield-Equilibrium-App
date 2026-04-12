import streamlit as st

# --- PASSWORD PROTECTION ---
def check_password():
    if "auth" not in st.session_state:
        st.session_state["auth"] = False
    if not st.session_state["auth"]:
        st.title("🏨 Yield Equilibrium Center")
        pwd = st.text_input("Enter Access Key", type="password", placeholder="Type key and hit Enter")
        if st.button("Unlock Dashboard") or (pwd > ""):
            if pwd == "Gayan2026": 
                st.session_state["auth"] = True
                st.rerun()
            elif pwd > "":
                st.error("Unauthorized Key.")
        return False
    return True

if check_password():
    st.set_page_config(layout="wide", page_title="Yield Equilibrium")
    st.markdown("""<style>
        .stMetric{background:#fff;border:1px solid #eee;padding:10px;border-radius:10px}
        .card{padding:8px;border-radius:8px;margin-bottom:5px;border-left:8px solid;font-weight:bold}
        .w-bar-bg {background-color: #e0e0e0; border-radius: 10px; width: 100%; height: 12px; margin: 8px 0;}
        .w-bar-fill {height: 12px; border-radius: 10px; transition: width 0.5s;}
    </style>""", unsafe_allow_html=True)
    st.title("🏨 Yield Equilibrium Center")
    
    with st.sidebar:
        st.title("⚙️ Control Panel")
        h_nm = st.text_input("Hotel Name", "Wyndham Garden Salalah")
        h_cp = st.number_input("Total Inventory", 1, 1000, 158)
        st.header("🍽️ Meal Allocation")
        b, l, d = st.number_input("BB", 0., 500., 2.), st.number_input("LN", 0., 500., 6.), st.number_input("DN", 0., 500., 6.)
        s, a = st.number_input("SAI", 0., 500., 8.), st.number_input("AI", 0., 500., 15.)
        m = {"RO": 0, "BB": b, "HB": b+d, "FB": b+l+d, "SAI": b+l+d+s, "AI": b+l+d+s+a}
        st.header("⚙️ Global Settings")
        p01 = st.number_input("P01 Fee (Maint)", 0., 100., 6.9)
        tx = st.number_input("Tax Div", 1., 2., 1.2327, format="%.4f")
        op = st.slider("OTA Comm %", 0, 50, 18) / 100
        cu = st.selectbox("Currency", ["OMR", "AED", "SAR", "THB", "EUR", "GBP", "USD"])

    def run(rms, adr, nts, mix, cp, fl, ev_rev=0, total_tr_cost=0):
        t_rms = sum(rms)
        if t_rms <= 0: return None
        pax = (rms[0]*1 + rms[1]*2 + rms[2]*3)
        nt_rev = (adr * t_rms) / tx
        fb_cost = sum(q * m[p] * (pax / t_rms) for p, q in mix.items())
        ev_w = (ev_rev * pax) / tx
        cm = (nt_rev - fb_cost) * cp
        dp = ((nt_rev - fb_cost - cm) - (p01 * t_rms)) + (ev_w / t_rms)
        tp = (dp * t_rms * n
