from langchain_community.document_loaders import PDFPlumberLoader

def load_pdf(pdf_path):
    loader=PDFPlumberLoader(pdf_path)
    documents=loader.load()
    return documents


if __name__=="__main__":
    path=input("enter the pdf path")
    documents=load_pdf(path)
    # print(documents)
    print(len(documents))




# loader=PDFPlumberLoader("./../docs/tsla-20241231-gen.pdf")
#"./../docs/tsla-20241231-gen.pdf"


# print(f"{'Page':<6} {'Characters':<12} {'Status':<10} {'Preview'}")
# print("-" * 60)

# for i, doc in enumerate(documents):
#     chars = len(doc.page_content.strip())
#     status = " OK" if chars > 0 else " EMPTY"
#     preview = doc.page_content.strip()[:30].replace('\n', ' ')
#     print(f"{i+1:<6} {chars:<12} {status:<10} {preview}")

