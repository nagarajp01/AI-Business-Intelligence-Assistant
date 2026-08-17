from agents.llm import load_llm
from agents.prompt_template import load_prompt

def create_rag_chain(retriever,question):
    retrieved_docs=retriever.invoke(question)

    context="\n\n".join(doc.page_content for doc in retrieved_docs)

    prompt=load_prompt()

    final_prompt=prompt.invoke({
        "context":context,
        "question":question
    })

    llm=load_llm()

    answer=llm.invoke(final_prompt)

    return answer.content

