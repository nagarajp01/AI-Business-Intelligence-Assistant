from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.platypus import Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table
from reportlab.platypus import TableStyle
from reportlab.lib import colors


def create_report(outputPath, analysis_result):

    sales_metrics = analysis_result["sales_metrics"]

    document = SimpleDocTemplate(
        outputPath,
        pagesize=letter
    )

    styles = getSampleStyleSheet()
    elements = []

    title = Paragraph(
        "AI Business Intelligence Report",
        styles["Title"]
    )

    elements.append(title)
    elements.append(Spacer(1, 20))

    heading = Paragraph(
        "Executive Summary",
        styles["Heading1"]
    )

    elements.append(heading)
    elements.append(Spacer(1, 10))

    summary_lines = []

    for key, value in sales_metrics.items():

        if isinstance(value, dict):
            continue

        summary_lines.append(
            f"{key}: {value}"
        )

    summary_text = "<br/>".join(summary_lines)

    summary = Paragraph(
        summary_text,
        styles["BodyText"]
    )

    elements.append(summary)
    elements.append(Spacer(1, 20))

    sales_heading = Paragraph(
        "Sales Intelligence",
        styles["Heading1"]
    )

    elements.append(sales_heading)
    elements.append(Spacer(1, 10))

    sales_data = [
        ["Metric", "Value"]
    ]

    for key, value in sales_metrics.items():

        if isinstance(value, dict):
            continue

        sales_data.append(
            [
                str(key),
                str(value)
            ]
        )

    sales_table = Table(sales_data)

    sales_table.setStyle(
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
        ])
    )

    elements.append(sales_table)
    elements.append(Spacer(1, 20))

    for key, value in sales_metrics.items():

        if not isinstance(value, dict):
            continue

        section_heading = Paragraph(
            key.replace("_", " ").title(),
            styles["Heading2"]
        )

        elements.append(section_heading)
        elements.append(Spacer(1, 10))

        table_data = [
            ["Category", "Value"]
        ]

        for nested_key, nested_value in value.items():

            table_data.append(
                [
                    str(nested_key),
                    str(nested_value)
                ]
            )

        data_table = Table(table_data)

        data_table.setStyle(
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
            ])
        )

        elements.append(data_table)
        elements.append(Spacer(1, 20))

    document.build(elements)