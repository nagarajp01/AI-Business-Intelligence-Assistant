# from langchain_groq import ChatGroq
# from dotenv import load_dotenv

# load_dotenv()


# def load_llm():

#     llm = ChatGroq(
#         model="groq/compound"
#     )

#     return llm


from langchain_groq import ChatGroq
from dotenv import load_dotenv


load_dotenv()


def load_llm():
    llm=ChatGroq(
        model="openai/gpt-oss-20b"
    )
    return llm