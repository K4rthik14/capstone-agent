import streamlit as st
import pandas as pd
import time
from core.memory import MemoryBank, InMemorySessionService
from core.agents import OrchestratorAgent
from core.utils import AgentLogger
import google.generativeai as genai

# Page Config
st.set_page_config(page_title="Daily Productivity OS", page_icon="🤖", layout="wide")

# Initialize Session State
if "memory_bank" not in st.session_state:
    st.session_state.memory_bank = MemoryBank()
if "session_service" not in st.session_state:
    st.session_state.session_service = InMemorySessionService()
if "generated" not in st.session_state:
    st.session_state.generated = False

# --- Sidebar: Configuration ---
with st.sidebar:
    st.header("🧠 Agent Configuration")

    # API Key
    stored_api_key = st.session_state.memory_bank.get_preference("api_key")
    api_key = st.text_input("Google API Key", value=stored_api_key, type="password", help="Required for Gemini 2.0 Flash")

    if api_key:
        genai.configure(api_key=api_key)
        if api_key != stored_api_key:
            st.session_state.memory_bank.update_preference("api_key", api_key)
            st.toast("API Key saved!")
    else:
        st.warning("Please enter your Google API Key to proceed.")

    st.divider()

    # Memory Bank Preferences
    st.subheader("Preferences (Memory Bank)")
    prefs = st.session_state.memory_bank.preferences

    focus_start = st.time_input("Focus Time Start", value=pd.to_datetime(prefs.get("focus_time_start", "09:00")).time())
    focus_end = st.time_input("Focus Time End", value=pd.to_datetime(prefs.get("focus_time_end", "12:00")).time())
    sleep_time = st.time_input("Sleep Time", value=pd.to_datetime(prefs.get("sleep_time", "23:00")).time())
    options = ["Pomodoro (25m work / 5m break)", "Deep Work (90m blocks)", "Flow State (Unstructured)"]
    current_style = prefs.get("work_style", "Pomodoro (25m work / 5m break)")
    try:
        index = options.index(current_style)
    except ValueError:
        index = 0

    work_style = st.selectbox("Work Style", options, index=index)

    if st.button("Update Memory Bank"):
        st.session_state.memory_bank.update_preference("focus_time_start", focus_start.strftime("%H:%M"))
        st.session_state.memory_bank.update_preference("focus_time_end", focus_end.strftime("%H:%M"))
        st.session_state.memory_bank.update_preference("sleep_time", sleep_time.strftime("%H:%M"))
        st.session_state.memory_bank.update_preference("work_style", work_style)
        st.success("Memory Updated!")

# --- Main Interface ---
st.title("🤖 Daily Productivity OS")
st.markdown("### Your Multi-Agent Personal Assistant")

# User Input
user_input = st.text_area("What are your goals for today?", placeholder="e.g., I need to finish the Capstone report by 5 PM and email the team.")

if st.button("Generate Schedule", disabled=not api_key):
    st.session_state.generated = True
    AgentLogger().clear() # Clear previous logs

    # Initialize Orchestrator
    orchestrator = OrchestratorAgent(st.session_state.memory_bank, st.session_state.session_service)

    # Run the Agent Flow
    with st.status("🤖 Agents Working...", expanded=True) as status:
        st.write("Orchestrator: Delegating to Loop Agent...")
        result = orchestrator.run(user_input, intent="plan_day")
        status.update(label="Planning Complete!", state="complete", expanded=False)

    # Display Results
    if "error" in result:
        st.error(f"An error occurred: {result['error']}")
    else:
        # 1. Schedule
        st.subheader("1. Optimized Schedule")
        df = pd.DataFrame(result["schedule"])
        st.dataframe(df, use_container_width=True)

        # 2. Coaching
        st.subheader("2. Focus Coach Advice")
        st.info(result["advice"])

        # 3. Tasks (Hidden by default)
        with st.expander("📝 View Extracted Tasks (Raw Data)"):
            st.json(result["tasks"])

# --- Observability Section ---
st.divider()
with st.expander("🛠️ Debug & Observability (Logs & Traces)"):
    st.caption("Real-time logs from the Agent System")
    logs = AgentLogger().get_logs()
    for log in logs:
        if log['level'] == 'INFO':
            st.success(f"[{log['timestamp']}] {log['message']}")
        elif log['level'] == 'ERROR':
            st.error(f"[{log['timestamp']}] {log['message']}")

        if log.get('details'):
            st.json(log['details'])
