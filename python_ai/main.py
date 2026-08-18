from document_processors.document_processor import document_processor
# from tools.rag_tool import RAGTool
from agents.react_agent import create_agent


# Ask the user for a file path
file_path = input("Enter your file path: ")

# Process the document only once
retriever = document_processor(file_path)

agent_executor=create_agent(retriever=retriever)



# Create the RAG tool object
# rag_tool = RAGTool(
#     retriever=retriever
# )


while True:

    # Ask the user for a question
    question = input("Enter your question: ")
    if question.lower() == "exit":
        break
    answer=agent_executor.invoke({
        "input":question
    })

    # Exit the program

    # Use the stored retriever

    # Print the answer
    print("\nANSWER:\n")

    print(answer['output'])