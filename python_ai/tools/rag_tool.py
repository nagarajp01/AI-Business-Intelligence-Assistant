from langchain_core.tools import BaseTool
from agents.rag_chain import create_rag_chain
from typing import Any
from pydantic import Field

class RAGTool(BaseTool):

    name:str="rag_tool"
    description:str=(
        "Answer questions using the content of the documents uploaded "
        "by the user, including PDFs, Word documents, annual reports, "
        "and business reports. "
        "Use this tool whenever the user asks about facts, definitions, "
        "products, customer segments, regions, financial information, "
        "or other content that may be contained in an uploaded document. "
        "For questions about the uploaded document, search the document "
        "rather than the public web. "
        "Do not use web search to answer questions about the uploaded "
        "document. If the answer is not found in the retrieved document "
        "content, state that the information could not be found in the "
        "uploaded document. Do not invent facts or use outside knowledge."
    )

    retriever: Any=Field(exclude=True)

    def _run (self,question:str):
        answer=create_rag_chain(
            self.retriever,
            question
        )

        return answer

    

