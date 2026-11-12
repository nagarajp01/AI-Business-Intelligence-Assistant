from langchain_community.vectorstores import Chroma

def create_vector_store(chunks,embedding_model,collection_name):
    vector_store= Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        collection_name=collection_name,
        persist_directory="../chroma_db"
    )
    return vector_store