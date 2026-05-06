try:
    # 1. Force the API version to v1 during configuration
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"], transport='rest')
    
    # 2. Use the most basic model string that works with the rest transport
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
        # 3. Add safety settings if the API is being over-sensitive
        response = model.generate_content(prompt)
        st.markdown(f"<div class='theory-card'>{response.text}</div>", unsafe_allow_html=True)

except Exception as e:
    # This will now show us exactly what the API is rejecting
    st.error(f"Audit Connection Error: {str(e)}")
