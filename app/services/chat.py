import faiss
import numpy as np
import pickle
import requests
from app.services.embeddings import model

INDEX_PATH = "vector_store/index.faiss"
METADATA_PATH = "vector_store/metadata.pkl"

OLLAMA_URL = "http://localhost:11434/api/generate"


def search_similar_chunks(question, top_k=3):
    index = faiss.read_index(INDEX_PATH)

    with open(METADATA_PATH, "rb") as f:
        metadata = pickle.load(f)

    question_vector = model.encode([question]).astype("float32")
    distances, indices = index.search(question_vector, top_k)

    results = []
    for idx in indices[0]:
        results.append(metadata[idx])

    return results


def ask_ollama(question, context_chunks):
    context_text = "\n\n".join(
        [f"File: {chunk['path']}\n{chunk['chunk']}" for chunk in context_chunks]
    )

    prompt = f"""You are an expert software engineer helping explain a codebase.
Only answer using the code context below. If the answer isn't in the context, say "I don't know based on the provided code."

Context:
{context_text}

Question: {question}

Answer:"""

    response = requests.post(OLLAMA_URL, json={
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    })

    result = response.json()
    return result["response"]


def answer_question(question, history=None):
    if history is None:
        history = []

    chunks = search_similar_chunks(question)

    history_text = ""
    for turn in history:
        history_text += f"User: {turn['question']}\nAssistant: {turn['answer']}\n\n"

    context_text = "\n\n".join(
        [f"File: {chunk['path']}\n{chunk['chunk']}" for chunk in chunks]
    )

    prompt = f"""You are an expert software engineer helping explain a codebase.
Only answer using the code context below. If the answer isn't in the context, say "I don't know based on the provided code."

Previous conversation:
{history_text}

Code context:
{context_text}

New question: {question}

Answer:"""

    response = requests.post(OLLAMA_URL, json={
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    })

    result = response.json()

    return {
        "question": question,
        "answer": result["response"],
        "sources": [chunk["path"] for chunk in chunks]
    }


def find_bugs(file_path_filter=None, top_k=5):
    index = faiss.read_index(INDEX_PATH)

    with open(METADATA_PATH, "rb") as f:
        metadata = pickle.load(f)

    if file_path_filter:
        relevant_chunks = [m for m in metadata if file_path_filter in m["path"]]
    else:
        relevant_chunks = metadata[:top_k]

    context_text = "\n\n".join(
        [f"File: {chunk['path']}\n{chunk['chunk']}" for chunk in relevant_chunks]
    )

    prompt = f"""You are a senior software engineer performing a code review.
Analyze the following code and identify potential bugs, security issues, or bad practices.
For each issue found, specify: the file, the problem, and a suggested fix.
If no issues are found, say so clearly.

Code:
{context_text}

Review:"""

    response = requests.post(OLLAMA_URL, json={
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    })

    result = response.json()

    return {
        "files_reviewed": [chunk["path"] for chunk in relevant_chunks],
        "review": result["response"]
    }


def generate_documentation():
    with open(METADATA_PATH, "rb") as f:
        metadata = pickle.load(f)

    context_text = "\n\n".join(
        [f"File: {chunk['path']}\n{chunk['chunk']}" for chunk in metadata]
    )

    prompt = f"""You are a technical writer creating documentation for a software project.
Based on the code below, generate a clear README.md style document including:
- Project overview
- Key features
- Technologies used
- Folder structure
- How the main components work together

Code:
{context_text}

Documentation:"""

    response = requests.post(OLLAMA_URL, json={
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    })

    result = response.json()
    return result["response"]