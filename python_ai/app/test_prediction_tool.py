from tools.prediction_tool import PredictionTool


file_path = "./../docs/Business_Sales_Forecasting_Test_Data.xlsx"

prediction_tool = PredictionTool(
    file_path=file_path
)


while True:

    question = input("\nEnter your question: ")

    if question.lower() == "exit":
        print("Exiting...")
        break

    result = prediction_tool.run(question)

    print("\nRESULT:\n")
    print(result)