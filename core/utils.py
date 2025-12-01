import logging
import functools
import time
import streamlit as st

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("AgentOS")

class AgentLogger:
    """
    Singleton logger that captures events for both console and UI display.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AgentLogger, cls).__new__(cls)
            cls._instance.logs = []
        return cls._instance

    def log(self, level, message, details=None):
        timestamp = time.strftime("%H:%M:%S")
        entry = {
            "timestamp": timestamp,
            "level": level,
            "message": message,
            "details": details
        }
        self.logs.append(entry)

        # Also log to standard python logger
        if level == "INFO":
            logger.info(f"{message} | {details}")
        elif level == "ERROR":
            logger.error(f"{message} | {details}")
        elif level == "WARNING":
            logger.warning(f"{message} | {details}")

    def get_logs(self):
        return self.logs

    def clear(self):
        self.logs = []

def trace_agent(func):
    """Decorator to trace agent execution time and inputs/outputs."""
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        agent_name = getattr(self, 'name', 'Unknown Agent')
        AgentLogger().log("INFO", f"🤖 {agent_name} Started", {"args": str(args), "kwargs": str(kwargs)})
        start_time = time.time()
        try:
            result = func(self, *args, **kwargs)
            duration = round(time.time() - start_time, 2)
            AgentLogger().log("INFO", f"✅ {agent_name} Completed", {"duration": f"{duration}s", "result": str(result)[:200] + "..."})
            return result
        except Exception as e:
            duration = round(time.time() - start_time, 2)
            AgentLogger().log("ERROR", f"❌ {agent_name} Failed", {"duration": f"{duration}s", "error": str(e)})
            raise e
    return wrapper

def trace_tool(func):
    """Decorator to trace tool execution."""
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        tool_name = func.__name__
        AgentLogger().log("INFO", f"🛠️ Tool Call: {tool_name}", {"args": str(args), "kwargs": str(kwargs)})
        try:
            result = func(self, *args, **kwargs)
            AgentLogger().log("INFO", f"✅ Tool Success: {tool_name}", {"result": str(result)[:200] + "..."})
            return result
        except Exception as e:
            AgentLogger().log("ERROR", f"❌ Tool Failure: {tool_name}", {"error": str(e)})
            raise e
    return wrapper
