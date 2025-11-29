import json
from datetime import datetime

class Memory:
    def __init__(self):
        # Default Preferences
        self.preferences = {
            "focus_time_start": "09:00",
            "focus_time_end": "12:00",
            "sleep_time": "23:00",
            "work_style": "Pomodoro (25m work / 5m break)",
        }
        # Dynamic State
        self.goals = []
        self.extracted_tasks = [] # List of dicts: {task, deadline, priority}
        self.schedule = [] # List of dicts: {time, task, duration}

    def update_preferences(self, focus_start, focus_end, sleep_time, work_style):
        self.preferences["focus_time_start"] = focus_start
        self.preferences["focus_time_end"] = focus_end
        self.preferences["sleep_time"] = sleep_time
        self.preferences["work_style"] = work_style

    def set_goals(self, goals_text):
        self.goals = [g.strip() for g in goals_text.split('\n') if g.strip()]

    def add_extracted_task(self, task, deadline=None, priority="Medium"):
        self.extracted_tasks.append({
            "task": task,
            "deadline": deadline,
            "priority": priority
        })

    def set_schedule(self, schedule_list):
        self.schedule = schedule_list

    def get_context_string(self):
        """Returns a formatted string for the agent prompt."""
        return f"""
* **Current Date:** {datetime.now().strftime('%Y-%m-%d')}
* **Goals:** {', '.join(self.goals)}
* **Best Focus Time:** {self.preferences['focus_time_start']} - {self.preferences['focus_time_end']}
* **Sleep Time:** {self.preferences['sleep_time']}
* **Work Style:** {self.preferences['work_style']}
* **Extracted Tasks:** {json.dumps(self.extracted_tasks, indent=2)}
"""
