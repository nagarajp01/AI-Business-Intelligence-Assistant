from langchain_text_splitters import RecursiveCharacterTextSplitter
# from loaders.pdf_loader import load_pdf
def split_documents(documents):
    splitter=RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks=splitter.split_documents(documents)
    return chunks