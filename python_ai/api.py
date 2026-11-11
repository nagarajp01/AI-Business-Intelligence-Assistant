from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse, FileResponse
from pathlib import Path
from pydantic import BaseModel
import uuid
import time
app=FastAPI()
workspaces = {}
#questionrequest-uses workspace
class QuestionRequest(BaseModel):
    question: str
    workspace_id:str

#processrequest-createsworkspace
class ProcessRequest(BaseModel):
    document_pdf:str
    excel_file:str

    # file_path:str
    # data_file_path:str



# file_path=input("Enter your pdf file path: ")
# data_file_path=input("Enter you excel/csv file path: ")
# retriever=document_processor(file_path)

# agent=build_agent(
#     retriever=retriever,
#     data_file_path=data_file_path
# )

#Creating the processing resources for a workspace.
def workspace_processing(document_pdf,excel_file):
    total_start = time.time()
    print("\n========== WORKSPACE PROCESSING ==========")
    print("\n1. Importing document processor...")
    start = time.time()
    from document_processors.document_processor import document_processor
    print(
        f"Document processor import: "
        f"{time.time() - start:.2f} seconds"
    )
    # 2. Import ReAct agent
    print("\n2. Importing ReAct agent...")
    start = time.time()
    from agents.react_agent import build_agent
    print(
        f"Agent import: "
        f"{time.time() - start:.2f} seconds"
    )
    # 3. Process PDF and create retriever
    print("\n3. Processing PDF and creating retriever...")
    start = time.time()

    file_path=document_pdf
    data_file_path=excel_file
    retriever=document_processor(file_path)
    print(
        f"PDF + RAG processing: "
        f"{time.time() - start:.2f} seconds"
    )
    # 4. Build ReAct agent
    print("\n4. Building ReAct agent...")
    start = time.time()

    agent=build_agent(
        retriever=retriever,
        data_file_path=data_file_path
    )
    print(
        f"Agent creation: "
        f"{time.time() - start:.2f} seconds"
    )
    # Total processing time
    print("\n==========================================")
    print(
        f"TOTAL PROCESSING TIME: "
        f"{time.time() - total_start:.2f} seconds"
    )
    print("==========================================\n")


    return agent

@app.get("/")
def home():
    return {
        "message":"AI Business Intelligence API is running"
    }


@app.post("/process")
def process(request: ProcessRequest):
    try:
        agent = workspace_processing(
            request.document_pdf,
            request.excel_file
        )

        workspace_id = str(uuid.uuid4())
        workspaces[workspace_id] = agent

        return {
            "workspace_id": workspace_id,
            "message": "Files processed successfully"
        }

    except Exception as error:
        print(f"Workspace processing failed: {error}")

        raise HTTPException(
            status_code=500,
            detail="Failed to process uploaded files."
        ) from error

# def process(request:ProcessRequest):
#     agent=workspace_processing(request.document_pdf,request.excel_file)
#     workspace_id = str(uuid.uuid4())
#     workspaces[workspace_id]=agent

#     return {
#         "workspace_id":workspace_id,
#         "message":"Files processed successfully"
#     }

# for message streaming ui,modifying it
async def stream_agent_response(agent, question, workspace_id):
    try:
        async for message_chunk, metadata in agent.astream(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": question
                    }
                ]
            },
            config={
                "configurable": {
                    "thread_id": workspace_id
                }
            },
            stream_mode="messages"
        ):

            if metadata.get("langgraph_node") == "agent":
                content = message_chunk.content

                if isinstance(content, str) and content:
                    yield content

    except Exception as error:
        print(f"Streaming failed: {error}")
        yield "\nSomething went wrong while generating the response. Please try again."

@app.post("/ask")
async def ask_question(request: QuestionRequest):

    agent = workspaces.get(request.workspace_id)

    if agent is None:
        raise HTTPException(
            status_code=404,
            detail="Workspace not found. Please upload your files again."
        )

    return StreamingResponse(
        stream_agent_response(
            agent,
            request.question,
            request.workspace_id
        ),
        media_type="text/plain"
    )

@app.get("/download-report/{workspace_id}")
def download_report(workspace_id: str):

    # Check whether the workspace exists
    if workspace_id not in workspaces:
        raise HTTPException(
            status_code=404,
            detail="Workspace not found."
        )

    # Locate the generated PDF
    pdf_path = Path.cwd() / "BusinessFileReport.pdf"

    if not pdf_path.exists():
        raise HTTPException(
            status_code=404,
            detail="PDF report not found. Generate the report first."
        )

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename="BusinessFileReport.pdf"
    )

# @app.post("/ask")
# def ask_question(request: QuestionRequest):
#     agent = workspaces.get(request.workspace_id)

#     if agent is None:
#         raise HTTPException(
#             status_code=404,
#             detail="Workspace not found. Please upload your files again."
#         )

#     try:
#         response = agent.invoke(
#             {
#                 "messages": [
#                     {
#                         "role": "user",
#                         "content": request.question
#                     }
#                 ]
#             },
#             config={
#                 "configurable": {
#                     "thread_id": request.workspace_id
#                 }
#             }
#         )

#         return {
#             "answer": response["messages"][-1].content
#         }

#     except Exception as error:
#         print(f"Question processing failed: {error}")

#         raise HTTPException(
#             status_code=500,
#             detail="Failed to process your question."
#         ) from error

