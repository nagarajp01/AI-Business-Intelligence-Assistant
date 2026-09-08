from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.platypus import Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table
from reportlab.platypus import TableStyle
from reportlab.lib import colors
from reportlab.platypus import Image
import matplotlib.pyplot as plt
from reportlab.platypus import KeepTogether



def create_report(outputPath, analysis_result):

    sales_metrics = analysis_result["sales_metrics"]
    chart_data=find_chart_data(sales_metrics)
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
        section_elements = []
        section_elements.append(section_heading)
        # elements.append(section_heading)
        section_elements.append(Spacer(1, 10))

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

        data_table = Table(table_data,colWidths=[250, 200])

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
                    10
                ),
            ])
        )

        # elements.append(data_table)
        section_elements.append(data_table)
        chart=create_chart(
            key,
            value
        )
        # elements.append(Image(chart, width=400, height=250))
        section_elements.append(Image(chart, width=400, height=250))
        section_elements.append(Spacer(1, 20))
        # elements.append(Spacer(1, 20))
        elements.append(
            KeepTogether(section_elements)
            )


    document.build(elements)
def find_chart_data(sales_metrics):
    chart_data={}
    for key,value in sales_metrics.items():
        if isinstance(value,dict) and len(value)>1:
            chart_data[key]=value
        
    return chart_data

def create_chart(chart_name,chart_values):

    categories=list(chart_values.keys())
    values=list(chart_values.values())
    plt.figure(figsize=(8, 5))
    plt.bar(categories,values)
    plt.title(chart_name.replace("_", " ").title())
    plt.xlabel("Category")
    plt.ylabel("Values")
    plt.tight_layout()
    chart_path=f"{chart_name}.png"
    plt.savefig(chart_path)
    plt.close()

    return chart_path

