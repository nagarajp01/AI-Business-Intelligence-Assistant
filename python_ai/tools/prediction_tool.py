import traceback

import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from langchain_core.tools import BaseTool
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from agents.llm import load_llm


class PredictionTool(BaseTool):

    name: str = "prediction_tool"
    description: str = (
        "Generate forecasts and predict future numerical values using an "
        "uploaded CSV or Excel dataset. "
        "Use this tool whenever the user explicitly asks to predict, forecast, "
        "estimate, or project future values such as sales, revenue, profit, "
        "demand, quantity, or other numerical metrics. "
        "Use historical data to generate model-based predictions. "
        "Identify the relevant date column and target column from the dataset. "
        "Use the requested forecast duration or default to 7 days. "
        "Do not invent historical data or predicted values. "
        "Use data_analysis_tool for historical calculations and "
        "Business_Insights_Tool for comprehensive business analysis."
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

        all_columns = list(df.columns)

        # Identify date and target columns using LLM
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

        llm = load_llm()
        parser = StrOutputParser()

        prediction_chain = prompt | llm | parser

        response = prediction_chain.invoke({
            "question": question,
            "columns": all_columns
        })

        time_column = None
        target_column = None

        for line in response.strip().splitlines():

            if line.startswith("time_column:"):
                time_column = line.split(":", 1)[1].strip()

            elif line.startswith("target_column:"):
                target_column = line.split(":", 1)[1].strip()

        # Validate identified columns
        if time_column not in df.columns:
            return "Could not identify a valid time column."

        if target_column not in df.columns:
            return "Could not identify a valid target column."

        # Prepare historical data
        forecast_df = df[[time_column, target_column]].copy()

        forecast_df[time_column] = pd.to_datetime(
            forecast_df[time_column],
            errors="coerce"
        )

        forecast_df[target_column] = pd.to_numeric(
            forecast_df[target_column],
            errors="coerce"
        )

        forecast_df = forecast_df.dropna(
            subset=[time_column, target_column]
        )

        forecast_df = forecast_df.sort_values(by=time_column)

        # Combine duplicate dates
        forecast_df = forecast_df.groupby(
            time_column,
            as_index=False
        )[target_column].sum()

        if len(forecast_df) < 3:
            return "Not enough historical data for forecasting."

        # Identify forecast duration using LLM
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
            input_variables=["question"]
        )

        horizon_chain = horizon_prompt | llm | parser

        horizon_response = horizon_chain.invoke({
            "question": question
        })

        periods = None
        unit = None

        for line in horizon_response.strip().splitlines():

            if line.startswith("periods:"):
                try:
                    periods = int(line.split(":", 1)[1].strip())
                except ValueError:
                    return "Could not determine a valid forecast period."

            elif line.startswith("unit:"):
                unit = line.split(":", 1)[1].strip().lower()

        if periods is None or periods <= 0:
            return "Forecast period must be greater than zero."

        if unit not in ["days", "weeks", "months", "years"]:
            return "Unsupported forecast time unit."

        # Map requested forecast unit to Pandas frequency
        frequency_map = {
            "days": "D",
            "weeks": "W-SUN",
            "months": "MS",
            "years": "YS"
        }

        forecast_freq = frequency_map[unit]

        # Resample historical observations to the requested frequency.
        # Summation is appropriate for additive metrics such as sales,
        # revenue, and quantity.
        historical_series = (
            forecast_df
            .set_index(time_column)[target_column]
            .resample(forecast_freq)
            .sum(min_count=1)
            .dropna()
        )

        if len(historical_series) < 3:
            return (
                "Not enough historical observations at the requested "
                "forecast frequency. Please provide more data or select "
                "a suitable forecast duration."
            )

        # Avoid forecasting at a finer frequency than the historical data.
        date_differences = (
            forecast_df[time_column]
            .sort_values()
            .diff()
            .dropna()
        )

        median_days = date_differences.dt.total_seconds().median() / 86400

        expected_days = {
            "days": 1,
            "weeks": 7,
            "months": 30,
            "years": 365
        }

        if median_days > expected_days[unit] * 1.5:
            return (
                "The requested forecast frequency is finer than the "
                "historical data frequency. Please select a suitable "
                "forecast period."
            )

        # Train Statsmodels Exponential Smoothing model
        try:

            if len(historical_series) >= 4:

                model = ExponentialSmoothing(
                    historical_series,
                    trend="add",
                    damped_trend=True,
                    initialization_method="estimated"
                )

            else:

                model = ExponentialSmoothing(
                    historical_series,
                    initialization_method="estimated"
                )

            fitted_model = model.fit(optimized=True)

            # Generate future predictions
            predictions = fitted_model.forecast(periods)

        except Exception as error:

            return f"Forecast generation failed: {str(error)}"

        # Calculate approximate forecast ranges using historical errors.
        # These are NOT formal statistical confidence intervals.
        residuals = (
            historical_series - fitted_model.fittedvalues
        ).dropna()

        error_std = residuals.std()

        if pd.isna(error_std):
            error_std = 0.0

        # Generate future dates
        last_date = historical_series.index[-1]

        future_dates = pd.date_range(
            start=last_date,
            periods=periods + 1,
            freq=forecast_freq
        )[1:]

        # Build output compatible with existing PDF generator
        forecast_records = []

        for date, prediction in zip(future_dates, predictions):

            predicted_value = float(prediction)

            forecast_records.append({
                "ds": date,
                "yhat": predicted_value,
                "yhat_lower": predicted_value - (1.96 * error_std),
                "yhat_upper": predicted_value + (1.96 * error_std)
            })

        return {
            "time_column": time_column,
            "target_column": target_column,
            "periods": periods,
            "unit": unit,
            "forecast": forecast_records
        }

    def _run_inner(self, question: str):

        forecast_result = self.get_forecast(question)

        if isinstance(forecast_result, str):
            return forecast_result

        if not isinstance(forecast_result, dict):
            return "Forecasting could not be completed."

        if "forecast" not in forecast_result:
            return "Forecasting did not return valid forecast data."

        llm = load_llm()
        parser = StrOutputParser()

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
6. Explain that lower and upper ranges are approximate estimates
   based on historical model errors, not formal confidence intervals.
7. Keep the answer concise.
""",
            input_variables=[
                "question",
                "prediction_result"
            ]
        )

        result_chain = result_prompt | llm | parser

        final_response = result_chain.invoke({
            "question": question,
            "prediction_result": forecast_result["forecast"]
        })

        return final_response

    def _run(self, question: str):

        try:
            return self._run_inner(question)

        except Exception as error:
            traceback.print_exc()
            return f"Forecasting failed: {error}"