from langchain_core.tools import BaseTool

from utils.report_generator import create_report

class ReportGenerationTool(BaseTool):

    name:str="report_generation_tool"

    description: str = (
        "Generate a professional PDF business intelligence report "
        "from the structured analysis results of an uploaded dataset. "
        "Use this tool when the user asks to generate, create, export, "
        "or produce a PDF report containing business insights, sales "
        "intelligence, tables, charts, and sales forecasts. "
        "The report must be based only on the provided analysis results "
        "and must not invent or modify any data."
    )

    output_path:str


    def _run(self,analysis_result:dict):

        create_report(
            self.output_path,
            analysis_result

        )

        return (
            f"PDF GENERATED SUCCESSFULLY:  "
            f"{self.output_path}"

        )
