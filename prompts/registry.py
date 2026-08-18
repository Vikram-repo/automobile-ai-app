from prompts.v2.system_prompt import SYSTEM_PROMPT as SYSTEM_PROMPT_V2
from prompts.v1.system_prompt import SYSTEM_PROMPT as SYSTEM_PROMPT_V1


PROMPT_REGISTRY = {
    "v1": SYSTEM_PROMPT_V1,
    "v2": SYSTEM_PROMPT_V2,
}


def get_system_prompt(version: str) -> str:
    try:
        return PROMPT_REGISTRY[version]
    except KeyError:
        raise ValueError(
            f"Unsupported prompt version: {version}"
        )
