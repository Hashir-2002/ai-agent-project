import streamlit as st
from agent.core import run_agent

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Agent",
    page_icon="🤖",
    layout="wide"
)

# ---------------- HEADER ----------------
st.markdown(
    """
    <h1 style='text-align: center; color: #4A90E2;'>
        🤖 AI Agent System
    </h1>
    <p style='text-align: center; color: gray;'>
        Tool-using AI assistant (Calculator • Web Search • Memory)
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()

# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("⚙️ Controls")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("### 🧠 Capabilities")
    st.markdown("- Calculator")
    st.markdown("- Web Search")
    st.markdown("- Notes Memory")
    st.markdown("- AI Responses")

# ---------------- CHAT DISPLAY ----------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------- USER INPUT ----------------
prompt = st.chat_input("Ask me anything...")

if prompt:

    # USER MESSAGE
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    # ---------------- AI THINKING ----------------
    with st.chat_message("assistant"):
        with st.spinner("🤖 Thinking..."):
            response = run_agent(prompt)

        # clean response rendering
        st.markdown(response)

    # SAVE ASSISTANT RESPONSE
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })