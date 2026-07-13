from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embeddings(chunks):
    texts = [item["chunk"] for item in chunks]
    vectors = model.encode(texts)

    embedded_chunks = []
    for i, item in enumerate(chunks):
        embedded_chunks.append({
            "path": item["path"],
            "chunk": item["chunk"],
            "embedding": vectors[i].tolist()
        })

    return embedded_chunks