from langchain.agents import create_react_agent,AgentExecutor
from langchain import hub
from agents.llm import load_llm
from tools.rag_tool import RAGTool
from tools.web_tool import web_search
from tools.news_tool import news_search
# from document_processors.document_processor import document_processor

def create_agent(retriever):
    rag_tool=RAGTool(
        retriever=retriever
    )

    llm=load_llm()

    prompt=hub.pull("hwchase17/react")

    agent=create_react_agent(
        llm=llm,
        tools=[rag_tool,web_search,news_search],
        prompt=prompt
    )

    agent_executor=AgentExecutor(
        agent=agent,
        tools=[rag_tool,web_search,news_search],
        verbose=True
    )

    return agent_executor