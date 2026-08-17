from tools.news_tool import news_search


question=input("enter your question...? : ??")

result=news_search.invoke(question)

print(result)

print(type(result))