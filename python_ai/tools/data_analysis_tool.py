import pandas as pd
from langchain_core.tools import BaseTool
from agents.llm import load_llm
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


class DataAnalysisTool(BaseTool):

    name: str = "data_analysis_tool"
    description: str = (
        "Analyze uploaded CSV or Excel datasets using Pandas and Python. "
        "Use this tool when the user requests numerical calculations, "
        "aggregations, filtering, grouping, sorting, statistical analysis, "
        "historical trends, or comparisons based on the uploaded data. "
        "It handles totals, averages, counts, percentages, minimums, maximums, "
        "rankings, revenue, sales, profit, quantities, and comparisons across "
        "products, regions, customers, dates, or other available columns. "
        "Use the actual dataset for every calculation and never invent or "
        "assume values. Use prediction_tool for standalone future forecasting "
        "and Business_Insights_Tool for comprehensive business analysis "
        "and strategic recommendations."
        )
    file_path: str
    
    def _run(self,question:str):
        try:
            if self.file_path.lower().endswith(".xlsx"):
                df=pd.read_excel(self.file_path)
            elif self.file_path.lower().endswith(".csv"):
                df=pd.read_csv(self.file_path)
            else :
                return "Unsupported file format. Please upload a CSV or XLSX file."
        except Exception as error:
            return f"Could not read the uploaded file: {error}"
        # Step 2: Validate the dataset
        if df.empty:
            return "The uploaded dataset is empty. Please upload a file containing data."

        # Step 3: Generate Pandas code using the LLM
        
        prompt1=PromptTemplate(
            template="""You are a Python data analysis assistant.
            You have access to a Pandas DataFrame named `df`.
            The user asks:
            {question}
            The dataset has these columns:
            {columns}
            Generate Python code using Pandas to answer the user's question.
            Rules:
            1. Use the existing DataFrame `df`.
            2. Do not create fake or sample data.
            3. Do not load the file again.
            4. Perform the actual calculation using Pandas.
            5. Use only the columns that exist in `df`.
            6. Return only executable Python code.
            7. Do not include Markdown code fences.
            8. Do not explain the code.
            9. The final expression should produce the answer/result.""",
            input_variables=["question","columns"]
        )
        try:
            llm=load_llm()
            parser=StrOutputParser()
            analysis_chain= prompt1 | llm | parser
            response=analysis_chain.invoke({
                "question":question,
                "columns":list(df.columns)
                })
            if not response or not response.strip():
                return "The AI could not generate analysis code. Please try again."

        except Exception as error:
            return f"Could not generate analysis code: {error}"
        # Step 4: Execute the generated Python code
        try:
            from langchain_experimental.tools import PythonAstREPLTool
            pythonTool=PythonAstREPLTool(
                locals={
                "df":df,
                "pd":pd
                }
                )
            result=pythonTool.invoke(response)
            if result is None or not str(result).strip():
                return "The analysis did not produce a result. Please try a different question."
        except Exception as error:
            return f"Data analysis execution failed: {error}"
        # Step 5: Generate a natural-language explanation
        prompt2=PromptTemplate(
            template="""
            The user asked: {question}
            The Python analysis produced this actual result:
            {result}
            Explain this result clearly to the user.
            Do not invent or change any numbers.
            Give a concise business-oriented answer.
            """,
            input_variables=["question","result"]
        )
        try:
            result_chain= prompt2 | llm | parser
            final_response=result_chain.invoke({
                "question":question,
                "result":result
            })
            if not final_response or not final_response.strip():
                return f"Analysis completed, but the explanation could not be generated. Result: {result}"
            return final_response
        except Exception as error:
            return f"Analysis completed, but explanation generation failed: {error}.Result: {result}"






        
