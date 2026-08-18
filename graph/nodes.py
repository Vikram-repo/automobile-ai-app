from llm.router import llm_with_fallback
from langchain_core.messages import SystemMessage

from graph.state import AgentState
from llm.ollama import llm_with_tools
from prompts.system_prompt import SYSTEM_PROMPT


def agent_node(state: AgentState):

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        *state["messages"],
    ]

    response = llm_with_fallback.invoke(messages)

    return {
        "messages": [response]
    }
