from pathlib import Path
from langchain_core.tools import tool

@tool
def read_text_file(file_path: str) ->str:
    """
    Read the contents of a text file.
    """

    try:
        path = Path(file_path)

        if not path.exists():
            return f"File not found: {file_path}"

        return path.read_text(encoding="utf-8")

    except Exception as e:
        return str(e)