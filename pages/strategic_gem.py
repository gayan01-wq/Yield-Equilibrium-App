# --- 4. AI STRATEGY AUDIT (PILLAR 02) ---
st.subheader("🤖 Equilibrium Theory Audit")

try:
    # 1. Force the REST transport to bypass gRPC/v1beta errors often found in cloud environments
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"], transport='rest')
    
    # 2. Use the stable model name
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    As a senior AI Revenue Consultant, provide a professional audit for:
    Segment: {audit['label']}
    Result: {audit['status']}
    Net Wealth: ﷼ {audit['yield']}
    Effective Hurdle: ﷼ {audit['hurdle']}
    
    Analyze based on Pillar 02: Wealth Protection and yield equilibrium optimization.
    """
    
    with st.spinner("Consulting the Yield Equilibrium Protocol..."):
        response = model.generate_content(prompt)
        st.markdown(f"<div class='theory-card'>{response.text}</div>", unsafe_allow_html=True)

except Exception as e:
    # This captures the error properly now
    st.error(f"Audit Connection Error: {str(e)}")
    st.info("Tip: Ensure your GEMINI_API_KEY is correctly set in Streamlit Secrets.")
