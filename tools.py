class CalendarTool:
    def __init__(self):
        # Mock existing conflicts
        self.conflicts = [
            {"start": "13:00", "end": "14:00", "event": "Team Sync"},
            {"start": "16:00", "end": "16:30", "event": "Coffee Chat"}
        ]

    def check_availability(self, start_time, duration_minutes):
        """
        Mock check. In a real app, this would check Google Calendar.
        Returns True if available, False (and reason) if conflict.
        """
        # Simple string comparison for mock purposes (assuming HH:MM format)
        # Real implementation would use datetime objects

        # For this mock, we'll just return the list of conflicts so the agent knows what to avoid
        return f"Existing Conflicts: {self.conflicts}"

    def schedule_task(self, task_name, start_time, duration_minutes):
        """
        Mock scheduling.
        """
        # In a real app, this would write to the calendar.
        return f"Scheduled '{task_name}' at {start_time} for {duration_minutes} mins."
