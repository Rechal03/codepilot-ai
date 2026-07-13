from fastapi import FastAPI, UploadFile, File, Form
import shutil
import os

from loaders import load_pdf, load_docx, load_website
from splitter import split_text
from embeddings import embed_chunks, get_embedding_model
from vectorstore import VectorStore
from rag import generate_answer

app = FastAPI()

# Keep everything in memory for now (one document at a time)
store = VectorStore()


@app.get("/")
def read_root():
    return {"message": "ResearchGPT backend is alive"}


@app.post("/upload")
def upload_document(file: UploadFile = File(...)):
    # Save the uploaded file temporarily
    temp_path = f"../documents/{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Pick the right loader based on file extension
    if file.filename.endswith(".pdf"):
        text = load_pdf(temp_path)
    elif file.filename.endswith(".docx"):
        text = load_docx(temp_path)
    else:
        return {"error": "Unsupported file type. Use PDF or DOCX."}

    # Process: chunk -> embed -> store
    chunks = split_text(text)
    vectors = embed_chunks(chunks)
    store.build(chunks, vectors)

    return {
        "message": f"Processed {file.filename}",
        "chunks_created": len(chunks)
    }


@app.post("/query")
def query_document(question: str = Form(...)):
    if store.index is None:
        return {"error": "No document has been uploaded yet."}

    model = get_embedding_model()
    question_vector = model.encode(question)

    results = store.search(question_vector, top_k=3)
    answer = generate_answer(question, results)

    return {
        "question": question,
        "answer": answer,
        "sources": results
    }