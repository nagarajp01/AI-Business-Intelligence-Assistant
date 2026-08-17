from langchain_core.tools import tool
from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()

client=TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


@tool
def web_search(query:str)->str:
    """ Search the web for company, market, and competitor information """
    response=client.search(
        query=query,
        max_result=5
    )

    return str(response)