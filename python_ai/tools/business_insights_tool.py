from langchain_core.tools import BaseTool

from services.business_analysis_service import BusinessAnalysisService


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
        "Do not invent or assume data that is not present in the dataset."
    )

    file_path: str

    def _run(self, question: str):

        service = BusinessAnalysisService()

        analysis_result = service.analyze(
            self.file_path,
            question
        )

        final_response = service.generate_response(
            question,
            analysis_result
        )

        return final_response