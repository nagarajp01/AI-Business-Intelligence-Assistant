from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    PageBreak
)
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import matplotlib.pyplot as plt
# CREATE REPORT
def create_report(outputPath, analysis_result):

    sales_metrics = analysis_result["sales_metrics"]
    forecast_result = analysis_result["forecast_result"]

    document = SimpleDocTemplate(
        outputPath,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    elements = []

    table_elements = []
    graph_elements = []


    # PAGE 1
    # EXECUTIVE SUMMARY

    title = Paragraph(
        "AI Business Intelligence Report",
        styles["Title"]
    )

    elements.append(title)

    elements.append(
        Spacer(1, 20)
    )

    # EXECUTIVE SUMMARY

    heading = Paragraph(
        "Executive Summary",
        styles["Heading1"]
    )

    elements.append(heading)

    elements.append(
        Spacer(1, 10)
    )

    summary_lines = []
    for key, value in sales_metrics.items():

        if isinstance(value, dict):
            continue

        formatted_key = (
            key.replace("_", " ").title()
        )

        formatted_value = format_number(
            value
        )

        summary_lines.append(
            f"<b>{formatted_key}:</b> {formatted_value}"
        )
    summary_text = "<br/><br/>".join(
        summary_lines
    )


    summary = Paragraph(
        summary_text,
        styles["BodyText"]
    )

    elements.append(summary)

    elements.append(
        Spacer(1, 25)
    )

    # SALES INTELLIGENCE

    sales_heading = Paragraph(
        "Sales Intelligence",
        styles["Heading1"]
    )

    elements.append(
        sales_heading
    )

    elements.append(
        Spacer(1, 10)
    )


    sales_data = [
        [
            "Metric",
            "Value"
        ]
    ]


    for key, value in sales_metrics.items():

        if isinstance(value, dict):
            continue

        sales_data.append(
            [
                key.replace(
                    "_",
                    " "
                ).title(),

                format_number(
                    value
                )
            ]
        )


    sales_table = Table(
        sales_data,
        colWidths=[
            250,
            200
        ]
    )
    sales_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.lightgrey
            ),

            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.black
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                1,
                colors.black
            ),

            (
                "PADDING",
                (0, 0),
                (-1, -1),
                6
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),
        ])
    )


    elements.append(
        sales_table
    )

    # CREATE TABLES AND GRAPHS


    for key, value in sales_metrics.items():

        if not isinstance(value, dict):
            continue

        # TABLE

        table_heading = Paragraph(
            key.replace(
                "_",
                " "
            ).title(),

            styles["Heading2"]
        )


        table_element = create_metric_table(
            key,
            value
        )
        table_elements.append(
            [
                table_heading,
                Spacer(1, 5),
                table_element
            ]
        )

        # GRAPH

        chart_path = create_chart(
            key,
            value
        )


        if chart_path is not None:

            graph_heading = Paragraph(
                key.replace(
                    "_",
                    " "
                ).title(),

                styles["Heading2"]
            )


            graph_table = Table(
                [
                    [
                        graph_heading
                    ],
                    [
                        Image(
                            chart_path,
                            width=250,
                            height=150
                        )
                    ]
                ],

                colWidths=[
                    250
                ]
            )


            graph_table.setStyle(
                TableStyle([
                    (
                        "ALIGN",
                        (0, 0),
                        (-1, -1),
                        "CENTER"
                    ),

                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP"
                    ),

                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        5
                    ),

                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        5
                    ),

                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        5
                    ),

                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        5
                    ),
                ])
            )


            graph_elements.append(
                graph_table
            )

    # PAGE 2+
    # TABLE PAGES

    if table_elements:

        elements.append(
            PageBreak()
        )


        for i in range(
            0,
            len(table_elements),
            4
        ):

            current_tables = table_elements[
                i:i + 4
            ]


            for table_block in current_tables:

                elements.extend(
                    table_block
                )

                elements.append(
                    Spacer(1, 15)
                )


            if i + 4 < len(table_elements):

                elements.append(
                    PageBreak()
                )


    # GRAPH PAGES

    if graph_elements:

        elements.append(
            PageBreak()
        )


        for i in range(
            0,
            len(graph_elements),
            4
        ):

            current_graphs = graph_elements[
                i:i + 4
            ]


            graph_rows = []


            for j in range(
                0,
                len(current_graphs),
                2
            ):

                row = current_graphs[
                    j:j + 2
                ]


                while len(row) < 2:

                    row.append("")


                graph_rows.append(
                    row
                )


            graph_table = Table(
                graph_rows,
                colWidths=[
                    270,
                    270
                ]
            )


            graph_table.setStyle(
                TableStyle([
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP"
                    ),

                    (
                        "ALIGN",
                        (0, 0),
                        (-1, -1),
                        "CENTER"
                    ),

                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        5
                    ),

                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        5
                    ),

                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        5
                    ),

                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        15
                    ),
                ])
            )


            elements.append(
                graph_table
            )


            if i + 4 < len(graph_elements):

                elements.append(
                    PageBreak()
                )

    # FORECAST PAGE

    elements.append(
        PageBreak()
    )


    forecast_heading = Paragraph(
        "Sales Forecast",
        styles["Heading1"]
    )


    elements.append(
        forecast_heading
    )


    elements.append(
        Spacer(1, 10)
    )


    # FORECAST INFORMATION

    forecast_info = []


    if "time_column" in forecast_result:

        forecast_info.append(
            f"<b>Time Column:</b> "
            f"{forecast_result['time_column']}"
        )


    if "target_column" in forecast_result:

        forecast_info.append(
            f"<b>Target Column:</b> "
            f"{forecast_result['target_column']}"
        )


    if "periods" in forecast_result:

        forecast_info.append(
            f"<b>Forecast Period:</b> "
            f"{forecast_result['periods']} "
            f"{forecast_result.get('unit', '')}"
        )

    if forecast_info:

        forecast_info_text = "<br/>".join(
            forecast_info
        )

        elements.append(
            Paragraph(
                forecast_info_text,
                styles["BodyText"]
            )
        )

        elements.append(
            Spacer(1, 15)
        )

    # FORECAST TABLE

    forecast_data = [
        [
            "Date",
            "Forecast",
            "Lower Bound",
            "Upper Bound"
        ]
    ]


    forecast_items = forecast_result.get(
        "forecast",
        []
    )


    for forecast_item in forecast_items:

        forecast_data.append(
            [
                format_date(
                    forecast_item.get("ds")
                ),

                format_number(
                    forecast_item.get("yhat")
                ),

                format_number(
                    forecast_item.get("yhat_lower")
                ),

                format_number(
                    forecast_item.get("yhat_upper")
                )
            ]
        )


    forecast_table = Table(
        forecast_data,
        colWidths=[
            110,
            110,
            110,
            110
        ]
    )


    forecast_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.lightgrey
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                1,
                colors.black
            ),

            (
                "PADDING",
                (0, 0),
                (-1, -1),
                6
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),

            (
                "ALIGN",
                (1, 1),
                (-1, -1),
                "RIGHT"
            ),
        ])
    )


    elements.append(
        forecast_table
    )


    elements.append(
        Spacer(1, 20)
    )

    # FORECAST GRAPH

    if forecast_items:

        forecast_chart_path = create_forecast_chart(
            forecast_items
        )


        if forecast_chart_path:

            forecast_graph_heading = Paragraph(
                "Sales Forecast Graph",
                styles["Heading2"]
            )


            elements.append(
                forecast_graph_heading
            )


            elements.append(
                Spacer(1, 5)
            )


            elements.append(
                Image(
                    forecast_chart_path,
                    width=450,
                    height=280
                )
            )

    # BUILD PDF

    document.build(
        elements
    )
