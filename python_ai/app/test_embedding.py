from embeddings.embedding_model import load_embedding_model
from loaders.pdf_loader import load_pdf
from utils.text_splitter import split_documents

#"./../docs/tsla-20241231-gen.pdf"

documents=load_pdf("./../docs/tsla-20241231-gen.pdf")

chunks=split_documents(documents)

embedding_model=load_embedding_model()

texts=[chunk.page_content for chunk in chunks]


vectors=embedding_model.embed_documents(texts)


print(f"pages :  :  {len(documents)}")
print(f"chunks :  :  {len(chunks)}")
print(f"vectors :  :  {len(vectors)}")


print(f"dimensions:   : {len(vectors[0])}")
# print(vector)


