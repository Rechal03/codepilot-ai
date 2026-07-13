import faiss
import numpy as np


class VectorStore:
    def __init__(self):
        self.index = None
        self.chunks = []

    def build(self, chunks: list[str], vectors):
        """
        Builds a FAISS index from chunks and their embedding vectors.
        """
        vectors = np.array(vectors).astype("float32")
        dimension = vectors.shape[1]

        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(vectors)
        self.chunks = chunks

    def search(self, query_vector, top_k: int = 3):
        """
        Finds the top_k chunks most similar to the query vector.
        """
        query_vector = np.array([query_vector]).astype("float32")
        distances, indices = self.index.search(query_vector, top_k)

        results = []
        for idx in indices[0]:
            results.append(self.chunks[idx])

        return results