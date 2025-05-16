
import openai
from app.vector_store import query_vector_store
from app.embedder import get_embeddings

client = openai.OpenAI()

def run_csv_agent(query, index, chunks):
    query_embedding = get_embeddings([query])[0]
    top_k_idx = query_vector_store(index, query_embedding)
    selected_chunks = [chunks[i] for i in top_k_idx]
    context = "\n".join(selected_chunks)
    prompt = f"Use the table data below to answer the question.\n\nTable:\n{context}\n\nQuestion: {query}\nAnswer:"
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()
