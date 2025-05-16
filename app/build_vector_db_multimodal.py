import openai
import os
import numpy as np
import json
import pickle
from dotenv import load_dotenv
from chunker_multimodal import extract_text_and_images

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_embeddings(texts, batch_size=100):
    all_embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        response = client.embeddings.create(
            model="text-embedding-ada-002",
            input=batch
        )
        all_embeddings.extend([e.embedding for e in response.data])
    return all_embeddings

def build_multimodal_vector_db(pdf_path, output_prefix):
    chunks = extract_text_and_images(pdf_path)
    contents = [c["content"][:3000] for c in chunks]
    embeddings = get_embeddings(contents)

    for i, emb in enumerate(embeddings):
        chunks[i]["embedding"] = emb

    os.makedirs("vector_db", exist_ok=True)
    with open(f"vector_db/{output_prefix}_chunks.pkl", "wb") as f:
        pickle.dump(chunks, f)

    import faiss
    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype("float32"))
    faiss.write_index(index, f"vector_db/{output_prefix}_index.faiss")

    with open(f"vector_db/{output_prefix}_meta.pkl", "wb") as f:
        pickle.dump({"source": pdf_path, "type": "multimodal", "count": len(chunks)}, f)

    print(f"✅ Saved multimodal vector DB for {output_prefix}")