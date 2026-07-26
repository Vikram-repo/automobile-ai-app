import sqlite3

from langchain_core.tools import tool

DB_NAME = "memory/user_memory.db"


@tool
def save_memory(text: str) -> str:
    
    """
    Save user information permanently for future conversations.

    Use this tool whenever the user says:
    - Remember this
    - Save this
    - Don't forget
    - Store this information

    """

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO memories (content) VALUES (?)",
        (text,)
    )

    conn.commit()
    conn.close()

    return f"Memory saved: {text}"