import streamlit as st
st.set_page_config(layout="wide", page_title="Yield Equilibrium")
st.markdown("""<style>.block-container { padding-top: 1rem !important; }.main-title { font-size: 2.5rem !important; font-weight: 900; color: #1e3799; text-align: center; margin-top: -10px; }.sub-header { font-size: 1rem; text-align: center; color: #4a69bd; font-weight: 600; margin-bottom: 15px; }.pillar-box { background: #fff; padding: 12px; border-radius: 10px; border-top: 4px solid #1e3799; text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.05); min-height: 100px; }.pillar-box h4 { color: #1e3799; font-size: 0.9rem; margin:0; }.card { padding: 12px; border-radius: 10px; margin-bottom: 10px; border-left: 10px solid; font-weight: bold; background: #fcfcfc; }.pricing-row { background: #f1f4f9; padding: 10px; border-radius: 8px; margin-top: 8px; border: 1px solid #1e3799; }.status-box { padding: 12px; border-radius: 12px; text-align: center; font-size: 1.3rem; font-weight: bold; color: white; margin-bottom: 8px; }.exposure-bar { padding: 8px; border-radius: 6px; font-weight: bold; text-align: center; color: white; margin-top: 6px; font-size: 0.85rem; }div.stButton > button:first-child[aria-label="🔄 Empty Data"] { background: #4b6584 !important; color: white !important; }[data-testid="stSidebar"] { background: #f1f4f9; border-right: 2px solid #3498db; }</style>""", unsafe_allow_html=True)
if "auth" not in st.session_state: st.session_state["auth"] = False
if not st.session_state["auth"]:
 st.markdown("<h1 class='main-title'>EQUILIBRIUM ENGINE</h1>", unsafe_allow_html=True)
 with st.form("login"):
  pwd = st.text_input("Access Key", type="password")
  if st.form_submit_button("Unlock"):
   if pwd == "Gayan2026": st.session_state["auth"] = True; st.rerun()
   else: st.error("Denied")
 st.stop()
with st.sidebar:
 st.markdown("<h2 style='color:#1e3799;'>Control Center</h2>", unsafe_allow_html=True)
 c1, c2 = st.columns(2)
 if c1.button("🔒 Sign Out"): st.session_state["auth"] = False; st.rerun()
 if c2.button("🔄 Empty Data"):
  for k in list(st.session_state.keys()):
   if any(s in k for s in ["fit","ota","corp","cgrp","tnt"]): st.session_state[k] = 1 if k.endswith("n") else 0
  st.rerun()
 st.divider(); crisis = st.toggle("🚨 ACTIVATE CRISIS MODE", value=False); st.divider()
 st.markdown("<p style='font-size:1.1rem;font-weight:800;color:#1e3799;margin:0;'>Gayan Nugawela</p><p style='font-size:0.75rem;'>Strategic Revenue Architect</p>", unsafe_allow_html=True); st.divider()
 hotel = st
