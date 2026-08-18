import sqlite3

from typing import Annotated

from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState
from langchain_core.runnables import RunnableConfig

DB_PATH = "memory/agent.db"


@tool
def save_memory(
    memory: str,
    state: Annotated[dict, InjectedState],
):
    """
    Save important user information.
    """

    user_id = state["user_id"]

    conn = sqlite3.connect(DB_PATH)

    conn.execute(
        "INSERT INTO memories(user_id,memory) VALUES(?,?)",
        (
            user_id,
            memory,
        ),
    )

    conn.commit()
    conn.close()

    return "Memory saved."


@tool
def recall_memory(
    state: Annotated[dict, InjectedState],
):
    """
    Recall user memories.
    """

    user_id = state["user_id"]

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.execute(
        "SELECT memory FROM memories WHERE user_id=?",
        (user_id,),
    )

    rows = cursor.fetchall()

    conn.close()

    if not rows:
        return "No memories found."

    return "\n".join(
        row[0]
        for row in rows
    )