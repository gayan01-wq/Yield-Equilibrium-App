import streamlit as st
import google.generativeai as genai

# --- Executive Styling ---
st.set_page_config(layout="wide", page_title="Executive Overview | Yield Equilibrium")
st.markdown("""<style>
    .main-header { color: #1e3799; font-weight: 900; text-transform: uppercase; }
    .theory-card { background: white; padding: 25px; border-radius: 12px; border-left: 10px solid #1e3799; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
</style>""", unsafe_allow_html=True)

# --- Data Retrieval from Home Page ---
if "current_audit" not in st.session_state:
    st.warning("No active analysis found. Please start at the Displacement Analyzer.")
    if st.button("⬅ Back to Analyzer"):
        st.switch_page("app.py")
    st.stop()

audit = st.session_state["current_audit"]

# --- Dashboard Layout ---
st.markdown(f"<h1 class='main-header'>Strategic Audit: {audit['label']}</h1>", unsafe_allow_html=True)
st.divider()

c1, c2, c3 = st.columns(3)
c1.metric("Net Wealth", f"﷼ {audit['yield']:,.2f}")
c2.metric("Effective Hurdle", f"﷼ {audit['hurdle']:,.2f}")
c3.metric("Verdict", audit['status'])

# --- AI Strategy Audit ---
st.subheader("🤖 Equilibrium Theory Audit")
try:
    # Uses the API key saved in your Streamlit Secrets
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    Provide a professional revenue management audit for:
    Segment: {audit['label']}
    Result: {audit['status']}
    Net Wealth: ﷼ {audit['yield']}
    Effective Hurdle: ﷼ {audit['hurdle']}
    
    Analyze based on Pillar 02: Wealth Protection and yield equilibrium optimization.
    """
    
    with st.spinner("Consulting Yield Equilibrium Protocol..."):
        response = model.generate_content(prompt)
        st.markdown(f"<div class='theory-card'>{response.text}</div>", unsafe_allow_html=True)
except Exception as e:
    st.error(f"Audit Connection Error: {str(e)}")

# --- Navigation ---
if st.button("Analyze Another Segment"):
    st.switch_page("app.py")
