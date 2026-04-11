import streamlit as st

# --- BRANDING ---
st.set_page_config(page_title="Yield Equilibrium Auditor", page_icon="🏨", layout="wide")
st.title("🏨 Yield Equilibrium Auditor")
st.markdown("Developed by **Gayan Nugawela** | *The Revenue Engineer Framework*")
st.divider()

# --- SIDEBAR INPUTS ---
st.sidebar.header("⚙️ Global Settings")
# Professional "Tax Formula" Divisor
tax_formula = st.sidebar.number_input("Tax Formula (Divisor)", value=1.2327, format="%.4f", help="The surgical formula to reverse-calculate taxes (e.g., Gross / 1.2327).")

def get_input(label, adr_def, comm_def, maint_def, floor_def):
    with st.sidebar.expander(label):
        a = st.number_input(f"{label} ADR", value=adr_def, help=f"Enter Gross ADR for {label}.")
        c = st.number_input(f"{label} Comm %", value=comm_def, help="P02: Acquisition cost as a decimal.")
        m = st.number_input(f"{label} Maint", value=maint_def, help="P01: Fixed asset reset costs.")
        f = st.number_input(f"{label} Floor", value=floor_def, help="Surgical Profit Floor target.")
    return a, c, m, f

ota = get_input("OTA", 195.0, 0.18, 11.0, 105.0)
drct = get_input("Direct", 220.0, 0.02, 10.0, 100.0)
corp = get_input("Corp", 180.0, 0.0, 10.0, 95.0)
whls = get_input("Wholesale", 130.0, 0.15, 15.0, 110.0)

# --- THE SURGICAL ENGINE ---
def audit(adr, comm, maint, floor):
    # Mathematical Formula: (Gross / Tax Formula) * (1 - Commission) - Maintenance
    net = (adr / tax_formula) * (1 - comm) - maint
    
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

# --- QUICK GUIDE ---
st.subheader("📖 Quick Guide")
c1, c2, c3 = st.columns(3)
with c1:
    st.write("### 🏷️ Tax Formula")
    st.write(f"Surgical Divisor used: **{tax_formula}**. This strips all inclusive fees to find the pure Base ADR.")
    st.success("**OPTIMIZED:** Wealth builder.")
with c2:
    st.write("### 🧼 P01: Asset Reset")
    st.write("Ensures you aren't selling below your physical cost (Laundry + Labor).")
    st.warning("**STABLE:** Margin warning.")
with c3:
    st.write("### 🎯 Profit Floor")
    st.write("The minimum 'Take-Home' required per room. Below this, you erode asset value.")
    st.error("**DILUTIVE:** Wealth destroyer.")
