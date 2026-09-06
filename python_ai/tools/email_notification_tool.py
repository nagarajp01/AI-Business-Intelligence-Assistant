from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from utils.email_sender import send_email


class SendEmailInput(BaseModel):
    # recipient: str = Field(description="Email address of the recipient")
    subject: str = Field(description="Subject of the email")
    message: str = Field(description="Content of the email")


class SendEmailTool(BaseTool):

    name:str="send_email_tool"

    description: str = (
    "Send an email notification when important business insights, "
    "significant findings, or actionable recommendations from the "
    "Business Insights Tool need to be communicated to the user."
    )

    args_schema:type[BaseModel]=SendEmailInput

    def _run(self,subject,message):
        send_email(subject,message)
        return "Email sent successfully."



