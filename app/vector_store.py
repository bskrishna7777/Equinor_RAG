
import faiss
import numpy as np
import pickle

def load_vector_store(index_path, metadata_path):
    index = faiss.read_index(index_path)
    with open(metadata_path, "rb") as f:
        metadata = pickle.load(f)
    return index, metadata

def query_vector_store(index, query_embedding, top_k=3):
    distances, indices = index.search(np.array([query_embedding]).astype("float32"), top_k)
    return indices[0]
