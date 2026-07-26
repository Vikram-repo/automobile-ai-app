from deepagents import create_deep_agent

from llm.ollama import llm
from tools.internet_search import internet_search
from prompts.system_prompt import SYSTEM_PROMPT
from tools.calculator import calculator
from tools.datetime_tool import current_datetime
from tools.file_reader import read_text_file
from tools.save_memory import save_memory
from tools.recall_memory import recall_memory


agent = create_deep_agent(
    model=llm,
    tools=[internet_search,
           calculator,
           current_datetime,
           read_text_file,
           save_memory,
           recall_memory,
           ],
    system_prompt=SYSTEM_PROMPT,
)

