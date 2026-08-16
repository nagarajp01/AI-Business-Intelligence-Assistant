from loaders.pdf_loader import load_pdf
from utils.text_splitter import split_documents

#"./../docs/tsla-20241231-gen.pdf"

documents=load_pdf("./../docs/tsla-20241231-gen.pdf")

chunks=split_documents(documents)

print(f"pages:  : {len(documents)}")
print(f"chunks:  : {len(chunks)}")

print(chunks[0].page_content)