import streamlit as st

# --- 1. STYLE ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium")
st.markdown("""
<style>
    .block-container { padding-top: 1rem !important; }
    .main-title { font-size: 2.8rem !important; font-weight: 900; color: #1e3799; text-align: center; margin-top: -10px; }
    .sub-header { font-size: 1rem; text-align: center; color: #4a69bd; font-weight: 600; margin-bottom: 15px; }
    .pillar-box { background-color: #fff; padding: 12px; border-radius: 10px; border-top: 4px solid #1e3799; text-align: center; box-shadow: 0px 4px 10px rgba(0,0,0,0.05); min-height: 100px; }
    .card { padding: 12px; border-radius: 10px; margin-bottom: 10px; border-left: 10px solid; font-weight: bold; background-color: #fcfcfc; }
    .pricing-row { background-color: #f1f4f9; padding: 10px; border-radius: 8px; margin-top: 8px; border: 1px dashed #1e3799; }
    .status-box { padding: 12px; border-radius: 12px; text-align: center; font-size: 1.3rem; font-weight: bold; color: white; margin-bottom: 8px; }
    .exposure-bar { padding: 8px; border-radius: 6px; font-weight: bold; text-align: center; color: white; margin-top: 6px; font-size: 0.85rem; }
    div.stButton > button:first-child[aria-label="🔄 Empty Data"] { background-color: #4b6584 !important; color: white !important; }
    [data-testid="stSidebar"] { background-color: #f1f4f9; border-right: 2px solid #3498db; }
</style>
""", unsafe_allow_html=True)

# --- 2. AUTH ---
if "auth" not in st.session_state: st.session_state["auth"] = False
if not st.session_state["auth"]:
    st.markdown("<h1 class='main-title'>EQUILIBRIUM ENGINE</h1>", unsafe_allow_html=True)
    with st.form("login"):
        pwd = st.text_input("Access Key", type="password")
        if st.form_submit_button("Unlock"):
            if pwd == "Gayan2026": st.session_state["auth"] = True; st.rerun
