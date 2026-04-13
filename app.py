import streamlit as st
import pandas as pd

# --- 1. CONFIG & THEME ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .main-title { font-size: 3rem !important; font-weight: 800; color: #2c3e50; text-align: center; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 2px; border-bottom: 5px solid #3498db; padding-bottom: 5px; }
    .framework-subtitle { text-align: center; color: #7f8c8d; font-style: italic; font-size: 1.1rem; margin-bottom: 30px; }
    [data-testid="stMetricValue"] { font-size: 1.8rem !important; }
    .stMetric {background:#fff; border:1px solid #eee; padding:15px; border-radius:12px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);}
    .card {padding:12px; border-radius:10px; margin-bottom:10px; border-left:12px solid; font-weight:bold; color: #2c3e50;}
    .dominance-warn {color: #d35400; font-weight: bold; border: 2px solid #d35400; padding: 8px; border-radius: 5px; text-align: center; background: #fff5f0;}
    .pillar-box {background:#f8f9fa; padding:15px; border-radius:10px; border-top:4px solid #2c3e50; min-height: 180px; margin-bottom: 20px;}
    .coach-note {padding: 12px; border-radius: 8px; font-size: 0.95rem; margin-top: 10px; border: 2px solid #eee; background-color: #fdfefe; line-height: 1.4;}
    .copyright-text {font-size: 0.75rem; color: #95a5a6; text-align: center; margin-top: 50px;}
    /* Ensure Tax Divisor is fully visible */
    .stNumberInput input { font-size: 1.1rem !important; font-weight: bold !important; }
    </style>
""", unsafe_allow_html=True)

# --- 2. PASSWORD PROTECTION ---
def check_password():
    if "auth" not in st.session_state:
        st.session_state["auth"] = False
    if not st.session_state["auth"]:
        st.markdown("<h1 class='main-title'>Yield Equilibrium</h1>", unsafe_allow_html=True)
        pwd = st.text_input("Access Key", type="password")
        if st.button("Unlock") or (pwd == "Gayan2026"): 
            if pwd == "Gayan2026":
                st.session_state["auth"] = True
                st.rerun()
            elif pwd != "": st.error("Invalid Key")
        return False
    return True

if check_password():
    # --- 3. SIDEBAR CONTROLS ---
    with st.sidebar:
        st.title("👨‍💼 Architect")
        st.subheader("Gayan Nugawela")
        st.caption("Revenue management specialist- SME")
        st.divider()
        st.header("⚙️ Global Architecture")
        h_nm = st.text_input("Hotel Name", "Wyndham Garden Salalah")
        h_cp = st.number_input("Total Inventory", 1, 1000, 158)
        
        currencies = ["OMR", "AED", "SAR", "QAR", "BHD", "KWD", "JOD", "EGP", "EUR", "GBP", "USD", "LKR", "INR", "JPY", "CNY", "SGD", "THB"]
        cu = st
