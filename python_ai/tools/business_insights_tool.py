from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from services.business_analysis_service import BusinessAnalysisService
from utils.report_generator import create_report


class BusinessInsightsInput(BaseModel):

    question: str = Field(
        description=(
            "The user's business analysis question. "
            "Use this to determine what business insights should be generated."
        )
    )

    generate_pdf: bool = Field(
        default=False,
        description=(
            "Set to True when the user explicitly asks for a PDF report, "
            "business report, or downloadable report. "
            "Otherwise set to False."
        )
    )


class BusinessInsightsTool(BaseTool):

    name: str = "Business_Insights_Tool"

    description: str = (
        "Generate business insights from uploaded CSV or Excel datasets. "
        "Use this tool when the user asks for sales intelligence, demand analysis, "
        "growth opportunities, business recommendations, or an overall business "
        "assessment based on uploaded data. "
        "The tool analyzes the actual dataset using Pandas and Python, "
        "uses forecasting information when required, and provides "
        "data-driven business insights and actionable recommendations. "
        "If the user asks for a PDF report, set generate_pdf to True. "
        "Do not invent or assume data that is not present in the dataset."
    )

    args_schema: type[BaseModel] = BusinessInsightsInput

    file_path: str

    output_path: str = "BusinessFileReport.pdf"

    def _run(
        self,
        question: str,
        generate_pdf: bool = False
    ):

        service = BusinessAnalysisService()

        # Step 1: Analyze the dataset
        analysis_result = service.analyze(
            self.file_path,
            question
        )

        # Step 2: Generate the natural-language business response
        final_response = service.generate_response(
            question,
            analysis_result
        )

        # Step 3: Generate PDF only when ReAct requested it
        pdf_path = None

        if generate_pdf:

            create_report(
                self.output_path,
                analysis_result
            )

            pdf_path = self.output_path

        # Step 4: Return the result to ReAct
        return {
            "analysis_result": analysis_result,
            "final_response": final_response,
            "pdf_path": pdf_path
        }





# from langchain_core.tools import BaseTool

# from services.business_analysis_service import BusinessAnalysisService


# class BusinessInsightsTool(BaseTool):

#     name: str = "Business_Insights_Tool"

#     description: str = (
#         "Generate business insights from uploaded CSV or Excel datasets. "
#         "Use this tool when the user asks for sales intelligence, demand analysis, "
#         "growth opportunities, business recommendations, or an overall business "
#         "assessment based on uploaded data. "
#         "The tool analyzes the actual dataset using Pandas and Python, "
#         "uses forecasting information when required, and provides "
#         "data-driven business insights and actionable recommendations. "
#         "Do not invent or assume data that is not present in the dataset."
#     )

#     file_path: str

#     def _run(self, question: str):

#         service = BusinessAnalysisService()

#         analysis_result = service.analyze(
#             self.file_path,
#             question
#         )

#         final_response = service.generate_response(
#             question,
#             analysis_result
#         )

#         return {
#             "analysis_result": analysis_result,
#             "final_response": final_response
#         }