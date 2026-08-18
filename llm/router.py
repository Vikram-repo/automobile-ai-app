from llm.ollama import llm_with_tools
from llm.foundry import foundry_llm_with_tools
from llm.fallback import LLMFallback


llm_with_fallback = LLMFallback(
    primary=llm_with_tools,
    fallback=foundry_llm_with_tools,
    max_retries=1,
)
