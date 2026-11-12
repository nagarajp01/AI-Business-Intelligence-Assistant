# from langchain_community.document_loaders import PDFPlumberLoader

# def load_pdf(file_path):
#     loader=PDFPlumberLoader(file_path)
#     documents=loader.load()
#     return documents


from langchain_community.document_loaders import PDFPlumberLoader

def load_pdf(file_path):
    loader = PDFPlumberLoader(file_path)
    documents = loader.load()

    print("\n========== PDF EXTRACTION DEBUG ==========")
    print("Total pages loaded:", len(documents))

    for i, doc in enumerate(documents):
        print(f"\nPage {i + 1}")
        print("Characters:", len(doc.page_content))
        print("Preview:", doc.page_content[:300])

    print("==========================================")

    return documents

