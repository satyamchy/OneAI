from langchain_groq import ChatGroq
from app.config import GROQ_API_KEY


# Setup LLM
def get_llm():
    return ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name="llama-3.1-8b-instant",
        temperature=0
    )

  
    