import streamlit as st
import pandas as pd

# --- BRANDING & UI ---
st.set_page_config(page_title="Yield Equilibrium Auditor", page_icon="🏨")
st.title("🏨 Yield Equilibrium Auditor")
st.markdown("Developed by **Gayan Nugawela** | *The Revenue Engineer Framework*")
st.divider()

# --- SIDEBAR: WHERE YOU ENTER DATA ---
st.sidebar.header("⚙️ Global Settings")
tax_pct = st.sidebar.number_input("Tax (%)", value=0.08, step=0.01)

st.sidebar.header("📊 Segment Performance")
ota_adr = st.sidebar.number_input("OTA Gross ADR", value=195.0)
ota_nights = st.sidebar.number_input("OTA Nights", value=600)

dir_adr = st.sidebar.number_input("Direct Gross ADR", value=220.0)
dir_nights = st.sidebar.number_input("Direct Nights", value=450)

# --- THE HIDDEN ENGINE (Your Secret Sauce) ---
rules = {
    'OTA':    {'comm': 0.18, 'maint': 11.0, 'floor': 105.0}, 
    'Direct': {'comm': 0.02, 'maint': 10.0, 'floor': 100.0}
}

def audit_logic(seg, adr, nights):
    pre_tax = adr / (1 + tax_pct)
    net_adr = pre_tax * (1 - rules[seg]['comm'])
    adj_net = net_adr - rules[seg]['maint']
    is_pass = adj_net >= rules[seg]['floor']
    return adj_net, is_pass

ota_net, ota_pass = audit_logic('OTA', ota_adr, ota_nights)
dir_net, dir_pass = audit_logic('Direct', dir_adr, dir_nights)

# --- DASHBOARD OUTPUT ---
st.subheader("Executive Verdict")
col1, col2 = st.columns(2)

with col1:
    st.metric("OTA Adjusted Net", f"${ota_net:.2f}")
    if ota_pass: st.success("🟢 OPTIMIZED")
    else: st.error("🔴 DILUTIVE")

with col2:
    st.metric("Direct Adjusted Net", f"${dir_net:.2f}")
    if dir_pass: st.success("🟢 OPTIMIZED")
    else: st.error("🔴 DILUTIVE")

st.divider()
st.info("The **Yield Equilibrium** model ensures every booking clears the filters of Tax, P02 (Acquisition), and P01 (Asset Maintenance).")
