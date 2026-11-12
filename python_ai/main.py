from document_processors.document_processor import document_processor
# from tools.rag_tool import RAGTool
from agents.react_agent import build_agent


# Ask the user for a file path
# file_path = input("Enter your file path: ")
file_path = input("Enter PDF path (press Enter to skip): ").strip()
# data_file_path = input("Enter CSV/Excel path: ")
data_file_path = input("Enter Excel/CSV path (press Enter to skip): ").strip()

retriever = None

# retriever = document_processor(file_path)

# Process the document only once
if file_path:
    retriever = document_processor(file_path)


agent=build_agent(
    retriever=retriever,
    data_file_path=data_file_path
)



# Create the RAG tool object
# rag_tool = RAGTool(
#     retriever=retriever
# )


while True:

    # Ask the user for a question
    question = input("Enter your question: ")
    if question.lower() == "exit":
        break
    response=agent.invoke({
        "messages":[
            
            {
                "role":"user",
                "content":question
            },
        ]
    })


    # Exit the program

    # Use the stored retriever

    # Print the answer
    print("\nANSWER:\n")

    print(response["messages"][-1].content)


    print("\nTOOLS USED:\n")
    for message in response["messages"]:
        if hasattr(message, "tool_calls") and message.tool_calls:
            for tool_call in message.tool_calls:
                print("→", tool_call["name"])

# print("\nANSWER:\n")

# print(response["messages"][-1].content)