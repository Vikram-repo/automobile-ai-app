from dotenv import load_dotenv
from langfuse import get_client

load_dotenv()

langfuse = get_client()

PROMPT_NAME = "automobile-agent-system"
PROMPT_LABEL = "production"

prompt = langfuse.get_prompt(
    PROMPT_NAME,
    label=PROMPT_LABEL,
)

SYSTEM_PROMPT = prompt.prompt
PROMPT_VERSION = prompt.version

print(
    f"Loaded prompt: {PROMPT_NAME} "
    f"version={PROMPT_VERSION} "
    f"label={PROMPT_LABEL}"
)
