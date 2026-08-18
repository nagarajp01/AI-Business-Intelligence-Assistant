from langchain_core.tools import BaseTool
from agents.rag_chain import create_rag_chain
from typing import Any
from pydantic import Field

class RAGTool(BaseTool):

    name:str="rag_tool"
    description:str=(
        "Answer questions from uploaded documents"
    )

    retriever: Any=Field(exclude=True)

    def _run (self,question:str):
        answer=create_rag_chain(
            self.retriever,
            question
        )

        return answer

    

