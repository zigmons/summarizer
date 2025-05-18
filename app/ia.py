# app/ia.py

from google import genai

def get_chat_client(api_key: str):
    """
    Retorna um cliente GenAI configurado com a API Key.
    """
    return genai.Client(api_key=api_key)
