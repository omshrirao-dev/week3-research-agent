import streamlit as st
import time
from graph import run_research

st.set_page_config(
    page_title="Research Agent",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Autonomous Research Agent")
st.caption("Powered by LangGraph + Groq + Tavily")

with st.sidebar:
    st.header("How it works")
    st.markdown("""
    1. Enter any research topic
    2. Agent searches the web
    3. Agent reads full articles
    4. Agent writes a structured report
    5. Report saved as markdown file
    """)
    st.divider()
    st.caption("Built with LangGraph ReAct loop")

topic = st.text_input(
    "Enter research topic",
    placeholder="e.g. How do AI agents work in 2024?"
)

if st.button("Start Research", type="primary"):
    if not topic.strip():
        st.error("Please enter a topic first.")
    else:
        with st.status("Agent is researching...", expanded=True) as status:
            st.write("🔎 Searching the web...")
            start_time = time.time()
            
            try:
                result = run_research(topic)
                elapsed = round(time.time() - start_time, 1)
                
                status.update(
                    label=f"Research complete in {elapsed}s",
                    state="complete"
                )
                
                st.success("Report ready!")
                st.markdown("---")
                st.markdown(result["result"])
                
            except Exception as e:
                status.update(label="Research failed", state="error")
                st.error(f"Error: {str(e)}")