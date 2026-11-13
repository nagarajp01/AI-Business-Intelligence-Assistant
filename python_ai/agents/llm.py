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

