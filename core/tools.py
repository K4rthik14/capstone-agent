import json
from core.utils import trace_tool

class CalendarTool:
    """
    MCP-style tool for Calendar operations.
    """
    def __init__(self):
        # Mock storage
        self.events = [
            {"start": "13:00", "end": "14:00", "event": "Team Sync"},
            {"start": "16:00", "end": "16:30", "event": "Coffee Chat"}
        ]

    @trace_tool
    def read_calendar(self, date: str = None):
        """
        Reads calendar events.
        Args:
            date: YYYY-MM-DD string. If None, returns all mock events.
        """
        # In a real app, filter by date
        return json.dumps(self.events)

    @trace_tool
    def write_calendar(self, event_name: str, start_time: str, duration_minutes: int):
        """
        Writes a new event to the calendar.
        """
        new_event = {
            "start": start_time,
            "end": f"{int(start_time[:2]) + (duration_minutes // 60):02d}:{int(start_time[3:]) + (duration_minutes % 60):02d}",
            "event": event_name
        }
        self.events.append(new_event)
        return json.dumps({"status": "success", "message": f"Added '{event_name}' to calendar.", "event": new_event})

class TaskTool:
    """
    MCP-style tool for Task List operations.
    """
    def __init__(self):
        self.tasks = []

    @trace_tool
    def read_tasklist(self):
        """Reads the current task list."""
        return json.dumps(self.tasks)

    @trace_tool
    def write_tasklist(self, tasks: list):
        """
        Overwrites the task list.
        Args:
            tasks: List of dicts [{"task": "name", "priority": "High", ...}]
        """
        self.tasks = tasks
        return json.dumps({"status": "success", "count": len(tasks)})
