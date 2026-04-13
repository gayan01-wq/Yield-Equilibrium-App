import streamlit as st

# --- 1. CONFIG & PREMIUM STYLING ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium")

st.markdown("""
    <style>
    .main-title { font-size: 3.5rem !important; font-weight: 900; color: #1e3799; text-align: center; text-shadow: 2px 2px 4px rgba(0,0,0,0.1); margin-bottom: 0px; }
    .sub-header { font-size: 1.2rem; text-align: center; color: #4a69bd; font-weight: 600; margin-bottom: 20px; letter-spacing: 1px; }
    .definition-box { background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 25px; border-radius: 15px; border-left: 8px solid #1e3799; margin-bottom: 30px; box-shadow: 0px 4px 15px rgba(0,0,0,0.05); }
    [data-testid="stSidebar"] { background-color: #f1f4f9; border-right: 2px solid #3498db; }
    .sidebar-name { font-size: 1.4rem; font-weight: 800; color: #1e3799; margin-bottom: 0px; }
    .sidebar-tag { color: #3498db; font-weight: 700; font-size: 0.9rem; margin-bottom: 20px; }
    .card { padding: 15px; border-radius: 12px; margin-bottom: 15px; border-left: 10px solid; font-weight: bold; background-color: #fcfcfc; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .status-box { padding: 20px; border-radius: 15px; text-align: center; font-size: 1.5rem; font-weight: bold; margin: 10px 0; border: 1px solid rgba(0,0,0,0.1); }
    .pillar-box { background-color: #ffffff; padding: 25px; border-radius: 12px; border-top: 5px solid #1e3799; min-height: 220px; box-shadow: 0px 4px 10px rgba(0,0,0,0.05); }
    </style>
""", unsafe_allow_html=True)

# --- 2. AUTHENTICATION ---
if "auth_key" not in st.session_state:
    st.session_state["auth_key"] = False

if not st.session_state["auth_key"]:
    st.markdown("<h1 class='main-title'>EQUILIBRIUM ENGINE</h1>", unsafe_allow_html=True)
    pwd = st.text_input("Access Key", type="password")
    if st.button("Unlock Dashboard"):
        if pwd == "Gayan2026":
            st.session_state["auth_key"] = True
            st.rerun()
        else: st.error("Invalid Key")
    st.stop()

# --- 3. SIDEBAR CONFIG ---
with st.sidebar:
    st.markdown("<p class='sidebar-name'>Gayan Nugawela</p>", unsafe_allow_html=True)
    st.markdown("<p class='sidebar-tag'>Strategic Revenue Architect</p>", unsafe_allow_html=True)
    st.divider()
    hotel_name = st.text_input("Property Identity", "Wyndham Garden Salalah")
    h_total = st.number_input("Total
