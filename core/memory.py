import json
import os
from datetime import datetime
from core.utils import AgentLogger

MEMORY_FILE = "user_preferences.json"

class MemoryBank:
    """
    Long-term memory storage for user preferences and persistent data.
    Implements the 'Memory Bank' pattern.
    """
    def __init__(self, filepath=MEMORY_FILE):
        self.filepath = filepath
        self.preferences = self._load_memory()

    def _load_memory(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'r') as f:
                    return json.load(f)
            except Exception as e:
                AgentLogger().log("ERROR", "Failed to load memory bank", {"error": str(e)})

        # Default Preferences
        return {
            "focus_time_start": "09:00",
            "focus_time_end": "12:00",
            "sleep_time": "23:00",
            "work_style": "Pomodoro (25m work / 5m break)",
            "energy_pattern": "Morning Person",
            "api_key": ""
        }

    def save_memory(self):
        try:
            with open(self.filepath, 'w') as f:
                json.dump(self.preferences, f, indent=4)
            AgentLogger().log("INFO", "Memory Bank Saved")
        except Exception as e:
            AgentLogger().log("ERROR", "Failed to save memory bank", {"error": str(e)})

    def update_preference(self, key, value):
        self.preferences[key] = value
        self.save_memory()

    def get_preference(self, key):
        return self.preferences.get(key)

class InMemorySessionService:
    """
    Short-term working memory for the current active session.
    Stores extracted tasks, current schedule, and immediate goals.
    """
    def __init__(self):
        self.goals = []
        self.extracted_tasks = []
        self.schedule = []
        self.chat_history = []

    def set_goals(self, goals_text):
        self.goals = [g.strip() for g in goals_text.split('\n') if g.strip()]

    def add_extracted_task(self, task_dict):
        self.extracted_tasks.append(task_dict)

    def set_schedule(self, schedule_list):
        self.schedule = schedule_list

    def add_chat(self, role, message):
        self.chat_history.append({"role": role, "message": message})

    def get_context_string(self, memory_bank: MemoryBank):
        """
        Compacts and returns the full context for the agent.
        Combines Long-term (MemoryBank) and Short-term (Session) memory.
        """
        prefs = memory_bank.preferences

        context = f"""
* **Current Date:** {datetime.now().strftime('%Y-%m-%d')}
* **User Profile:**
    - Focus Time: {prefs.get('focus_time_start')} - {prefs.get('focus_time_end')}
    - Sleep Time: {prefs.get('sleep_time')}
    - Work Style: {prefs.get('work_style')}
    - Energy Pattern: {prefs.get('energy_pattern')}

* **Current Session Goals:**
{', '.join(self.goals) if self.goals else "No specific goals set yet."}

* **Pending Tasks:**
{json.dumps(self.extracted_tasks, indent=2) if self.extracted_tasks else "[]"}

* **Current Schedule:**
{json.dumps(self.schedule, indent=2) if self.schedule else "[]"}
"""
        return context
