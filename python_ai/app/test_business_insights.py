from tools.business_insights_tool import BusinessInsightsTool


data_file_path = "./../docs/Business_Sales_Forecasting_Test_Data.xlsx"

business_insights_tool = BusinessInsightsTool(
    file_path=data_file_path
)


while True:

    question = input("\nEnter your question (or type 'exit' to quit): ")

    if question.lower() == "exit":
        break

    result = business_insights_tool.invoke(
        question
    )

    print("\nBUSINESS INSIGHTS:\n")
    print(result)