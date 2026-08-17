from agents.llm import load_llm

llm=load_llm()

response=llm.invoke("hey groq")

print(response.content)