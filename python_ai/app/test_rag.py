# from loaders.pdf_loader import load_pdf
from utils.text_splitter import split_documents
from embeddings.embedding_model import load_embedding_model
from vector_store.chroma_store import create_vector_store
from retrievers.retriever import create_retriever
from agents.rag_chain import create_rag_chain
from loaders.documents_loader import load_documents
#"./../docs/tsla-20241231-gen.pdf"

# documents=load_pdf("./../docs/tsla-20241231-gen.pdf")
file_path=input("enter your file path")
documents=load_documents(file_path)

chunks=split_documents(documents)

embedding_model=load_embedding_model()

# texts=[chunk.page_content for chunk in chunks]


vector_store=create_vector_store(
    chunks,
    embedding_model
)

retriever=create_retriever(vector_store)

question=input("enter your question ??> : ")

answer=create_rag_chain(
    retriever,
    question
)

print("\nANSWER:\n")

print(answer)



# print(f"pages :  :  {len(documents)}")
# print(f"chunks :  :  {len(chunks)}")
# print("chromadb created suuccfully")
# print(vector)


