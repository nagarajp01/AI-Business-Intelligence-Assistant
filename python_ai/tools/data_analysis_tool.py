import pandas as pd
from langchain_core.tools import BaseTool
from agents.llm import load_llm
from langchain_core.prompts import PromptTemplate
from langchain_experimental.tools import PythonAstREPLTool
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

        if self.file_path.endswith(".xlsx"):
            df=pd.read_excel(self.file_path)
        elif self.file_path.endswith(".csv"):
            df=pd.read_csv(self.file_path)
        else :
            return "unsupported file"
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

        # final_prompt1=prompt.invoke({
        #     "question":question,
        #     "columns":list(df.columns)
        # })
        llm=load_llm()
        parser=StrOutputParser()
        # response=llm.invoke(final_prompt1)
        analysis_chain= prompt1 | llm | parser

        response=analysis_chain.invoke({
            "question":question,
            "columns":list(df.columns)
        })

        pythonTool=PythonAstREPLTool(
            locals={
                "df":df,
                "pd":pd
            }
        )

        # result=pythonTool.invoke(response.content)
        result=pythonTool.invoke(response)  #as parser is used it converts into string

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

        result_chain= prompt2 | llm | parser
        final_response=result_chain.invoke({
            "question":question,
            "result":result
        })

        # final_prompt2=second_prompt.invoke({
        #     "question":question,
        #     "result":result
        # })

        # final_response=llm.invoke(final_prompt2)

        # return final_response.content
        return final_response





        
