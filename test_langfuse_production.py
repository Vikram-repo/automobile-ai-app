from dotenv import load_dotenv
from langfuse import get_client

load_dotenv()

langfuse = get_client()

prompt = langfuse.get_prompt(
    "automobile-agent-system",
    label="production",
)

print("Production prompt fetched successfully")
print("Prompt name:", prompt.name)
print("Prompt version:", prompt.version)
print(prompt.prompt[:300])
