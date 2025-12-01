# Daily Productivity OS: The Agentic Chief of Operations

## 🚀 Executive Summary
In a world of infinite distractions, static to-do lists are obsolete. They fail to account for the most critical variables of productivity: **energy, focus, and time constraints**.

The **Daily Productivity OS** is not just a task manager; it is an **Agentic Chief of Operations (COO)** for your life. Built on a modular multi-agent architecture powered by **Google Gemini 2.0 Flash**, it transforms unstructured "brain dumps" into optimized, realistic schedules. It doesn't just list tasks—it *negotiates* with your reality, aligning high-cognitive work with your peak energy windows and managing your calendar like a human executive assistant.

## 🏗️ System Architecture: The Hub-and-Spoke Model
To ensure reliability and separation of concerns, the system employs a robust **Hub-and-Spoke** multi-agent architecture.

```mermaid
graph TD
    User[User Input] --> Orchestrator[Orchestrator Agent]

    subgraph "Core Agent Cluster"
        Orchestrator --> Loop[Loop Agent (The Manager)]
        Loop --> Reminder[Reminder Agent (The Parser)]
        Loop --> Planner[Task Planner Agent (The Strategist)]
        Loop --> Coach[Focus Coach Agent (The Psychologist)]
    end

    subgraph "Memory & State"
        Loop <--> Session[InMemory Session]
        Loop <--> Bank[Memory Bank (Persistent JSON)]
    end

    subgraph "MCP Tools"
        Planner <--> Calendar[Calendar Tool]
        Reminder <--> TaskList[Task Tool]
    end
```

### The Agent Team
1.  **Orchestrator Agent**: The entry point that understands user intent and routes requests.
2.  **Reminder Agent (The Parser)**: Uses advanced semantic analysis to extract structured tasks, deadlines, and priorities from messy natural language.
3.  **Task Planner Agent (The Strategist)**: A constraint-satisfaction engine that maps tasks to time slots. It respects "Deep Work" blocks, avoids calendar conflicts, and ensures realistic duration estimates.
4.  **Focus Coach Agent (The Psychologist)**: Analyzes the generated schedule and provides tactical advice (e.g., "You have a heavy morning; take a walk at 11 AM") based on the user's work style.

## 💡 Key Innovations

### 1. The "Memory Bank" Pattern
Agents often suffer from amnesia. This system implements a **Memory Bank** that persists user preferences (Sleep Time, Energy Patterns, Work Style) to a local JSON store. The agent "learns" you over time, eliminating the need to repeat your preferences.

### 2. MCP-Native Tooling
The system adopts the **Model Context Protocol (MCP)** standard for its tools (`read_calendar`, `write_calendar`). This ensures the architecture is future-proof and can be easily connected to real-world APIs like Google Calendar or Notion with minimal refactoring.

### 3. White-Box Observability
Trust is the biggest barrier to AI adoption. I implemented a custom **Tracing System** (`@trace_agent`) that streams real-time execution logs (inputs, outputs, latency) to the UI. This "Glass Box" approach allows users to see exactly *why* the agent made a decision.

## 🌍 Real-World Value
This system solves the "Paralysis by Analysis" problem. By automating the cognitive load of **planning**, it frees the user to focus on **executing**.
-   **For the Student**: Aligns study blocks with peak focus times.
-   **For the Professional**: Protects "Deep Work" hours from meeting creep.
-   **For the ADHD Mind**: Breaks overwhelming days into manageable, structured chunks.

## 🛠️ Tech Stack
-   **LLM**: Google Gemini 2.0 Flash (via `google-generativeai`)
-   **Framework**: Streamlit (Python)
-   **Design Pattern**: Modular Monolith (`core/` package)

## 🔮 Future Roadmap
-   **Voice Interface**: Adding audio input/output for a true "Iron Man" Jarvis experience.
-   **Biometric Integration**: Using wearable data (Apple Watch) to adjust schedules based on real-time stress levels.
-   **RAG Integration**: Connecting to personal documents for deeper context awareness.
