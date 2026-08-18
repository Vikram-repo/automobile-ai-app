from dotenv import load_dotenv
from langfuse import get_client

load_dotenv()

langfuse = get_client()

prompt = langfuse.get_prompt(
    "automobile-agent-system",
    label="staging",
)

print("Prompt fetched successfully")
print("Prompt name:", prompt.name)
print("Prompt version:", prompt.version)
print("Prompt text:")
print(prompt.prompt)
