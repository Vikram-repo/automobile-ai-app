import os

from prompts.registry import get_system_prompt

PROMPT_VERSION = os.getenv("PROMPT_VERSION", "v1")

SYSTEM_PROMPT = get_system_prompt(PROMPT_VERSION)
