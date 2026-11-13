from loaders.documents_loader import load_documents
from utils.text_splitter import split_documents
from embeddings.embedding_model import load_embedding_model
from vector_store.chroma_store import create_vector_store
from retrievers.retriever import create_retriever


def document_processor(file_path, collection_name):

    documents = load_documents(file_path)
    embedding_model = load_embedding_model()

    vector_store = None
    batch = []
    batch_size = 20
    total_chunks = 0

    for document in documents:

        chunks = split_documents([document])

        for chunk in chunks:
            batch.append(chunk)

            if len(batch) >= batch_size:
                vector_store = create_vector_store(
                    batch,
                    embedding_model,
                    collection_name,
                    vector_store
                )

                total_chunks += len(batch)
                print(f"Processed chunks: {total_chunks}")
                batch = []

    # Process remaining chunks
    if batch:
        vector_store = create_vector_store(
            batch,
            embedding_model,
            collection_name,
            vector_store
        )

        total_chunks += len(batch)

    if vector_store is None:
        raise ValueError("No text could be extracted from the uploaded document.")

    print(f"Total chunks processed: {total_chunks}")

    retriever = create_retriever(vector_store)

    return retriever
