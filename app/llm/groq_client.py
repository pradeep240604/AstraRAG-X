from langchain_groq import ChatGroq

from app.config.settings import settings


class GroqClient:

    def __init__(self):

        self.llm = ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model="llama-3.1-8b-instant",
            streaming=True
        )

    def get_llm(self):

        return self.llm