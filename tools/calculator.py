from langchain_core.tools import tool


@tool
def calculator(expression: str) -> str:
    """
    Evaluate a mathematical expression.
    Example: 2+3*5
    """
    try:
        return str(eval(expression))
    except Exception as e:
        return str(e)