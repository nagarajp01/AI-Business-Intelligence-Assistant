import re
import json
import pandas as pd
from agents.llm import load_llm
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import numpy as np


class BusinessAnalysisService:

    # ------------------------------------------------------------------
    # Main analysis function
    # ------------------------------------------------------------------
    def analyze(self, file_path: str, question: str):

        # Load dataset
        if file_path.endswith(".xlsx"):
            df = pd.read_excel(file_path)
        elif file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
        else:
            return "Unsupported file"

        columns = list(df.columns)

        llm = load_llm()
        parser = StrOutputParser()

        # Identify relevant columns
        prompt1 = PromptTemplate(
            template="""
You are a Sales Intelligence data analysis assistant.

The user wants business insights from an uploaded dataset.

User request:
{question}

The uploaded dataset contains these columns:
{columns}

Identify the columns that are relevant for calculating Sales Intelligence metrics.

Look for columns representing concepts such as:
- date or time
- sales or revenue
- profit
- product
- region
- quantity
- customer
- other business dimensions that may be useful for sales analysis

Only select columns that actually exist in the provided dataset.

Return ONLY a comma-separated list of the relevant column names.

Do not invent column names.
Do not include explanations.
""",
            input_variables=["question", "columns"]
        )

        column_chain = prompt1 | llm | parser

        raw_columns = column_chain.invoke({
            "question": question,
            "columns": columns
        })

        # Keep only valid columns instead of failing the whole analysis
        columns_identified = [
            column.strip().strip("'\"[]")
            for column in raw_columns.split(",")
        ]
        columns_identified = [
            column for column in columns_identified
            if column in columns
        ]

        # Fall back to all columns if the LLM returned nothing valid
        if not columns_identified:
            columns_identified = columns

        # Generate Pandas code
        pandas_code = self.generate_pandas_code(
            question=question,
            columns=columns,
            columns_identified=columns_identified,
            llm=llm,
            parser=parser
        )
        # print("GENERATED CODE:\n", pandas_code)

        # Execute generated Pandas code
        sales_metrics = self.execute_pandas_code(
            pandas_code=pandas_code,
            df=df
        )
        # print("EXEC RESULT:", sales_metrics)

        # If execution fails, ask the LLM to correct the code (up to 3 times)
        if not isinstance(sales_metrics, dict):

            correction_prompt = PromptTemplate(
                template="""
You are a Python debugging assistant.

The following Python code was generated to analyze a Pandas DataFrame.

Generated code:
{pandas_code}

The code failed during execution.

Execution result or error:
{execution_error}

The available DataFrame columns are:
{columns}

The user asked:
{question}

Correct the Python code.

Rules:

1. Use the existing DataFrame named `df`.
2. Do not load the file again.
3. Do not create fake or sample data.
4. Use only columns that actually exist in the DataFrame.
5. Perform the actual calculations using Pandas.
6. Convert date columns with pd.to_datetime(..., errors="coerce").
7. Create a variable named `sales_metrics`.
8. `sales_metrics` MUST contain a Python dictionary with plain
   Python values (use float(), int(), and .to_dict()).
9. Return ONLY executable Python code.
10. Do not include Markdown code fences.
11. Do not explain the code.
""",
                input_variables=[
                    "pandas_code",
                    "execution_error",
                    "columns",
                    "question"
                ]
            )

            correction_chain = correction_prompt | llm | parser

            for attempt in range(3):

                if isinstance(sales_metrics, dict):
                    break

                pandas_code = correction_chain.invoke({
                    "pandas_code": pandas_code,
                    "execution_error": sales_metrics,
                    "columns": columns,
                    "question": question
                })

                sales_metrics = self.execute_pandas_code(
                    pandas_code=pandas_code,
                    df=df
                )
                # print(f"RETRY {attempt + 1} RESULT:", sales_metrics)

        # Final validation (return text instead of raising,
        # so the agent does not crash)
        if not isinstance(sales_metrics, dict):
            return (
                "Sales analysis failed after retries. "
                f"Last error: {sales_metrics}"
            )

        # Return complete analysis result
        return {
            "sales_metrics": sales_metrics,
        }

    # ------------------------------------------------------------------
    # Generate Pandas code
    # ------------------------------------------------------------------
    def generate_pandas_code(
        self,
        question,
        columns,
        columns_identified,
        llm,
        parser
    ):

        prompt2 = PromptTemplate(
            template="""
You are a Python data analysis assistant.

You have access to a Pandas DataFrame named `df`.

The user asks:
{question}

The dataset has these columns:
{columns}

The columns identified as relevant for Sales Intelligence are:
{llm_columns}

Generate Python code using Pandas to calculate the Sales Intelligence metrics
that can be determined from the available data.

Rules:

1. Use the existing DataFrame `df`.
2. Do not create fake or sample data.
3. Do not load the file again.
4. Perform the actual calculations using Pandas.
5. Use only columns listed in `llm_columns`.
6. Only calculate metrics that are possible from the available columns.
7. Return only executable Python code.
8. Do not include Markdown code fences.
9. Do not explain the code.
10. Create a Python variable named `sales_metrics`.
11. `sales_metrics` MUST contain a Python dictionary.
12. Use clear metric names as dictionary keys.
13. Convert numpy/pandas values to plain Python values
    (use float(), int(), and .to_dict()).
14. Convert date columns with pd.to_datetime(..., errors="coerce").
15. If calculating growth rate, calculate the growth from the first
recorded date to the last recorded date:

((last sales - first sales) / first sales) * 100

16. Use the metric name:

first_to_last_day_growth_rate

17. Do not call this simply "growth rate".
""",
            input_variables=[
                "question",
                "columns",
                "llm_columns"
            ]
        )

        pandas_chain = prompt2 | llm | parser

        pandas_code = pandas_chain.invoke({
            "question": question,
            "columns": columns,
            "llm_columns": columns_identified
        })

        return pandas_code

    # ------------------------------------------------------------------
    # Clean LLM code (remove markdown fences)
    # ------------------------------------------------------------------
    def clean_code(self, code: str) -> str:
        code = code.strip()
        match = re.search(r"```(?:python)?\s*(.*?)```", code, re.DOTALL)
        if match:
            code = match.group(1)
        return code.strip()

    # ------------------------------------------------------------------
    # Execute Pandas code
    # ------------------------------------------------------------------
    def execute_pandas_code(self, pandas_code, df):

        code = self.clean_code(pandas_code)

        # Workspace the generated code runs in
        namespace = {
            "df": df.copy(),
            "pd": pd,
            "np": np
        }

        try:
            exec(code, namespace)
        except Exception as error:
            # print(f"Pandas execution error: {error}")
            return f"Execution error: {type(error).__name__}: {error}"

        sales_metrics = namespace.get("sales_metrics")

        if isinstance(sales_metrics, dict):
            return sales_metrics

        return "Code ran but `sales_metrics` is not a dictionary."

    # ------------------------------------------------------------------
    # Generate final natural-language response
    # ------------------------------------------------------------------
    def generate_response(
        self,
        question: str,
        analysis_result
    ):

        if isinstance(analysis_result, str):
            return analysis_result

        if not isinstance(analysis_result, dict):
            raise ValueError("Invalid business analysis result.")

        if "sales_metrics" not in analysis_result:
            raise ValueError("Sales metrics are missing.")

        llm = load_llm()
        parser = StrOutputParser()

        final_prompt = PromptTemplate(
            template="""
You are an AI Business Intelligence assistant.

The user asked:
{question}

The actual historical Sales Intelligence metrics calculated
from the uploaded dataset are:
{sales_metrics}

Using ONLY the provided calculated metrics, generate a
clear business analysis with the following sections:

1. Sales Intelligence
- Present the important historical sales metrics.
- Mention the strongest and weakest available products,
  regions, or other business dimensions.
- Do not invent metrics that were not calculated.

2. Business Performance
- Analyze historical business performance.
- Identify important patterns and comparisons visible
  in the calculated metrics.
- Do not invent causes for changes.

3. Growth Opportunities
- Identify areas showing strong performance.
- Identify products, regions, or other dimensions that
  may represent opportunities for growth.
- Base observations only on the provided data.

4. Business Recommendations
- Provide practical recommendations based on actual metrics.
- Do not invent business facts or external information.
- Recommend investigating or improving weak-performing
  areas rather than assuming their underlying causes.

Rules:

1. Use only the provided historical Sales Intelligence metrics.
2. Do not invent or change any numbers.
3. Do not assume information that is not present.
4. If a metric is unavailable, do not fabricate it.
5. Clearly distinguish revenue, quantities, percentages,
   and other measurements.
6. Keep the response concise but useful.
7. Use clear headings and bullet points.
8. Do not mention customer satisfaction, product quality,
   market demand, or other factors unless present in the data.
9. Clearly state the metric used when identifying the best
   or worst product, region, or other business dimension.
10. If the data does not contain enough information to answer
    a question, say that the required metric is unavailable.
11. Every factual statement must be supported by the
    provided sales_metrics.

""",
            input_variables=[
                "question",
                "sales_metrics"
            ]
        )

        final_chain = final_prompt | llm | parser

        final_response = final_chain.invoke({
            "question": question,
            "sales_metrics": json.dumps(
                analysis_result["sales_metrics"],
                default=str,
                indent=2
            ),
        })

        return final_response