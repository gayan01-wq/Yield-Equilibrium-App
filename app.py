import streamlit as st

# --- BRANDING ---
st.set_page_config(page_title="Yield Equilibrium Auditor", page_icon="🏨", layout="wide")
st.title("🏨 Yield Equilibrium Auditor")
st.markdown("Developed by **Gayan Nugawela** | *The Revenue Engineer Framework*")
st.divider()

# --- SIDEBAR INPUTS ---
st.sidebar.header("📊 Data & Calibration")
tax = st.sidebar.number_input("Tax (%)", 0.08)

def get_input(label, adr_def, comm_def, maint_def, floor_def):
    with st.sidebar.expander(label):
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
    net = (adr / (1 + tax)) * (1 - comm) - maint
    if net >= (floor + 10): return net, "OPTIMIZED", "green"
    elif net >= floor: return net, "STABLE", "orange"
    else: return net, "DILUTIVE", "red"

# --- DISPLAY ---
st.subheader("Executive Verdict")
cols = st.columns(4)
for i, (name, data) in enumerate({"OTA":ota, "Direct":drct, "Corp":corp, "Wholesale":whls}.items()):
    val, status, color = audit(*data)
    with cols[i]:
        st.metric(f"{name} Net", f"${val:.2f}")
        if color == "green": st.success(status)
        elif color == "orange": st.warning(status)
        else: st.error(status)

st.divider()

# --- COMPACT GUIDE ---
st.subheader("📖 Quick Guide")
c1, c2, c3 = st.columns(3)
with c1:
    st.write("**P02 (Comm):** Channel costs.")
    st.success("GREEN: Wealth builder.")
with c2:
    st.write("**P01 (Maint):** Room reset costs.")
    st.warning("YELLOW: Thin margins.")
with c3:
    st.write("**Floor:** Your minimum target.")
    st.error("RED: Asset erosion.")
