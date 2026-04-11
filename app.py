import streamlit as st

# --- BRANDING & UI ---
st.set_page_config(page_title="Yield Equilibrium Auditor", page_icon="🏨", layout="wide")
st.title("🏨 Yield Equilibrium Auditor")
st.markdown("Developed by **Gayan Nugawela** | *The Revenue Engineer Framework*")
st.divider()

# --- SIDEBAR: SEGMENT INPUTS ---
st.sidebar.header("⚙️ Global Settings")
tax_pct = st.sidebar.number_input("Tax (%)", value=0.08, step=0.01)

st.sidebar.header("📊 Segment Data")

with st.sidebar.expander("1. OTA", expanded=True):
    ota_adr = st.number_input("OTA Gross ADR", value=195.0, key="ota_a")
    ota_nights = st.number_input("OTA Nights", value=600, key="ota_n")

with st.sidebar.expander("2. Direct"):
    dir_adr = st.number_input("Direct Gross ADR", value=220.0, key="dir_a")
    dir_nights = st.number_input("Direct Nights", value=450, key="dir_n")

with st.sidebar.expander("3. Corporate"):
    corp_adr = st.number_input("Corp Gross ADR", value=180.0, key="corp_a")
    corp_nights = st.number_input("Corp Nights", value=300, key="corp_n")

with st.sidebar.expander("4. Wholesale"):
    whole_adr = st.number_input("Wholesale Gross ADR", value=130.0, key="whole_a")
    whole_nights = st.number_input("Wholesale Nights", value=150, key="whole_n")

# --- THE HIDDEN ENGINE (P01 & P02 Logic) ---
rules = {
    'OTA':       {'comm': 0.18, 'maint': 11.0, 'floor': 105.0}, 
    'Direct':    {'comm': 0.02, 'maint': 10.0, 'floor': 100.0},
    'Corporate': {'comm': 0.00, 'maint': 10.0, 'floor': 95.0},
    'Wholesale': {'comm': 0.15, 'maint': 15.0, 'floor': 110.0}
}

def audit_logic(seg, adr):
    pre_tax = adr / (1 + tax_pct)
    net_adr = pre_tax * (1 - rules[seg]['comm'])
    adj_net = net_adr - rules[seg]['maint']
    is_pass = adj_net >= rules[seg]['floor']
    return adj_net, is_pass

# --- DASHBOARD OUTPUT ---
st.subheader("Executive Verdict")
cols = st.columns(4) 

segments = {
    'OTA': ota_adr,
    'Direct': dir_adr,
    'Corporate': corp_adr,
    'Wholesale': whole_adr
}

for i, (name, adr_val) in enumerate(segments.items()):
    net, passed = audit_logic(name, adr_val)
    with cols[i]:
        st.metric(f"{name} Adj. Net", f"${net:.2f}")
        if passed: 
            st.success("OPTIMIZED")
        else: 
            st.error("DILUTIVE")

st.divider()

# --- THE DEFINITION SECTION ---
st.subheader("💡 Strategy Guide")
col_a, col_b = st.columns(2)

with col_a:
    st.write("### 🟢 OPTIMIZED")
    st.write("""
    **Asset Health:** This segment is a 'Wealth Builder.' 
    It covers Tax, P02 (Acquisition), and P01 (Maintenance) while leaving a profit 
    that exceeds the sustainability floor. **Action: Target for Growth.**
    """)

with col_b:
    st.write("### 🔴 DILUTIVE")
    st.write("""
    **Asset Erosion:** This segment is a 'Wealth Destroyer.' 
    The net revenue is too low to cover the long-term wear and tear of the room. 
    You are losing asset value to gain occupancy. **Action: Surgical Rate Increase.**
    """)

st.info("The Yield Equilibrium ensures that the hotel isn't just 'busy,' but actually 'profitable' enough to sustain its quality.")
