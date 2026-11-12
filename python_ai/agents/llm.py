import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()


def load_llm():

    llm = ChatOpenAI(
        model="openrouter/free",
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY")
    )

    return llm



# import os
# from langchain_google_genai import ChatGoogleGenerativeAI
# from dotenv import load_dotenv

# load_dotenv()

# def load_llm():
#     llm = ChatGoogleGenerativeAI(
#         model="gemini-3.8-flash",
#         google_api_key=os.getenv("GOOGLE_API_KEY"),
#         temperature=0
#     )
#     return llm


# import os
# from langchain_groq import ChatGroq
# from dotenv import load_dotenv

# load_dotenv()

# def load_llm():
#     llm = ChatGroq(
#         # model="openai/gpt-oss-120b",
#         # model="openai/gpt-oss-20b",
#         api_key=os.getenv("GROQ_API_KEY")
#     )
#     return llm

# from langchain_groq import ChatGroq
# from dotenv import load_dotenv


# load_dotenv()


# def load_llm():
#     llm=ChatGroq(
#         # model="openai/gpt-oss-20b"
#         model="openai/gpt-oss-120b"
#     )
#     return llm




