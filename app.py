import streamlit as st
import pandas as pd
import time
from memory import Memory
from agents import ReminderAgent, TaskPlannerAgent, FocusCoachAgent

# Page Config
st.set_page_config(page_title="Daily Productivity OS", page_icon="🤖", layout="wide")

# Initialize Session State
if "memory" not in st.session_state:
    st.session_state.memory = Memory()
if "generated" not in st.session_state:
    st.session_state.generated = False

# --- Sidebar: Memory & Preferences ---
with st.sidebar:
    st.header("🧠 Agent Memory")
    st.info("Configure the agent's long-term memory and preferences here.")

    focus_start = st.time_input("Focus Time Start", value=pd.to_datetime("09:00").time())
    focus_end = st.time_input("Focus Time End", value=pd.to_datetime("12:00").time())
    sleep_time = st.time_input("Sleep Time", value=pd.to_datetime("23:00").time())
    work_style = st.selectbox("Work Style", ["Pomodoro (25m work / 5m break)", "Deep Work (90m blocks)", "Flow State (Unstructured)"])

    if st.button("Update Memory"):
        st.session_state.memory.update_preferences(
            focus_start.strftime("%H:%M"),
            focus_end.strftime("%H:%M"),
            sleep_time.strftime("%H:%M"),
            work_style
        )
        st.success("Memory Updated!")

# --- Main Interface ---
st.title("🤖 Daily Productivity OS")
st.markdown("### Your Multi-Agent Personal Assistant")

# User Input
user_input = st.text_area("What are your goals for today?", placeholder="e.g., I need to finish the Capstone report by 5 PM and email the team.")

if st.button("Generate Schedule"):
    st.session_state.generated = True

    # 1. Initialize Agents
    reminder_agent = ReminderAgent()
    planner_agent = TaskPlannerAgent(st.session_state.memory)
    coach_agent = FocusCoachAgent()

    # --- Agent 1: Reminder Agent ---
    st.markdown("---")
    st.subheader("1. 🟡 Reminder Agent")
    with st.status("Extracting tasks and deadlines...", expanded=True) as status:
        st.write("Analyzing your input...")
        extracted_tasks = reminder_agent.run(user_input)

        # Update Memory with extracted tasks
        st.session_state.memory.extracted_tasks = extracted_tasks
        st.session_state.memory.set_goals(user_input)

        st.write("✅ Tasks Extracted:")
        st.json(extracted_tasks)
        status.update(label="Reminder Agent Complete", state="complete", expanded=False)

    # --- Agent 2: Task Planner Agent ---
    st.subheader("2. 🟢 Task Planner Agent")
    with st.status("Scheduling your day...", expanded=True) as status:
        st.write("Checking calendar availability...")
        st.write("Prioritizing tasks based on Focus Time...")

        schedule = planner_agent.run()
        st.session_state.memory.set_schedule(schedule)

        st.write("✅ Schedule Generated!")
        status.update(label="Task Planner Complete", state="complete", expanded=False)

        # Display Schedule nicely
        df = pd.DataFrame(schedule)
        st.dataframe(df, use_container_width=True)

    # --- Agent 3: Focus Coach Agent ---
    st.subheader("3. 🟣 Focus Coach Agent")
    with st.chat_message("assistant", avatar="🟣"):
        with st.spinner("Analyzing schedule for optimal flow..."):
            advice = coach_agent.run(schedule, st.session_state.memory.preferences["work_style"])
            st.markdown(advice)

# --- Footer ---
if st.session_state.generated:
    st.markdown("---")
    st.caption("System Status: All Agents Executed Successfully. Ready for execution.")
