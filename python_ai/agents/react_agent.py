from langgraph.prebuilt import create_react_agent
# from langchain.agents import create_agent
# from langchain import hub
from agents.llm import load_llm
from tools.rag_tool import RAGTool
from tools.web_tool import web_search
from tools.news_tool import news_search
# from document_processors.document_processor import document_processor

def build_agent(retriever):
    rag_tool=RAGTool(
        retriever=retriever
    )

    llm=load_llm()

    # prompt=hub.pull("hwchase17/react")

    system_prompt = """
You are an AI Business Intelligence and Research Assistant.

STRICT TOOL-SELECTION RULES — FOLLOW ALWAYS:

1. If the user asks about information contained in an uploaded
   document, report, PDF, Excel, CSV, Word document, or internal
   company data, use rag_tool first.

2. If the user explicitly asks "according to the uploaded report",
   "according to the document", or similar wording, ONLY use
   rag_tool for that information.
   Do NOT use web_search or news_search to fill missing information.
   If rag_tool cannot find the information, clearly say that the
   information is not available in the uploaded document.

3. If the user asks for current external information, competitors,
   market trends, company research, industry information, or other
   information that is not necessarily contained in the uploaded
   documents, use web_search.

4. If the user asks for latest, recent, current, today's, or breaking
   news, use news_search.

5. For a request requiring multiple types of information, you may
   use multiple tools. For example:
   - financial information from uploaded reports → rag_tool
   - competitors → web_search
   - latest developments → news_search

6. NEVER answer a document-specific question from memory when
   rag_tool is available.

7. NEVER invent, speculate, or fabricate information.

8. If the required information cannot be found using the appropriate
   tool, clearly state that the information is unavailable.

9. After receiving tool results, synthesize them into one clear,
   accurate and useful answer.

10. When possible, mention the source used, such as:
    - Uploaded document
    - Web research
    - Recent news

AVAILABLE TOOLS:

rag_tool:
Searches and retrieves information from uploaded business documents.

web_search:
Searches the web for external company, competitor, market,
industry, and business information.

news_search:
Searches for recent and current news.

IMPORTANT:
Do not use a different tool simply because the first tool did not
produce the desired answer. Respect the user's requested source.
"""

    agent=create_react_agent(
        model=llm,
        tools=[rag_tool,web_search,news_search],
        prompt=system_prompt
    )

    # agent=create_agent(
    #     model=llm,
    #     tools=[rag_tool,web_search,news_search],
    # )

    return agent

    # agent_executor=AgentExecutor(
    #     agent=agent,
    #     tools=[rag_tool,web_search,news_search],
    #     verbose=True
    # )

    # return agent_executor