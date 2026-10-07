def load_documents(file_path):

    if file_path.endswith(".pdf"):
        from loaders.pdf_loader import load_pdf

        documents = load_pdf(file_path)

        return documents

    elif file_path.endswith(".docx"):
        from loaders.word_loader import load_word

        documents = load_word(file_path)

        return documents

    elif file_path.endswith(".csv"):
        from loaders.csv_loader import load_csv

        documents = load_csv(file_path)

        return documents

    elif file_path.endswith(".xlsx"):
        from loaders.excel_loader import load_excel

        documents = load_excel(file_path)

        return documents

    else:

        raise ValueError("Invalid file format")