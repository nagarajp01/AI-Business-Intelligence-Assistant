from langchain_core.tools import tool
from tavily import TavilyClient
from dotenv import load_dotenv
import os


client=TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


@tool
def news_search(query:str)->str:
    """Search for recent company and market news
    """
    response=client.search(
        query=query,
        topic="news",
        max_result=5
    )

    return str(response)