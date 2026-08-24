import pandas as pd

from langchain_core.tools import BaseTool
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from agents.llm import load_llm

from prophet import Prophet


class PredictionTool(BaseTool):

    name: str = "prediction_tool"

    description: str = (
        "Predict and forecast future values from uploaded CSV or Excel data. "
        "Use this tool when the user asks to predict, forecast, estimate "
        "future sales, revenue, profit, demand, quantity, or other numerical "
        "values from uploaded CSV or Excel data."
    )

    file_path: str

    def get_forecast(self, question: str):

        # Load uploaded CSV or Excel file
        if self.file_path.endswith(".xlsx"):
            df = pd.read_excel(self.file_path)

        elif self.file_path.endswith(".csv"):
            df = pd.read_csv(self.file_path)

        else:
            return "Unsupported file."

        # Get all available columns
        all_columns = list(df.columns)

        # Ask LLM to identify time and target columns
        prompt = PromptTemplate(
            template="""
You are a forecasting assistant.

The user wants to make a prediction:

{question}

The uploaded dataset contains these columns:

{columns}

Identify:

1. The column representing the time/date.
2. The column representing the value that should be predicted.

Return only the names of the two columns in this format:

time_column: <column name>
target_column: <column name>

Do not invent column names.
""",
            input_variables=["question", "columns"]
        )

        # Load LLM
        llm = load_llm()

        parser = StrOutputParser()

        prediction_chain = prompt | llm | parser

        # Ask LLM to identify the columns
        response = prediction_chain.invoke({
            "question": question,
            "columns": all_columns
        })

        # Convert response into lines
        lines = response.strip().splitlines()

        # Create variables for column names
        time_column = None
        target_column = None

        # Extract column names
        for line in lines:

            if line.startswith("time_column:"):
                time_column = line.split(":", 1)[1].strip()

            elif line.startswith("target_column:"):
                target_column = line.split(":", 1)[1].strip()

        # Validate the identified columns
        if time_column not in df.columns:
            return "Could not identify a valid time column."

        if target_column not in df.columns:
            return "Could not identify a valid target column."

        # Keep only the required columns
        forecast_df = df[
            [time_column, target_column]
        ].copy()

        # Convert time column to datetime
        forecast_df[time_column] = pd.to_datetime(
            forecast_df[time_column],
            errors="coerce"
        )

        # Remove invalid dates
        forecast_df = forecast_df.dropna(
            subset=[time_column]
        )

        # Convert target column to numeric
        forecast_df[target_column] = pd.to_numeric(
            forecast_df[target_column],
            errors="coerce"
        )

        # Remove invalid target values
        forecast_df = forecast_df.dropna(
            subset=[target_column]
        )

        # Sort data by date
        forecast_df = forecast_df.sort_values(
            by=time_column
        )

        # Combine duplicate dates
        forecast_df = forecast_df.groupby(
            time_column,
            as_index=False
        )[target_column].sum()

        # Check whether enough historical data exists
        if len(forecast_df) < 3:
            return "Not enough historical data for forecasting."

        # Detect data frequency
        frequency = pd.infer_freq(
            forecast_df[time_column]
        )

        # Calculate common date difference if frequency cannot be detected
        if frequency is None:

            date_differences = (
                forecast_df[time_column]
                .diff()
                .dropna()
            )

            if date_differences.empty:
                return "Could not determine the time frequency."

            common_difference = (
                date_differences.mode()[0]
            )

        else:

            common_difference = None

        # Convert data to Prophet format
        forecast_data = forecast_df.rename(
            columns={
                time_column: "ds",
                target_column: "y"
            }
        )

        # Create Prophet model
        model = Prophet()

        # Train Prophet
        model.fit(forecast_data)

        # Ask LLM for forecast duration
        horizon_prompt = PromptTemplate(
            template="""
You are a forecasting assistant.

User request:
{question}

Identify the forecast duration requested by the user.

Return ONLY these two lines:

periods: <number>
unit: <days, weeks, months, or years>

Examples:

"Predict the next 7 days of sales."

periods: 7
unit: days

"Forecast the next 3 weeks."

periods: 3
unit: weeks

"Forecast the next 6 months."

periods: 6
unit: months

"Forecast the next 2 years."

periods: 2
unit: years

If the user does not specify a duration:

periods: 7
unit: days
""",
            input_variables=[
                "question"
            ]
        )

        # # Determine a readable frequency unit
        # if frequency is not None:

        #     if frequency.startswith("D"):
        #         frequency_unit = "days"

        #     elif frequency.startswith("W"):
        #         frequency_unit = "weeks"

        #     elif frequency.startswith("M"):
        #         frequency_unit = "months"

        #     elif frequency.startswith("Y"):
        #         frequency_unit = "years"

        #     else:
        #         frequency_unit = "days"

        # else:

        #     if common_difference <= pd.Timedelta(days=1):
        #         frequency_unit = "days"

        #     elif common_difference <= pd.Timedelta(days=7):
        #         frequency_unit = "weeks"

        #     else:
        #         frequency_unit = "months"

        # Create horizon chain
        horizon_chain = (
            horizon_prompt
            | llm
            | parser
        )

        # Ask LLM for periods and unit
        horizon_response = horizon_chain.invoke({
            "question": question
        })

        # Convert horizon response into lines
        horizon_lines = (
            horizon_response
            .strip()
            .splitlines()
        )

        # Create variables for periods and unit
        periods = None
        unit = None

        # Extract periods and unit
        for line in horizon_lines:

            if line.startswith("periods:"):
                periods = int(
                    line.split(":", 1)[1].strip()
                )

            elif line.startswith("unit:"):
                unit = (
                    line
                    .split(":", 1)[1]
                    .strip()
                    .lower()
                )

        # Validate forecast duration
        if periods is None:
            return "Could not determine a valid forecast period."

        if periods <= 0:
            return "Forecast period must be greater than zero."

        if unit not in ["days", "weeks", "months", "years"]:
            return "Unsupported forecast time unit."

        # Convert unit into Prophet frequency
        if unit == "days":
            forecast_freq = "D"

        elif unit == "weeks":
            forecast_freq = "W"

        elif unit == "months":
            forecast_freq = "MS"

        elif unit == "years":
            forecast_freq = "YS"

        # Create future dates
        if frequency is not None:

            future = model.make_future_dataframe(
                periods=periods,
                freq=forecast_freq
            )

        else:

            last_date = forecast_data["ds"].max()

            if unit == "days":

                future_dates = pd.date_range(
                    start=last_date + pd.Timedelta(days=1),
                    periods=periods,
                    freq="D"
                )

            elif unit == "weeks":

                future_dates = pd.date_range(
                    start=last_date + pd.Timedelta(weeks=1),
                    periods=periods,
                    freq="W"
                )

            elif unit == "months":

                future_dates = pd.date_range(
                    start=last_date + pd.offsets.MonthBegin(1),
                    periods=periods,
                    freq="MS"
                )

            elif unit == "years":

                future_dates = pd.date_range(
                    start=last_date + pd.offsets.YearBegin(1),
                    periods=periods,
                    freq="YS"
                )

            future = pd.DataFrame({
                "ds": future_dates
            })

        # Generate predictions
        forecast = model.predict(future)

        # Get last historical date
        last_date = forecast_data["ds"].max()

        # Keep only future predictions
        future_forecast = forecast[
            forecast["ds"] > last_date
        ][
            ["ds", "yhat", "yhat_lower", "yhat_upper"]
        ]

        # Convert forecast DataFrame into structured records
        forecast_records = future_forecast.to_dict(
            orient="records"
        )

        # Return structured forecast
        return {
            "time_column": time_column,
            "target_column": target_column,
            "periods": periods,
            "unit": unit,
            "forecast": forecast_records
        }

    def _run(self, question: str):

        # Get structured forecast
        forecast_result = self.get_forecast(
            question
        )

        # Check whether forecasting failed
        if isinstance(forecast_result, str):
            return forecast_result

        # Load LLM
        llm = load_llm()

        parser = StrOutputParser()

        # Ask LLM to explain the structured forecast
        result_prompt = PromptTemplate(
            template="""
You are a business forecasting assistant.

The user asked:

{question}

The forecasting model produced these actual predictions:

{prediction_result}

Explain the forecast clearly to the user.

Rules:
1. Do not invent numbers.
2. Do not change the predicted values.
3. Clearly mention the predicted values.
4. Explain the forecast in simple business language.
5. Mention that these are model-based predictions, not guarantees.
6. Keep the answer concise.
""",
            input_variables=[
                "question",
                "prediction_result"
            ]
        )

        # Create final result chain
        result_chain = (
            result_prompt
            | llm
            | parser
        )

        # Generate final answer
        final_response = result_chain.invoke({
            "question": question,
            "prediction_result": forecast_result["forecast"]
        })

        # Return final answer
        return final_response