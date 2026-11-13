from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse, FileResponse
import tempfile
from pathlib import Path
from pydantic import BaseModel
from typing import Optional
import uuid


app=FastAPI()
workspaces = {}

class QuestionRequest(BaseModel):
    question: str
    workspace_id:str

#Creating the processing resources for a workspace
def workspace_processing(document_pdf,excel_file,workspace_id):
    from agents.react_agent import build_agent
    retriever=None
    if document_pdf:
         from document_processors.document_processor import document_processor
         retriever = document_processor(
            document_pdf,
            collection_name=workspace_id
            )
    agent=build_agent(
        retriever=retriever,
        data_file_path=excel_file
        )
    return agent

@app.get("/")
def home():
    return {
        "message":"AI Business Intelligence API is running"
    }


@app.post("/process")
async def process(
    document_pdf: Optional[UploadFile] = File(None),
    excel_file: Optional[UploadFile] = File(None)
):
    try:
        if not document_pdf and not excel_file:
            raise HTTPException(
                status_code=400,
                detail="Please upload at least one file"
            )

        workspace_id = str(uuid.uuid4())

        # Create a separate temporary folder for this workspace
        workspace_dir = Path(
            tempfile.mkdtemp(prefix=f"workspace_{workspace_id}_")
        )

        pdf_path = None
        excel_path = None

        # Save uploaded PDF
        if document_pdf:
            if Path(document_pdf.filename or "").suffix.lower() != ".pdf":
                raise HTTPException(
                    status_code=400,
                    detail="Please upload a valid PDF file."
                )

            pdf_path = workspace_dir / "document.pdf"
            pdf_path.write_bytes(await document_pdf.read())

        # Save uploaded Excel/CSV file
        if excel_file:
            extension = Path(excel_file.filename or "").suffix.lower()

            if extension not in [".xlsx", ".csv"]:
                raise HTTPException(
                    status_code=400,
                    detail="Only XLSX and CSV files are supported."
                )

            excel_path = workspace_dir / f"dataset{extension}"
            excel_path.write_bytes(await excel_file.read())

        # Build the agent using the saved file paths
        agent = workspace_processing(
            str(pdf_path) if pdf_path else None,
            str(excel_path) if excel_path else None,
            workspace_id
        )

        workspaces[workspace_id] = agent

        return {
            "workspace_id": workspace_id,
            "message": "Files processed successfully"
        }

    except HTTPException:
        raise

    except Exception as error:
        print(f"Workspace processing failed: {error}")

        raise HTTPException(
            status_code=500,
            detail="Failed to process uploaded files."
        ) from error
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

