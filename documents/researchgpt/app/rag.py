import ollama


def generate_answer(question: str, context_chunks: list[str]) -> str:
    """
    Sends the question + retrieved chunks to the local LLM and returns an answer.
    """
    context = "\n\n".join(context_chunks)

    prompt = f"""You are a helpful research assistant. Answer the question using ONLY the context below.
If the answer is not in the context, say "I couldn't find that in the document."

Context:
{context}

Question:
{question}

Answer:"""

    response = ollama.chat(
        model="llama3",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response["message"]["content"]