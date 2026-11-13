import traceback

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from services.business_analysis_service import BusinessAnalysisService


class BusinessInsightsInput(BaseModel):

    question: str = Field(
        description=(
            "The user's business question or analysis objective. "
            "Specify the business metrics, performance areas, trends, "
            "opportunities, problems, or recommendations to investigate "
            "using the uploaded dataset."
        )
    )

    generate_pdf: bool = Field(
        default=False,
        description=(
            "Set to True only when the user explicitly requests a PDF, "
            "downloadable business report, or a report file. "
            "Set to False for normal business analysis and conversational answers."
        )
    )


class BusinessInsightsTool(BaseTool):

    name: str = "Business_Insights_Tool"
    description: str = (
        "Perform comprehensive business analysis using the uploaded CSV "
        "or Excel dataset. "
        "Use this tool when the user requests an overall business assessment, "
        "sales intelligence, business performance evaluation, demand analysis, "
        "growth opportunities, problem identification, or strategic "
        "recommendations based on the dataset. "
        "Analyze the actual dataset and provide data-driven findings, "
        "business insights, and actionable recommendations. "
        "Use data_analysis_tool for individual calculations and "
        "prediction_tool for standalone future forecasting. "
        "This tool is intended for broader business analysis rather than "
        "isolated numerical questions. "
        "Set generate_pdf to True only when the user explicitly requests "
        "a PDF or downloadable report. "
        "Never invent data, figures, trends, or conclusions unsupported "
        "by the uploaded dataset."
    )

    args_schema: type[BaseModel] = BusinessInsightsInput

    file_path: str

    output_path: str = "BusinessFileReport.pdf"

    def _run(
        self,
        question: str,
        generate_pdf: bool = False
    ):

        try:
            service = BusinessAnalysisService()

            # Step 1: Analyze the dataset
            analysis_result = service.analyze(
                self.file_path,
                question
            )

            # Step 2: Validate analysis result
            if not isinstance(analysis_result, dict):
                return f"Business analysis failed: {analysis_result}"

            if "sales_metrics" not in analysis_result:
                return "Business analysis did not return sales metrics."

            # Step 3: Generate the natural-language business response
            final_response = service.generate_response(
                question,
                analysis_result
            )

            # Step 4: Generate PDF only when explicitly requested
            if generate_pdf:
                from utils.report_generator import create_report

                create_report(
                    self.output_path,
                    analysis_result
                )

                final_response += (
                    f"\n\nPDF report generated: {self.output_path}"
                )

            # Step 5: Return the result to the ReAct agent
            return final_response

        except Exception as error:
            traceback.print_exc()
            return f"Business analysis failed: {error}"