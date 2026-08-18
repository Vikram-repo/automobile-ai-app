import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url=os.getenv("AZURE_OPENAI_ENDPOINT") + "/openai/v1/",
)

response = client.responses.create(
    model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
    input="Say hello in one short sentence."
)

print(response.output_text)
