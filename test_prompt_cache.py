import os

from dotenv import load_dotenv
from openai import OpenAI

from prompts.system_prompt import SYSTEM_PROMPT, PROMPT_VERSION


load_dotenv()


# ---------------------------------------------------------
# Azure OpenAI / Foundry client
# ---------------------------------------------------------

client = OpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url=os.getenv("AZURE_OPENAI_ENDPOINT") + "/openai/v1/",
)

deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")


# ---------------------------------------------------------
# Langfuse production prompt
# ---------------------------------------------------------

# Langfuse returns:
#
# [
#     {
#         "type": "message",
#         "role": "system",
#         "content": "..."
#     }
# ]
#
# We only need the actual system prompt text.

system_prompt = SYSTEM_PROMPT[0]["content"]


print("=" * 70)
print("PROMPT CACHE TEST")
print("=" * 70)

print(f"Prompt name       : automobile-agent-system")
print(f"Prompt version    : {PROMPT_VERSION}")
print(f"Prompt label      : production")
print(f"Deployment        : {deployment}")
print(f"Prompt characters : {len(system_prompt)}")
print(f"Prompt words      : {len(system_prompt.split())}")

print("=" * 70)


# ---------------------------------------------------------
# Model call
# ---------------------------------------------------------

def call_model(request_number, user_message):

    print(f"\n{'=' * 25} REQUEST {request_number} {'=' * 25}")

    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_message,
            },
        ],
        temperature=0,
    )

    # -----------------------------------------------------
    # Response
    # -----------------------------------------------------

    print("\nResponse:")
    print(response.choices[0].message.content)

    # -----------------------------------------------------
    # Usage
    # -----------------------------------------------------

    print("\nUsage:")
    print(response.usage)

    # -----------------------------------------------------
    # Prompt cache details
    # -----------------------------------------------------

    prompt_details = getattr(
        response.usage,
        "prompt_tokens_details",
        None,
    )

    print("\nPrompt token details:")

    if prompt_details:
        print(prompt_details)

        cached_tokens = getattr(
            prompt_details,
            "cached_tokens",
            0,
        )

        cache_write_tokens = getattr(
            prompt_details,
            "cache_write_tokens",
            None,
        )

        print(f"\nCached tokens      : {cached_tokens}")
        print(f"Cache write tokens : {cache_write_tokens}")

    else:
        print("Prompt cache details not returned.")

    return response


# ---------------------------------------------------------
# Request 1
# ---------------------------------------------------------

call_model(
    1,
    "What is the automobile policy?",
)


# ---------------------------------------------------------
# Request 2
# ---------------------------------------------------------

call_model(
    2,
    "What is the warranty policy?",
)


# ---------------------------------------------------------
# Request 3
# ---------------------------------------------------------

call_model(
    3,
    "How should an engineer handle a production machine repair?",
)


print("\n")
print("=" * 70)
print("PROMPT CACHE TEST COMPLETED")
print("=" * 70)
