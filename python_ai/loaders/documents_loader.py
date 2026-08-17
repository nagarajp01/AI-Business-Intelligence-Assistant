from loaders.pdf_loader import load_pdf
from loaders.csv_loader import load_csv
from loaders.excel_loader import load_excel
from loaders.word_loader import load_word


def load_documents(file_path):

    if file_path.endswith(".pdf"):

        documents = load_pdf(file_path)

        return documents

    elif file_path.endswith(".docx"):

        documents = load_word(file_path)

        return documents

    elif file_path.endswith(".csv"):

        documents = load_csv(file_path)

        return documents

    elif file_path.endswith(".xlsx"):

        documents = load_excel(file_path)

        return documents

    else:

        raise ValueError("Invalid file format")