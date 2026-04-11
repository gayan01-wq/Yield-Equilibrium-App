import streamlit as st

# --- BRANDING ---
st.set_page_config(page_title="Yield Equilibrium Auditor", page_icon="🏨", layout="wide")
st.title("🏨 Yield Equilibrium Auditor")
st.markdown("Developed by **Gayan Nugawela** | *The Revenue Engineer Framework*")
st.divider()

# --- SIDEBAR: GLOBAL SETTINGS ---
st.sidebar.header("🏨 Property Identity")
hotel_name = st.sidebar.text_input("Property Name", value="Wyndham Garden Salalah Mirbat")

st.sidebar.header("⚙️ Global Settings")
currency_list = ["$ (USD)", "€ (EUR)", "£ (GBP)", "OMR (OMR)", "THB (THB)", "AED (AED)", "SAR (SAR)", "SGD (SGD)"]
currency_display = st.sidebar.selectbox("Select Currency", currency_list)
currency_symbol = currency_display.split(" ")[0]
tax_div = st.sidebar.number_input("Tax Formula (Divisor)", value=1.2327, format="%.4f")

def get_input(label, adr_def, comm_def, maint_def, floor_def, rooms_def=1):
    with st.sidebar.expander(f"📊 {label} Settings"):
        r = st.number_input(f"{label} No. of Rooms", value=rooms_def, step=1)
        a = st.number_input(f"{label} Gross ADR", value=adr_def)
        c = st.number_input(f"{label} Comm % (P02)", value=comm_def)
        m = st.number_input(f"{label} Maint (P01)", value=maint_def)
        f = st.number_input(f"{label} Profit Floor", value=floor_def)
    return r, a, c, m, f

# --- DATA ---
st.sidebar.subheader("Individual Segments")
ota = get_input("OTA", 195.0, 0.18, 11.0, 105.0)
drct = get_input("Direct", 220.0, 0.02, 10.0, 100.0)
corp = get_input("Corporate", 180.0, 0.0, 10.0, 95.0)
whls = get_input("Wholesale", 130.0, 0.15, 15.0, 110.0)

st.sidebar.subheader("Group Segments")
grp_corp = get_input("Corp Group", 160.0, 0.0, 10.0, 90.0, 20)
grp_tour = get_input("Tour/Travel", 120.0, 0.10, 12.0, 85.0, 30)
grp_mice = get_input("MICE Group", 175.0, 0.05, 18.0, 100.0, 50)

# --- ENGINE ---
def audit(rooms, adr, comm, maint, floor):
    # Surgical Math: Strip Tax -> Deduct Commission -> Deduct Maintenance
    net_unit = (adr / tax_div) * (1 - comm) - maint
    total_net = net_unit * rooms
    if net_unit >= (floor + 10): return net_unit, total_net, "OPTIMIZED", "green"
    elif net_unit >= floor: return net_unit, total_net, "STABLE", "orange"
    else: return net_unit, total_net, "DILUTIVE", "red"

# --- DISPLAY ---
st.markdown(f"<h1 style='text-align: center; color: #1E3A8A;'>{hotel_name}</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-style: italic;'>Surgical Revenue Audit Dashboard</p>", unsafe_allow_html=True)

# Row 1: Individuals
st.subheader("Individual Segment Health")
cols1 = st.columns(4)
for i, (name, data) in enumerate({"OTA":ota, "Direct":drct, "Corporate":corp, "Wholesale":whls}.items()):
    unit, total, stat, colr = audit(*data)
    with cols1[i]:
        st.metric(f"{name} Net ADR", f"{currency_symbol} {unit:.2f}")
        if colr == "green": st.success(f"🟢 {stat}")
        elif colr == "orange": st.warning(f"🟡 {stat}")
        else: st.error(f"🔴 {stat}")

# Row 2: Groups
st.divider()
st.subheader("Group Volume Impact")
cols2 = st.columns(3)
for i, (name, data) in enumerate({"Corp Group":grp_corp, "Tour & Travel":grp_tour, "MICE":grp_mice}.items()):
    unit, total, stat, colr = audit(*data)
    with cols2[i]:
        st.metric(f"{name} Total Net", f"{currency_symbol} {total:,.2f}")
        st.caption(f"Per Room Net: {currency_symbol} {unit:.2f}")
        if colr == "green": st.success(f"🟢 {stat}")
        elif colr == "orange": st.warning(f"🟡 {stat}")
        else: st.error(f"🔴 {stat}")

st.divider()

# --- THE SURGICAL PILLARS ---
st.subheader("🛡️ The Three Pillars of Yield Equilibrium")
s1, s2, s3 = st.columns(3)

with s1:
    st.write("### 🏗️ P01: Asset Protection")
    st.info("""
    **The Cost of Wear:** Maintenance is the price to 'reset' the asset. 
    By accounting for labor and linen costs, you ensure the hotel is 
    compensated for every physical interaction with the building.
    """)

with s2:
    st.write("### 📉 P02: Channel Efficiency")
    st.info("""
    **The Price of Visibility:** Commission is the fee paid to secure 
    the guest. True equilibrium is shifting your mix toward low-P02 
    direct business to keep more wealth inside the property.
    """)

with s3:
    st.write("### ⚖️ The Profit Floor")
    st.info("""
    **The Final Take-Home:** This is your net rate minus maintenance 
    and all other variable costs. It is the absolute minimum cash 
    the hotel must retain per room to remain financially sustainable.
    """)
