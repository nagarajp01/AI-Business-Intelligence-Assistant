from langchain_core.tools import BaseTool
from agents.rag_chain import create_rag_chain
from typing import Any
from pydantic import Field

class RAGTool(BaseTool):

    name:str="rag_tool"
    description: str = (
        "Retrieve and answer questions using information from PDF documents "
        "uploaded by the user. "
        "Use this tool whenever the user asks about document-specific facts, "
        "figures, dates, definitions, products, customers, regions, financial "
        "information, findings, or summaries. "
        "For questions about uploaded PDF content, use this tool instead of "
        "web search or general knowledge. "
        "Base answers only on the retrieved document content. Do not invent "
        "facts or fill missing information using assumptions or external knowledge. "
        "If the answer is not found, clearly state that the information could "
        "not be found in the uploaded document."
    )


    retriever: Any=Field(exclude=True)

    def _run (self,question:str):
        answer=create_rag_chain(
            self.retriever,
            question
        )

        return answer

    

