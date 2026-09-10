from tools.business_insights_tool import BusinessInsightsTool
from services.business_analysis_service import BusinessAnalysisService
from utils.report_generator import create_report,find_chart_data



data_file_path = "./../docs/Business_Sales_Forecasting_Test_Data.xlsx"

business_insights_tool = BusinessInsightsTool(
    file_path=data_file_path
)

service = BusinessAnalysisService()


while True:

    question = input("\nEnter your question (or type 'exit' to quit): ")

    if question.lower() == "exit":
        break

    analysis_result = service.analyze(
        data_file_path,
        question
    )
    print("\nSTRUCTURED BUSINESS ANALYSIS:\n")
    print(analysis_result)

    if isinstance(analysis_result, str):
        continue

    result = service.generate_response(
        question,
        analysis_result
    )

    print("\nBUSINESS INSIGHTS:\n")
    print(result)

    chart_data=find_chart_data(
        analysis_result["sales_metrics"]
    )
    print("\nCHART DATA:\n")
    print(chart_data)

    create_report(
        "finalBusinessReport.pdf",
        analysis_result
    )
    print("\nPDF REPORT GENERATED: businesssample_report.pdf")


    