# CREATE METRIC TABLE

def create_metric_table(
    metric_name,
    metric_values
):


    if is_simple_dictionary(
        metric_values
    ):

        table_data = [
            [
                "Category",
                "Value"
            ]
        ]


        for key, value in metric_values.items():

            table_data.append(
                [
                    str(key),

                    format_number(
                        value
                    )
                ]
            )


        data_table = Table(
            table_data,
            colWidths=[
                250,
                200
            ]
        )


    else:

        table_data = [
            [
                "Product-Region",
                "Total Sales",
                "Total Quantity",
                "Avg Price / Unit"
            ]
        ]


        for category, details in metric_values.items():

            if not isinstance(
                details,
                dict
            ):
                continue


            table_data.append(
                [
                    str(category),

                    format_number(
                        details.get(
                            "total_sales"
                        )
                    ),

                    format_number(
                        details.get(
                            "total_quantity"
                        )
                    ),

                    format_number(
                        details.get(
                            "avg_price_per_unit"
                        )
                    )
                ]
            )


        data_table = Table(
            table_data,
            colWidths=[
                130,
                110,
                100,
                110
            ]
        )


    data_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.lightgrey
            ),

            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.black
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                1,
                colors.black
            ),

            (
                "PADDING",
                (0, 0),
                (-1, -1),
                5
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),
        ])
    )


    return data_table


def is_simple_dictionary(
    dictionary
):

    if not isinstance(
        dictionary,
        dict
    ):
        return False


    for value in dictionary.values():

        if isinstance(
            value,
            dict
        ):
            return False


    return True


def format_number(
    value
):

    if value is None:

        return ""


    try:

        numeric_value = float(
            value
        )


        # Integer values
        # should not show .00

        if numeric_value.is_integer():

            return f"{numeric_value:,.0f}"


        return f"{numeric_value:,.2f}"


    except (
        ValueError,
        TypeError
    ):

        return str(value)

# FORMAT DATE

def format_date(
    value
):

    if value is None:

        return ""


    try:

        return value.strftime(
            "%Y-%m-%d"
        )

    except AttributeError:

        return str(value).split(
            " "
        )[0]

# FIND CHART DATA

def find_chart_data(
    sales_metrics
):

    chart_data = {}


    for key, value in sales_metrics.items():

        if isinstance(
            value,
            dict
        ):

            chart_data[key] = value


    return chart_data

# CREATE CHART

