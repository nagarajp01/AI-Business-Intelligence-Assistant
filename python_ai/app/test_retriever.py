from embeddings.embedding_model import load_embedding_model
from loaders.pdf_loader import load_pdf
from utils.text_splitter import split_documents
from vector_store.chroma_store import create_vector_store
from retrievers.retriever import create_retriever

#"./../docs/tsla-20241231-gen.pdf"

documents=load_pdf("./../docs/tsla-20241231-gen.pdf")

chunks=split_documents(documents)

embedding_model=load_embedding_model()

# texts=[chunk.page_content for chunk in chunks]


vector_store=create_vector_store(
    chunks,
    embedding_model
)

retriever=create_retriever(vector_store)

query=input("enter your question ??>")
results=retriever.invoke(query)

print(f"retrieved chunks :  :  {len(results)}")

for i,doc in enumerate(results):
    print("\n" + "="*50)
    print(f"chunk {i+1}")
    print("="*50)
    print(doc.page_content[:500])



# print(f"pages :  :  {len(documents)}")
# print(f"chunks :  :  {len(chunks)}")
# print("chromadb created suuccfully")
# print(vector)


