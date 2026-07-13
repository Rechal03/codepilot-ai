import os

IGNORE_FOLDERS = {".git", ".venv", "venv", "node_modules", "__pycache__", "dist", "build"}

ALLOWED_EXTENSIONS = {
    ".py", ".js", ".ts", ".tsx", ".java", ".cpp",
    ".html", ".css", ".json", ".md", ".yaml", ".yml"
}


def scan_project(root_folder):
    code_files = []

    for current_folder, folders, files in os.walk(root_folder):
        folders[:] = [f for f in folders if f not in IGNORE_FOLDERS]

        for filename in files:
            ext = os.path.splitext(filename)[1]
            if ext in ALLOWED_EXTENSIONS:
                full_path = os.path.join(current_folder, filename)
                code_files.append(full_path)

    return code_files


def read_files(file_paths):
    documents = []

    for path in file_paths:
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            documents.append({
                "path": path,
                "content": content
            })
        except Exception as e:
            print(f"Could not read {path}: {e}")

    return documents


def chunk_text(text, chunk_size=300, overlap=50):
    words = text.split()
    chunks = []

    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]
        chunk = " ".join(chunk_words)
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks