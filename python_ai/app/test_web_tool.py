from tools.web_tool import web_search


question=input("enter your question...? : ??")

result=web_search.invoke(question)

print(result)

print(type(result))