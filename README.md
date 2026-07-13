# CodePilot AI

CodePilot AI is an AI-powered coding assistant that ingests an entire codebase, indexes it using semantic embeddings, and answers natural language questions about the project — architecture, specific files, how things work — grounded in the actual source code rather than guesses. It can also generate a code review and auto-generate documentation for any uploaded repository.

## Features

- **Repository upload** — upload a zipped project and it's automatically extracted, scanned, and indexed
- **AI chat** — ask questions about the codebase in plain English, with answers grounded in retrieved source code and cited file sources
- **Conversation memory** — follow-up questions retain context from earlier in the conversation
- **AI code review** — automatically flags bugs, security issues, and code smells with suggested fixes
- **Documentation generator** — generates a full README-style document for any uploaded project
- **Simple web UI** — upload and chat through a browser interface, no API tool required

## Tech Stack

- **Backend:** FastAPI, Uvicorn
- **AI / RAG:** Sentence Transformers (`all-MiniLM-L6-v2`) for embeddings, FAISS for vector search
- **LLM:** Llama 3, served locally via Ollama — fully private, no API costs
- **Frontend:** HTML/CSS/JavaScript
- **Language:** Python

## Architecture

```
Upload ZIP
    │
    ▼
Extract & Scan (ignore .git, .venv, node_modules, etc.)
    │
    ▼
Read file contents
    │
    ▼
Chunk text (overlapping windows)
    │
    ▼
Generate embeddings (Sentence Transformers)
    │
    ▼
Store in FAISS vector index
    │
    ▼
User asks a question
    │
    ▼
Embed question → semantic search in FAISS → retrieve top matching chunks
    │
    ▼
Send question + retrieved chunks to Llama 3 (via Ollama)
    │
    ▼
Grounded answer + cited sources
```

## Project Structure

```
codepilot-ai/
│
├── app/
│   ├── api/
│   │   ├── upload.py       # Upload, extraction, indexing endpoint
│   │   └── chat.py         # Chat, review, and documentation endpoints
│   │
│   └── services/
│       ├── project_scanner.py   # File discovery, reading, chunking
│       ├── embeddings.py        # Embedding model + generation
│       ├── vector_store.py      # FAISS storage
│       └── chat.py              # RAG retrieval, LLM prompting, review, docs
│
├── frontend/
│   └── index.html           # Simple web UI (upload + chat)
│
├── documents/                # Uploaded/extracted repositories (gitignored)
├── vector_store/             # FAISS index + metadata (gitignored)
├── main.py                   # FastAPI app entrypoint
└── requirements.txt
```

## Setup

### Prerequisites
- Python 3.10+
- [Ollama](https://ollama.com) installed, with the `llama3` model pulled:
  ```bash
  ollama pull llama3
  ```

### Installation
```bash
git clone https://github.com/Rechal03/codepilot-ai.git
cd codepilot-ai
python -m venv .venv
.venv\Scripts\Activate.ps1   # Windows
pip install -r requirements.txt
```

### Running
```bash
uvicorn main:app --reload
```

- API docs: `http://127.0.0.1:8000/docs`
- Web UI: open `frontend/index.html` directly in a browser

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/upload` | POST | Upload a zipped repository — extracts, scans, chunks, embeds, and indexes it |
| `/chat` | POST | Ask a question about the indexed codebase (supports conversation history) |
| `/review` | POST | Run an AI code review on the indexed codebase, optionally filtered by file |
| `/generate-docs` | POST | Auto-generate README-style documentation for the indexed codebase |

## Example

**Request:** `POST /chat`
```json
{
  "question": "What embedding model does this project use?",
  "history": []
}
```

**Response:**
```json
{
  "question": "What embedding model does this project use?",
  "answer": "The embedding model used is all-MiniLM-L6-v2, a Hugging Face Sentence Transformers model, loaded and run locally.",
  "sources": ["app/embeddings.py"]
}
```

## Future Improvements

- GitHub URL ingestion (clone directly instead of requiring a zip)
- React frontend with multi-repo project management
- JWT authentication and per-user projects
- Docker Compose deployment (FastAPI + Redis + Postgres)
- Streaming responses for faster perceived latency