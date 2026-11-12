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
    """
    Search the public web for external information and research.

    Use this tool when the user asks for company profiles, competitor
    analysis, market research, industry trends, products, services,
    business information, or external facts that require web sources.

    Use specific search queries relevant to the user's question.
    Do not use this tool as the primary source for questions about
    uploaded documents; use rag_tool instead.
    For recent news and current events, use news_search.

    Base answers on the retrieved search results and do not invent
    facts or present unsupported information as verified.
    """
    response=client.search(
        query=query,
        max_result=5
    )

    return str(response)