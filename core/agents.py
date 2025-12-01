import json
import google.generativeai as genai
from core.utils import trace_agent, AgentLogger
from core.tools import CalendarTool, TaskTool

class BaseAgent:
    def __init__(self, name):
        self.name = name

    def run(self, *args, **kwargs):
        raise NotImplementedError

class ReminderAgent(BaseAgent):
    def __init__(self):
        super().__init__("Reminder Agent")

    @trace_agent
    def run(self, user_input):
        """
        Uses Gemini to extract tasks and deadlines from user input.
        """
        model = genai.GenerativeModel('gemini-2.0-flash')
        prompt = f"""
        You are a Senior Executive Assistant with a talent for structured thinking.
        Your goal is to turn the user's stream-of-consciousness input into a clear, actionable task list.

        User Input:
        "{user_input}"

        Instructions:
        1. Analyze the input for explicit tasks (e.g., "Email Bob") and implied tasks (e.g., "Prepare for meeting" implies "Read agenda").
        2. Assign a realistic deadline (HH:MM) if mentioned or implied (e.g., "morning" -> 11:00).
        3. Assign a Priority (High/Medium/Low) based on urgency and impact.
        4. If the input is vague, create a task to "Clarify requirements".

        Return a JSON list of objects, where each object has:
        - "task": The task description (concise and actionable)
        - "deadline": The deadline time (HH:MM) or null
        - "priority": "High", "Medium", or "Low"

        Return ONLY valid JSON.
        """
        try:
            response = model.generate_content(prompt)
            text = response.text.replace("```json", "").replace("```", "").strip()
            tasks = json.loads(text)
            return tasks
        except Exception as e:
            AgentLogger().log("ERROR", "ReminderAgent Failed", {"error": str(e)})
            return [{"task": "Error parsing input", "deadline": None, "priority": "High", "error": str(e)}]

class TaskPlannerAgent(BaseAgent):
    def __init__(self, memory_bank, session_service):
        super().__init__("Task Planner Agent")
        self.memory_bank = memory_bank
        self.session_service = session_service
        self.calendar_tool = CalendarTool() # In a real app, inject this

    @trace_agent
    def run(self):
        """
        Uses Gemini to schedule tasks based on memory and calendar.
        """
        context = self.session_service.get_context_string(self.memory_bank)
        calendar_events = self.calendar_tool.read_calendar()

        model = genai.GenerativeModel('gemini-2.0-flash')
        prompt = f"""
        You are a World-Class Logistics Manager and Productivity Expert.
        Your goal is to create the perfect daily schedule that maximizes flow and minimizes burnout.

        Context:
        {context}

        Existing Calendar Events:
        {calendar_events}

        Instructions:
        1. **Deep Work First**: Schedule High-priority, high-cognitive tasks during the user's "Focus Time" ({self.memory_bank.get_preference('focus_time_start')} - {self.memory_bank.get_preference('focus_time_end')}).
        2. **Batching**: Group shallow tasks (emails, calls) together outside of focus blocks.
        3. **Realistic Buffers**: Leave 5-10 minutes between tasks. Do not back-to-back schedule without breaks.
        4. **Respect Constraints**: Do not double-book against Existing Calendar Events.
        5. **Granularity**: Break down large tasks into 45-90 minute blocks.

        Create a detailed schedule starting at 09:00 (or the current time if later).

        Return a JSON list of objects, where each object has:
        - "time": Start time (HH:MM)
        - "task": Task name
        - "duration": Duration string (e.g., "60 mins")
        - "priority": Task priority
        - "status": "Scheduled"

        Return ONLY valid JSON.
        """

        try:
            response = model.generate_content(prompt)
            text = response.text.replace("```json", "").replace("```", "").strip()
            schedule = json.loads(text)
            return schedule
        except Exception as e:
            AgentLogger().log("ERROR", "TaskPlannerAgent Failed", {"error": str(e)})
            return [{"time": "09:00", "task": "Error generating schedule", "duration": "0 mins", "priority": "High", "status": "Error"}]

class FocusCoachAgent(BaseAgent):
    def __init__(self):
        super().__init__("Focus Coach Agent")

    @trace_agent
    def run(self, schedule, work_style):
        """
        Uses Gemini to suggest a workflow based on the schedule.
        """
        model = genai.GenerativeModel('gemini-2.0-flash')
        prompt = f"""
        You are a Behavioral Science Performance Coach.
        Your goal is to mentally prepare the user for their day using psychological techniques.

        User's Work Style: {work_style}

        Current Schedule:
        {json.dumps(schedule)}

        Instructions:
        1. **Analyze the Load**: Is the day heavy? Light? Balanced? Acknowledge it.
        2. **Tactical Advice**: Suggest specific techniques based on the Work Style (e.g., for Pomodoro, remind them to actually stand up during breaks).
        3. **Motivation**: Provide a stoic or encouraging thought to start the day.
        4. **Tone**: Professional, empathetic, and concise.

        Provide a short, 3-4 sentence paragraph.
        """

        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
             AgentLogger().log("ERROR", "FocusCoachAgent Failed", {"error": str(e)})
             return "Keep pushing! You can do this."

class LoopAgent(BaseAgent):
    """
    Manages the daily planning loop.
    """
    def __init__(self, memory_bank, session_service):
        super().__init__("Loop Agent")
        self.memory_bank = memory_bank
        self.session_service = session_service
        self.reminder_agent = ReminderAgent()
        self.planner_agent = TaskPlannerAgent(memory_bank, session_service)
        self.coach_agent = FocusCoachAgent()

    @trace_agent
    def run(self, user_input):
        # 1. Extract Tasks
        tasks = self.reminder_agent.run(user_input)
        self.session_service.extracted_tasks = tasks # Update session

        # 2. Generate Schedule
        schedule = self.planner_agent.run()
        self.session_service.set_schedule(schedule) # Update session

        # 3. Get Coaching Advice
        advice = self.coach_agent.run(schedule, self.memory_bank.get_preference("work_style"))

        return {
            "tasks": tasks,
            "schedule": schedule,
            "advice": advice
        }

class OrchestratorAgent(BaseAgent):
    """
    Main entry point. Routes requests to the appropriate sub-agent or flow.
    """
    def __init__(self, memory_bank, session_service):
        super().__init__("Orchestrator Agent")
        self.loop_agent = LoopAgent(memory_bank, session_service)

    @trace_agent
    def run(self, user_input, intent="plan_day"):
        if intent == "plan_day":
            return self.loop_agent.run(user_input)
        else:
            # Future expansion: Handle other intents like "add_task", "reschedule", etc.
            return {"error": "Unknown intent"}
