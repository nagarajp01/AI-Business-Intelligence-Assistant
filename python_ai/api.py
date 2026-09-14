from fastapi import FastAPI
from pydantic import BaseModel
from document_processors.document_processor import document_processor
from agents.react_agent import build_agent

app=FastAPI()

class QuestionRequest(BaseModel):
    question: str


file_path=input("Enter your pdf file path: ")
data_file_path=input("Enter you excel/csv file path: ")
retriever=document_processor(file_path)

agent=build_agent(
    retriever=retriever,
    data_file_path=data_file_path
)

@app.get("/")
def home():
    return {
        "message":"AI Business Intelligence API is running"
    }

@app.post("/ask")
def ask_question(request:QuestionRequest):
    response=agent.invoke({
        "messages":[
            {
                "role":"user",
                "content":request.question
            }
        ]
    })

    return {
        "answer":response["messages"][-1].content
    }