import sqlite3

from langchain_core.tools import tool

DB_NAME = "memory/user_memory.db"


@tool
def recall_memory(question: str) -> str:
    """
    Retrieve previously saved user memories.

    Use this tool whenever the user asks:

    - What is my name?
    - Who am I?
    - What do you remember about me?
    - What is my experience?
    """

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("SELECT content FROM memories")

    rows = cursor.fetchall()

    conn.close()

    if not rows:
        return "No memories found."

    memories = "\n".join(row[0] for row in rows)

    return memories