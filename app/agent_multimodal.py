# -*- coding: utf-8 -*-
"""
Created on Tue May 13 18:47:28 2025

@author: ShivakrishnaBoora
"""

import openai
from app.embedder import get_embeddings
from app.vector_store import query_vector_store
# import os

# client = openai.OpenAI(api_key=os.getenv("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"))
import os
from dotenv import load_dotenv
load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def run_multimodal_agent(query, index, chunks, top_k=3):
    # from app.embedder import get_embeddings
    # from app.vector_store import query_vector_store

    # Embed query
    query_embedding = get_embeddings([query])[0]

    # Run vector search
    top_k_idx = query_vector_store(index, query_embedding, top_k=top_k)

    # ✅ Ensure index is within bounds
    selected_chunks = [chunks[i] for i in top_k_idx if i < len(chunks)]

    # Build context
    context = ""
    sources = []

    for c in selected_chunks:
        label = "Figure" if c["chunk_type"] == "figure" else "Text"
        context += f"[{label} - Page {c['source_page']}]: {c['content']}"

        sources.append({
            # "type": c["chunk_type"],
            "page": c["source_page"],
            "snippet": c["content"][:300] + ("..." if len(c["content"]) > 300 else ""),
            "image_path": c.get("image_path")
        })

    prompt = f"""You are a technical assistant analyzing a document containing text, tables and figures. Use the content below to answer the question.

                {context}
                
                Question:
                {query}
                
                Answer:"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    answer = response.choices[0].message.content.strip()
    return answer, sources