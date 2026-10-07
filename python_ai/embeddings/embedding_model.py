from langchain_huggingface import HuggingFaceEmbeddings
_embedding_model = None
def load_embedding_model():
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

    return _embedding_model


# from langchain_huggingface import HuggingFaceEmbeddings


# def load_embedding_model():
#     embedding_model=HuggingFaceEmbeddings(
#         model_name="sentence-transformers/all-MiniLM-L6-v2"
#     )

#     return embedding_model