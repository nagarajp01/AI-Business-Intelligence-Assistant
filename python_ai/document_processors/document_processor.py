# from loaders.pdf_loader import load_pdf
import time
#from loaders.documents_loader import load_documents
#from utils.text_splitter import split_documents
#from embeddings.embedding_model import load_embedding_model
#from vector_store.chroma_store import create_vector_store
#from retrievers.retriever import create_retriever
# from agents.rag_chain import create_rag_chain
#"./../docs/tsla-20241231-gen.pdf"

# documents=load_pdf("./../docs/tsla-20241231-gen.pdf")

print("\n========== DOCUMENT PROCESSOR IMPORT ==========")
print("\n1. Importing documents_loader...")
start = time.time()
from loaders.documents_loader import load_documents
print(
    f"documents_loader import: "
    f"{time.time() - start:.2f} seconds"
)
print("\n2. Importing text_splitter...")
start = time.time()
from utils.text_splitter import split_documents
print(
    f"text_splitter import: "
    f"{time.time() - start:.2f} seconds"
)

print("\n3. Importing embedding_model...")
start = time.time()

from embeddings.embedding_model import load_embedding_model
print(
    f"embedding_model import: "
    f"{time.time() - start:.2f} seconds"
)

print("\n4. Importing chroma_store...")
start = time.time()

from vector_store.chroma_store import create_vector_store
print(
    f"chroma_store import: "
    f"{time.time() - start:.2f} seconds"
)
print("\n5. Importing retriever...")
start = time.time()
from retrievers.retriever import create_retriever
print(
    f"retriever import: "
    f"{time.time() - start:.2f} seconds"
)
print("\n===============================================")
# def document_processor(file_path):
#     # file_path=input("enter your file path")

#     documents=load_documents(file_path)

#     chunks=split_documents(documents)

#     embedding_model=load_embedding_model()

#     vector_store=create_vector_store(
#         chunks,
#         embedding_model)

#     retriever=create_retriever(vector_store)

#     return retriever
def document_processor(file_path):

    print("\n========== DOCUMENT PROCESSING ==========")

    print("\n1. Loading PDF...")
    start = time.time()

    documents = load_documents(file_path)

    print(
        f"PDF loading: "
        f"{time.time() - start:.2f} seconds"
    )

    print("\n2. Splitting documents...")
    start = time.time()

    chunks = split_documents(documents)

    print(
        f"Text splitting: "
        f"{time.time() - start:.2f} seconds"
    )

    print("\n3. Loading embedding model...")
    start = time.time()

    embedding_model = load_embedding_model()

    print(
        f"Embedding model: "
        f"{time.time() - start:.2f} seconds"
    )

    print("\n4. Creating vector store...")
    start = time.time()

    vector_store = create_vector_store(
        chunks,
        embedding_model
    )

    print(
        f"Vector store creation: "
        f"{time.time() - start:.2f} seconds"
    )

    print("\n5. Creating retriever...")
    start = time.time()

    retriever = create_retriever(vector_store)

    print(
        f"Retriever creation: "
        f"{time.time() - start:.2f} seconds"
    )

    print("\n========================================")

    return retriever






