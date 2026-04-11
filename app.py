import streamlit as st

# --- BRANDING ---
st.set_page_config(page_title="Yield Equilibrium Auditor", page_icon="🏨", layout="wide")
st.title("🏨 Yield Equilibrium Auditor")
st.markdown("Developed by **Gayan Nugawela** | *The Revenue Engineer Framework*")
st.divider()

# --- SIDEBAR ---
st.sidebar.header("⚙️ Global Settings")
tax_div = st.sidebar.number_input("Tax Formula (Divisor)", value=1.2327, format="%.4f")

def get_input(label, adr_def, comm_def, maint_def, floor_def):
    with st.sidebar.expander(f"📊 {label}"):
        a = st.number_input(f"{label} ADR", value=adr_def)
        c = st.number_input(f"{label} Comm %", value=comm_def)
        m = st.number_input(f"{label} Maint", value=maint_def)
        f = st.number_input(f"{label} Floor", value=floor_def)
    return a, c, m, f

ota = get_input("OTA", 195.0, 0.18, 11.0, 105.0)
drct = get_input("Direct", 220.0, 0.02, 10.0, 100.0)
corp = get_input("Corp", 180.0, 0.0, 10.0, 95.0)
whls = get_input("Wholesale", 130.0, 0.15, 15.0, 110.0)

# --- ENGINE ---
def audit(adr, comm, maint, floor):
    net = (adr / tax_div) * (1 - comm) - maint
    if net >= (floor + 10): return net, "OPTIMIZED", "green"
    elif net >= floor: return net, "STABLE", "orange"
    else: return net, "DILUTIVE", "red"

# --- DISPLAY ---
st.subheader("Executive Verdict")
cols = st.columns(4)
for i, (name, data) in enumerate({"OTA":ota, "Direct":drct, "Corp":corp, "Wholesale":whls}.items()):
    val, stat, colr = audit(*data)
    with cols[i]:
        st.metric(f"{name} Net", f"${val:.2f}")
        if colr == "green": st.success(f"🟢 {stat}")
        elif colr == "orange": st.warning(f"🟡 {stat}")
        else: st.error(f"🔴 {stat}")

st.divider()

# --- DEFINITIONS ---
st.subheader("📖 Revenue Engineering Glossary")
g1, g2, g3 = st.columns(3)
with g1:
    st.write("### 🏷️ P02: Commission")
    st.write("Acquisition Cost: The fee paid to secure the booking.")
    st.success("**OPTIMIZED:** Wealth Builder. High margin profit.")
with g2:
    st.write("### 🧼 P01: Maintenance")
    st.write("Asset Reset: Costs for Labor, Linen, and Amenities.")
    st.warning("**STABLE:** Margin Warning. Thin operational surplus.")
with g3:
    st.write("### 🎯 Profit Floor")
    st.write("Sustainability: The minimum 'Take-Home' required per stay.")
    st.error("**DILUTIVE:** Wealth Destroyer. Eroding asset value.")
