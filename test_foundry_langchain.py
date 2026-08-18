from llm.foundry import foundry_llm_with_tools

response = foundry_llm_with_tools.invoke(
    "Hello. Explain in one sentence what an automobile insurance policy is."
)

print(response.content)
