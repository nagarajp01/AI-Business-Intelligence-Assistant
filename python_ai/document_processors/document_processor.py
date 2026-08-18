# from loaders.pdf_loader import load_pdf
from loaders.documents_loader import load_documents
from utils.text_splitter import split_documents
from embeddings.embedding_model import load_embedding_model
from vector_store.chroma_store import create_vector_store
from retrievers.retriever import create_retriever
# from agents.rag_chain import create_rag_chain
#"./../docs/tsla-20241231-gen.pdf"

# documents=load_pdf("./../docs/tsla-20241231-gen.pdf")




def document_processor(file_path):
    # file_path=input("enter your file path")

    documents=load_documents(file_path)

    chunks=split_documents(documents)

    embedding_model=load_embedding_model()

    vector_store=create_vector_store(
        chunks,
        embedding_model)

    retriever=create_retriever(vector_store)

    return retriever






