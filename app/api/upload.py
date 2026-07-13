from app.services.project_scanner import scan_project, read_files, chunk_text
from fastapi import APIRouter, UploadFile, File
import shutil
import os
import zipfile
from app.services.embeddings import create_embeddings
from app.services.vector_store import save_to_vector_store
router = APIRouter()


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    os.makedirs("documents", exist_ok=True)

    file_path = f"documents/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    extract_folder = os.path.join(
        "documents",
        os.path.splitext(file.filename)[0]
    )

    os.makedirs(extract_folder, exist_ok=True)

    with zipfile.ZipFile(file_path, "r") as zip_ref:
        zip_ref.extractall(extract_folder)

    files_found = scan_project(extract_folder)
    file_contents = read_files(files_found)

    all_chunks = []
    for doc in file_contents:
        chunks = chunk_text(doc["content"])
        for chunk in chunks:
            all_chunks.append({
                "path": doc["path"],
                "chunk": chunk
            })

    embedded_chunks = create_embeddings(all_chunks)
    storage_result = save_to_vector_store(embedded_chunks)

    return {
        "filename": file.filename,
        "message": "File uploaded and extracted successfully!",
        "extract_location": extract_folder,
        "total_files": len(files_found),
        "total_chunks": len(all_chunks),
        "total_vectors_stored": storage_result["total_vectors_stored"]
    }