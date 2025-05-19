from app.agent_pdf import run_pdf_agent
from app.agent_csv import run_csv_agent
from app.agent_multimodal import run_multimodal_agent
from app.vector_store import load_vector_store
import pickle, json
from openai import OpenAI
import os 
from app.vector_store import query_vector_store
from app.embedder import get_embeddings
from app.agent_multimodal import run_multimodal_agent

def extract_keywords_from_query(query):
    prompt = f"""Extract 3–6 most relevant keywords or phrases from the following user question that can be used to search a document:

            Question: "{query}"
            
            Keywords:"""
    # client = OpenAI(api_key=os.getenv("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"))
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    keywords_text = response.choices[0].message.content
    keywords = [k.strip().lower() for k in keywords_text.replace(",", "\n").splitlines() if k.strip()]
    return keywords[:5]


def orchestrate(query, source_key=None):
    with open("vector_db/metadata.json", "r") as f:
        metadata = json.load(f)

    # Auto-pick first matching or allow explicit source
    if not source_key:
        source_key = next(iter(metadata))  # pick first

    meta = metadata[source_key]
    kind = meta["type"]
    index_path = meta["index_path"]
    chunks_path = meta["chunks_path"]
    meta_path = meta["meta_path"]

    index, _ = load_vector_store(index_path, meta_path)
    with open(chunks_path, "rb") as f:
        chunks = pickle.load(f)

    if kind == "pdf":
        return run_pdf_agent(query, index, chunks)
    elif kind == "csv":
        return run_csv_agent(query, index, chunks)
    elif kind == "multimodal":
        # Get top-k from full index
        query_embedding = get_embeddings([query])[0]
        top_k_idx = query_vector_store(index, query_embedding)
    
        # Retrieve from full chunk list
        selected_chunks = [chunks[i] for i in top_k_idx if i < len(chunks)]
    
        # Optional: Re-rank or highlight chunks matching keywords
        keywords = extract_keywords_from_query(query)
        for chunk in selected_chunks:
            chunk["score_boost"] = sum(k in chunk["content"].lower() for k in keywords)
    
        return run_multimodal_agent(query, index, chunks)
    else:
        return f"❌ Unsupported document type: {kind}"