def create_chart(
    chart_name,
    chart_values
):

    # CASE 1
    # SIMPLE DICTIONARY

    if is_simple_dictionary(
        chart_values
    ):

        categories = []

        values = []


        for category, value in chart_values.items():

            try:

                numeric_value = float(
                    value
                )

            except (
                ValueError,
                TypeError
            ):

                continue


            categories.append(
                str(category)
            )

            values.append(
                numeric_value
            )


        if not values:

            return None

        # DETERMINE Y AXIS LABEL

        if "growth" in chart_name.lower():

            y_label = "Growth Rate (%)"

        else:

            y_label = "Value"

        # CREATE CHART

        plt.figure(
            figsize=(10, 5)
        )


        plt.bar(
            categories,
            values
        )


        plt.title(
            chart_name.replace(
                "_",
                " "
            ).title()
        )


        plt.xlabel(
            "Product / Region"
        )


        plt.ylabel(
            y_label
        )


        plt.xticks(
            rotation=60,
            ha="right"
        )


        plt.tight_layout()


        chart_path = (
            f"{chart_name}.png"
        )


        plt.savefig(
            chart_path,
            dpi=150,
            bbox_inches="tight"
        )


        plt.close()


        return chart_path

    # CASE 2
    # NESTED DICTIONARY

    categories = []

    values = []


    for category, details in chart_values.items():

        if not isinstance(
            details,
            dict
        ):
            continue


        metric_value = None

        # PRODUCT REGION METRICS
        # Use total_sales

        if "total_sales" in details:

            metric_value = details[
                "total_sales"
            ]

        # OTHER NESTED METRICS

        elif "growth_rate" in details:

            metric_value = details[
                "growth_rate"
            ]


        else:
            # Find first numeric nested value

            for nested_value in details.values():

                try:

                    metric_value = float(
                        nested_value
                    )

                    break

                except (
                    ValueError,
                    TypeError
                ):

                    continue


        if metric_value is None:

            continue


        try:

            numeric_value = float(
                metric_value
            )

        except (
            ValueError,
            TypeError
        ):

            continue


        categories.append(
            str(category)
        )

        values.append(
            numeric_value
        )

    # NOTHING TO PLOT

    if not values:

        return None
    # CREATE NESTED DATA CHARt

    plt.figure(
        figsize=(10, 5)
    )


    plt.bar(
        categories,
        values
    )


    plt.title(
        chart_name.replace(
            "_",
            " "
        ).title()
    )

    # Y AXIS LABEL

    if "growth" in chart_name.lower():

        plt.ylabel(
            "Growth Rate (%)"
        )

    elif "sales" in chart_name.lower():

        plt.ylabel(
            "Total Sales"
        )

    else:

        plt.ylabel(
            "Value"
        )


    plt.xlabel(
        "Product / Region"
    )


    plt.xticks(
        rotation=60,
        ha="right"
    )


    plt.tight_layout()


    chart_path = (
        f"{chart_name}.png"
    )


    plt.savefig(
        chart_path,
        dpi=150,
        bbox_inches="tight"
    )


    plt.close()


    return chart_path

# CREATE FORECAST CHART

def create_forecast_chart(
    forecast_items
):

    forecast_dates = []

    forecast_values = []

    forecast_lower = []

    forecast_upper = []


    for forecast_item in forecast_items:

        date_value = forecast_item.get(
            "ds"
        )

        yhat = forecast_item.get(
            "yhat"
        )

        yhat_lower = forecast_item.get(
            "yhat_lower"
        )

        yhat_upper = forecast_item.get(
            "yhat_upper"
        )


        if date_value is None:

            continue


        if yhat is None:

            continue


        forecast_dates.append(
            date_value
        )


        forecast_values.append(
            float(yhat)
        )


        if yhat_lower is not None:

            forecast_lower.append(
                float(yhat_lower)
            )

        else:

            forecast_lower.append(
                float(yhat)
            )


        if yhat_upper is not None:

            forecast_upper.append(
                float(yhat_upper)
            )

        else:

            forecast_upper.append(
                float(yhat)
            )


    if not forecast_values:

        return None

    # CREATE FORECAST GRAPH

    plt.figure(
        figsize=(9, 5)
    )


    plt.plot(
        forecast_dates,
        forecast_values,
        marker="o",
        label="Forecast"
    )

    # CONFIDENCE RANGE

    if (
        len(forecast_lower)
        == len(forecast_upper)
        == len(forecast_values)
    ):

        plt.fill_between(
            forecast_dates,
            forecast_lower,
            forecast_upper,
            alpha=0.2,
            label="Confidence Range"
        )


    plt.title(
        "Sales Forecast"
    )


    plt.xlabel(
        "Date"
    )


    plt.ylabel(
        "Forecast Sales"
    )


    plt.xticks(
        rotation=45
    )


    plt.legend()


    plt.tight_layout()


    forecast_chart_path = (
        "sales_forecast.png"
    )


    plt.savefig(
        forecast_chart_path,
        dpi=150,
        bbox_inches="tight"
    )


    plt.close()


    return forecast_chart_path