
import openai
import os
from dotenv import load_dotenv

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_embeddings(texts):
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=texts
    )
    return [e.embedding for e in response.data]
