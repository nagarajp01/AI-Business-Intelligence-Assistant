from langchain_core.tools import tool
from tavily import TavilyClient
from dotenv import load_dotenv
import os


client=TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


@tool
def news_search(query:str)->str:
    """
    Search for recent news and current developments.

    Use this tool when the user asks for the latest news, recent
    announcements, company updates, market developments, industry
    news, business events, or recent competitor activities.

    Focus on recent information relevant to the user's query.
    Prefer dated news reports and reliable sources.

    Use web_search for general web research and rag_tool for
    information contained in uploaded documents.

    Do not invent news, dates, events, or claims. Base answers
    on the retrieved news search results.
    """
    response=client.search(
        query=query,
        topic="news",
        max_result=5
    )

    return str(response)