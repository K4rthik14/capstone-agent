import json
import time
from tools import CalendarTool

class BaseAgent:
    def __init__(self, name):
        self.name = name

    def run(self, input_data):
        raise NotImplementedError

class ReminderAgent(BaseAgent):
    def __init__(self):
        super().__init__("Reminder Agent")

    def run(self, user_input):
        """
        Mock LLM: Extracts tasks and deadlines from user input.
        """
        # Simulate thinking
        time.sleep(1)

        # Simple heuristic for mock: check for "by [time]" or "at [time]"
        # In a real LLM, this would be a prompt call.

        tasks = []
        if "capstone" in user_input.lower():
            tasks.append({"task": "Work on Capstone Project", "deadline": "17:00", "priority": "High"})
        if "email" in user_input.lower():
            tasks.append({"task": "Reply to Emails", "deadline": None, "priority": "Low"})

        # Fallback if no keywords found
        if not tasks:
            tasks.append({"task": "General Research", "deadline": None, "priority": "Medium"})

        return tasks

class TaskPlannerAgent(BaseAgent):
    def __init__(self, memory):
        super().__init__("Task Planner Agent")
        self.memory = memory
        self.calendar = CalendarTool()

    def run(self):
        """
        Mock LLM: Schedules tasks based on memory and calendar.
        """
        # Simulate thinking
        time.sleep(1.5)

        context = self.memory.get_context_string()
        # In a real agent, we would pass 'context' to the LLM.

        # Mock Logic:
        # 1. Get tasks from memory
        tasks = self.memory.extracted_tasks

        # 2. Schedule High priority first during Focus Time
        schedule = []
        current_hour = 9 # Start at 9 AM

        for task in tasks:
            start_time = f"{current_hour:02d}:00"
            duration = 60 if task['priority'] == 'High' else 30

            # Check conflicts (Mock check)
            conflicts = self.calendar.check_availability(start_time, duration)

            schedule.append({
                "time": start_time,
                "task": task['task'],
                "duration": f"{duration} mins",
                "priority": task['priority'],
                "status": "Scheduled"
            })

            current_hour += 1 # Simple increment

        return schedule

class FocusCoachAgent(BaseAgent):
    def __init__(self):
        super().__init__("Focus Coach Agent")

    def run(self, schedule, work_style):
        """
        Mock LLM: Suggests a workflow based on the schedule.
        """
        time.sleep(1)

        if "Pomodoro" in work_style:
            return f"""
**Focus Strategy: Pomodoro Technique**
Based on your schedule, here is your workflow:
1.  **Start with High Priority**: Tackle the first task using 25m work / 5m break intervals.
2.  **Break Management**: Take a longer 15m break after 4 cycles.
3.  **Low Energy Blocks**: Use the afternoon slots for lower priority tasks like emails.
"""
        else:
            return "Just keep swimming! Focus on one task at a time."
