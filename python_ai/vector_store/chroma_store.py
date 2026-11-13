from langchain_community.vectorstores import Chroma

def create_vector_store(
    chunks,
    embedding_model,
    collection_name,
    vector_store=None
):
    if vector_store is None:
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embedding_model,
            collection_name=collection_name,
            persist_directory="../chroma_db"
        )
    else:
        vector_store.add_documents(chunks)

    return vector_store
