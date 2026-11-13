from langchain_community.document_loaders import PDFPlumberLoader

def load_pdf(file_path):
    loader = PDFPlumberLoader(file_path)
    return loader.lazy_load()
