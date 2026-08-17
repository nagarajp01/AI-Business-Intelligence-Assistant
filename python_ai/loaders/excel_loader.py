import pandas as pd
from langchain_community.document_loaders import DataFrameLoader


def load_excel(file_path):

    dataframe = pd.read_excel(file_path)

    loader = DataFrameLoader(
        dataframe,
        page_content_column=dataframe.columns[0]
    )

    documents = loader.load()

    return documents