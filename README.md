# Daily Productivity OS Agent 🤖

**Kaggle Agentic Coding Competition Submission**

## 🚀 Problem Statement
Managing daily tasks, calendars, and energy levels is complex. Traditional to-do lists are static and don't account for "focus time" or "energy patterns." We need an intelligent system that doesn't just list tasks but **orchestrates** a day based on personal work styles.

## 💡 Solution
The **Daily Productivity OS** is a multi-agent system powered by **Google Gemini 2.0 Flash**. It acts as a personal executive assistant that:
1.  **Understands** natural language goals.
2.  **Extracts** actionable tasks.
3.  **Schedules** them intelligently around existing calendar events and user preferences (e.g., "Deep Work" mornings).
4.  **Coaches** the user on how to execute the day.

## 🏗️ Architecture

The system uses a **Hub-and-Spoke** multi-agent architecture with a **Memory Bank** for persistence.

```mermaid
graph TD
    User[User Input] --> App[Streamlit UI]
    App --> Orchestrator[Orchestrator Agent]

    subgraph "Core Agent System"
        Orchestrator --> Loop[Loop Agent]
        Loop --> Reminder[Reminder Agent]
        Loop --> Planner[Task Planner Agent]
        Loop --> Coach[Focus Coach Agent]
    end

    subgraph "Tools (MCP Style)"
        Planner --> CalendarTool[Calendar Tool]
        Reminder --> TaskTool[Task Tool]
    end

    subgraph "Memory"
        Loop --> Session[InMemory Session]
        Loop --> Bank[Memory Bank (JSON)]
    end

    subgraph "Observability"
        Orchestrator -.-> Logger[Agent Logger]
        Loop -.-> Logger
    end
```

## ✨ Key Features

### 1. Multi-Agent Orchestration
-   **Orchestrator Agent**: Routes user intent.
-   **Reminder Agent**: Extracts structured tasks from unstructured text.
-   **Task Planner Agent**: Optimizes schedules using constraint satisfaction (via LLM).
-   **Focus Coach Agent**: Provides motivational and tactical advice.

### 2. MCP-Style Tools
-   `read_calendar` / `write_calendar`: Manages time slots.
-   `read_tasklist` / `write_tasklist`: Manages task state.
-   *Designed to be easily extensible to real Google Calendar APIs.*

### 3. Memory Bank & Context
-   **Memory Bank**: Persists user preferences (Sleep time, Work style) to `user_preferences.json`.
-   **Session Service**: Maintains short-term context for the current planning session.

### 4. Observability
-   **Tracing**: Custom decorators (`@trace_agent`, `@trace_tool`) capture execution time, inputs, and outputs.
-   **Live Logs**: Visible directly in the UI for debugging and transparency.

## 🛠️ How to Run

1.  **Clone the repository**:
    ```bash
    git clone <repo-url>
    cd capstone-agent
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application**:
    ```bash
    streamlit run app.py
    ```

4.  **Enter your Google API Key** in the sidebar (Get one from [Google AI Studio](https://aistudio.google.com/)).

## 📝 Example Session

**User Input:**
> "I need to finish the Q3 report by 2 PM, email the marketing team, and prepare for the 4 PM client call."

**Agent Output:**
1.  **Tasks Extracted**:
    -   "Finish Q3 Report" (High Priority, Deadline: 14:00)
    -   "Email Marketing Team" (Low Priority)
    -   "Prepare for Client Call" (Medium Priority)
2.  **Schedule**:
    -   09:00 - 11:00: Finish Q3 Report (Deep Work Block)
    -   11:00 - 11:30: Email Marketing Team
    -   13:00 - 14:00: Prepare for Client Call
3.  **Coach Advice**:
    -   "You have a heavy morning. Use the Pomodoro technique for the report to stay fresh. Take a real lunch break before prep!"

## 📦 File Structure
-   `app.py`: Streamlit UI entry point.
-   `core/agents.py`: Agent logic and definitions.
-   `core/tools.py`: Tool definitions.
-   `core/memory.py`: Memory management.
-   `core/utils.py`: Logging and tracing utilities.
