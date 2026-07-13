from sentence_transformers import SentenceTransformer

_model = None


def get_embedding_model():
    """
    Loads the embedding model once and reuses it (avoids reloading every time).
    """
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def embed_chunks(chunks: list[str]):
    """
    Converts a list of text chunks into a list of embedding vectors.
    """
    model = get_embedding_model()
    embeddings = model.encode(chunks)
    return embeddings