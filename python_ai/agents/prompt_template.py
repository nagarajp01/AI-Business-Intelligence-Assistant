from langchain_core.prompts import PromptTemplate

def load_prompt():

    prompt = PromptTemplate(

        template="""
You are an AI Business Intelligence Assistant.

Answer the question only from the provided context.

If the context does not contain the answer, say:

"I don't know based on the provided documents."

Context:
{context}

Question:
{question}

Answer:
""",

        input_variables=["context", "question"]

    )

    return prompt