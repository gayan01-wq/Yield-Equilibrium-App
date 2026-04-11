import streamlit as st

# --- BRANDING & UI ---
st.set_page_config(page_title="Yield Equilibrium Auditor", page_icon="🏨", layout="wide")
st.title("🏨 Yield Equilibrium Auditor")
st.markdown("Developed by **Gayan Nugawela** | *The Revenue Engineer Framework*")
st.divider()

# --- SIDEBAR: GLOBAL & DATA INPUTS ---
st.sidebar.header("⚙️ Global Settings")
tax_pct = st.sidebar.number_input("Tax (%)", value=0.08, step=0.01)

st.sidebar.header("📊 Segment Data")
with st.sidebar.expander("1. OTA Data"):
    ota_adr = st.number_input("OTA Gross ADR", value=195.0, key="ota_a")
with st.sidebar.expander("2. Direct Data"):
    dir_adr = st.number_input("Direct Gross ADR", value=220.0, key="dir_a")
with st.sidebar.expander("3. Corporate Data"):
    corp_adr = st.number_input("Corp Gross ADR", value=180.0, key="corp_a")
with st.sidebar.expander("4. Wholesale Data"):
    whole_adr = st.number_input("Wholesale Gross ADR", value=130.0, key="whole_a")

# --- SIDEBAR: CALIBRATION ---
st.sidebar.header("🔧 Model Calibration")
with st.sidebar.expander("Calibrate OTA"):
    ota_comm = st.number_input("OTA Comm %", value=0.18)
    ota_maint = st.number_input("OTA Maint (P01)", value=11.0)
    ota_floor = st.number_input("OTA Target Floor", value=105.0)

with st.sidebar.expander("Calibrate Direct"):
    dir_comm = st.number_input("Direct Comm %", value=0.02)
    dir_maint = st.number_input("Direct Maint (P01)", value=10.0)
    dir_floor = st.number_input("Direct Target Floor", value=100.0)

with st.sidebar.expander("Calibrate Corporate"):
    corp_comm = st.number_input("Corp Comm %", value=0.00)
    corp_maint = st.number_input("Corp Maint (P01)", value=10.0)
    corp_floor = st.number_input("Corp Target Floor", value=95.0)

with st.sidebar.expander("Calibrate Wholesale"):
    whole_comm = st.number_input("Wholesale Comm %", value=0.15)
    whole_maint = st.number_input("Wholesale Maint (P01)", value=15.0)
    whole_floor = st.number_input("Wholesale Target Floor", value=110.0)

# --- LOGIC ENGINE ---
def audit_logic(adr, comm, maint, floor):
    pre_tax = adr / (1 + tax_pct)
    net_adr = pre_tax * (1 - comm)
    adj_net = net_adr - maint
    
    if adj_net >= (floor + 10):
        return adj_net, "OPTIMIZED", "green"
    elif adj_net >= floor:
        return adj_net, "STABLE", "orange"
    else:
        return adj_net, "DILUTIVE", "red"

# --- DASHBOARD OUTPUT ---
st.subheader("Executive Verdict")
c1, c2, c3, c4 = st.columns(4)

segments = [
    (c1, "OTA", ota_adr, ota_comm, ota_maint, ota_floor),
    (c2, "Direct", dir_adr, dir_comm, dir_maint, dir_floor),
    (c3, "Corporate", corp_adr, corp_comm, corp_maint, corp_floor),
    (c4, "Wholesale", whole_adr, whole_comm, whole_maint, whole_floor)
]

for col, name, adr, comm, maint, floor in segments:
    net, status, color = audit_logic(adr, comm, maint, floor)
    with col:
        st.metric(f"{name} Adj. Net", f"${net:.2f}")
        if color == "green": st.success(status)
        elif color == "orange": st.warning(status)
        else: st.error(status)

st.divider()

# --- THE "HOW TO USE" SECTION ---
st.subheader("📖 Calibration Guide: How to Enter Data")
col_exp1, col_exp2, col_exp3 = st.columns(3)

with col_exp1:
    st.write("### 🏷️ Commission (P02)")
    st.write("""
    **What to enter:** The percentage (decimal) paid to the booking channel.
    * **OTA:** Typically **0.15 to 0.22** (15-22%) depending on your contract.
    * **Direct:** Usually **0.02** to account for credit card fees or engine costs.
    * **Corporate:** Often **0.00** if it's a net-rate contract.
    """)

with col_exp2:
    st.write("### 🧼 Maintenance (P01)")
