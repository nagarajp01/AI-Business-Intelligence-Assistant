import traceback

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from utils.email_sender import send_email


class SendEmailInput(BaseModel):
    subject: str = Field(
        description=(
            "A clear and relevant subject line for the email. "
            "Summarize the main business insight, finding, or notification."
        )
    )
    message: str = Field(
        description=(
            "The complete email body containing the important business "
            "insights, significant findings, results, or actionable "
            "recommendations to communicate. Use clear and professional language."
        )
    )


class SendEmailTool(BaseTool):

    name: str = "send_email_tool"
    description: str = (
        "Send an email notification containing important business insights, "
        "significant findings, analysis results, or actionable recommendations. "
        "Use this tool when the user explicitly requests an email or when "
        "the agent is instructed by the application workflow to send an "
        "important business notification. "
        "Prepare a meaningful subject and a clear, complete email message. "
        "Do not send unnecessary or empty notifications. "
        "Do not claim that an email was sent unless this tool executes successfully."
    )

    args_schema: type[BaseModel] = SendEmailInput

    def _run(self, subject: str, message: str):

        try:
            send_email(subject, message)
            return "Email sent successfully."

        except Exception as error:
            traceback.print_exc()
            return f"Email failed to send: {error}"