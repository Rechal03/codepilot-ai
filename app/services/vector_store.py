import faiss
import numpy as np
import pickle
import os

INDEX_PATH = "vector_store/index.faiss"
METADATA_PATH = "vector_store/metadata.pkl"


def save_to_vector_store(embedded_chunks):
    os.makedirs("vector_store", exist_ok=True)

    vectors = np.array([item["embedding"] for item in embedded_chunks]).astype("float32")

    dimension = vectors.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(vectors)

    faiss.write_index(index, INDEX_PATH)

    metadata = [
        {"path": item["path"], "chunk": item["chunk"]}
        for item in embedded_chunks
    ]
    with open(METADATA_PATH, "wb") as f:
        pickle.dump(metadata, f)

    return {
        "total_vectors_stored": index.ntotal
    }