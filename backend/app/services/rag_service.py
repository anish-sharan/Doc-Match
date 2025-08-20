import os
from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader, ServiceContext, VectorStoreIndex
from llama_index.llms.openai import OpenAI


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def process_text_with_llm(text: str):
    # Create LLM instance
    llm = OpenAI(api_key=OPENAI_API_KEY)
    
    # Tokenize & embed
    documents = [text]
    # For now, we can return tokenized text as a list of words
    return text.split()
