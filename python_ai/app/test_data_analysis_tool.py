from tools.data_analysis_tool import DataAnalysisTool

file_path = input("Enter your CSV/Excel file path: ")

tool = DataAnalysisTool(
    file_path=file_path
)

while True:

    question = input("\nEnter your question: ")

    if question.lower() == "exit":
        break

    result = tool.invoke(question)

    print("\nRESULT:\n")
    print(result)