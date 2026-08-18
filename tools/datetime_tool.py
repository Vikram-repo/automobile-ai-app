from langchain_core.tools import tool
from datetime import datetime


@tool
def current_datetime() -> str:
    """
    Returns current date and time.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
