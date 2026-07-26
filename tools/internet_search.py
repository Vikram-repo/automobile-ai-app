from ddgs import DDGS
from langchain_core.tools import tool




@tool
def internet_search(query: str) -> str:
    """
    Search internet.
    """

    results = DDGS().text(query, max_results=5)

    return "\n\n".join(
        f"{r['title']}\n{r['href']}\n{r['body']}"
        for r in results
    )
