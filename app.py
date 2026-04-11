import streamlit as st

# --- BRANDING ---
st.set_page_config(page_title="Yield Equilibrium Auditor", page_icon="🏨", layout="wide")
st.title("🏨 Yield Equilibrium Auditor")
st.markdown("Developed by **Gayan Nugawela** | *The Revenue Engineer Framework*")
st.divider()

# --- SIDEBAR INPUTS ---
st.sidebar.header("⚙️ Global Settings")
tax_formula = st.sidebar.number_input("Tax Formula (Divisor)", value=1.2327, format="%.4f")

def get_input(label, adr_def, comm_def, maint_def, floor_def):
    with st.sidebar.expander(f"📊 {label} Calibration"):
        a = st.number_input(f"{label} Gross ADR", value=adr_def)
        c = st.number_input(f"{label} Comm % (P02)", value=comm_def)
        m = st.number_input(f"{label} Maint (P01)", value=maint_def)
        f = st.number_input(f"{label} Profit Floor", value=floor_def)
    return a, c, m, f

ota = get_input("OTA", 195.0, 0.18, 11.0, 105.0)
drct = get_input("Direct", 220.0, 0.02, 10.0, 100.0)
corp = get_input("Corp", 180.0, 0.0, 10.0, 95.0)
whls = get_input("Wholesale", 130.0, 0.15, 15.0, 110.0)

# --- THE SURGICAL ENGINE ---
def audit(adr, comm, maint, floor):
    net = (adr / tax_formula) * (1 - comm) - maint
    if net >= (floor + 10): return net, "OPTIMIZED", "green"
    elif net >= floor: return net, "STABLE", "orange"
    else: return net, "DILUTIVE", "red"

# --- DISPLAY VERDICTS ---
st.subheader("Executive Verdict")
cols = st.columns(4)
for i, (name, data) in enumerate({"OTA":ota, "Direct":drct, "Corp":corp, "Wholesale":whls}.items()):
    val, status, color = audit(*data)
    with cols[i]:
        st.metric(f"{name} Net", f"${val:.2f}")
        if color == "green": st.success(f"🟢 {status}")
        elif color == "orange": st.warning(f"🟡 {status}")
        else: st.error(f"🔴 {status}")

st.divider()

# --- THE FULL DEFINITION GLOSSARY ---
st.subheader("📖 Revenue Engineering Glossary")
g1, g2, g3 = st.columns(3)

with g1:
    st.write("### 🏷️ P02: Commission")
    st.write("""
    **Definition:** The Acquisition Cost. 
    It is the fee paid to the channel (OTA) or bank (Direct) to secure the booking.
    * *Surgical Goal:* Minimize this to increase the 'Take-Home' ratio.
    """)
    st.success("**🟢 OPTIMIZED**")
    st.write("**Wealth Builder:** High margin. These bookings build owner wealth and future renovation funds.")

with g2:
    st.write("### 🧼 P01: Maintenance")
    st.write("""
    **Definition:** The Asset Reset Cost. 
    Includes Laundry, Labor, and Amenities. This is what it costs the hotel just to open the door.
    * *Surgical Goal:* Ensure ADR stays high enough to never sell below this cost.
    """)
    st.warning("**🟡 STABLE**")
    st.write("**Margin Warning:** Covering basic operational costs, but failing
