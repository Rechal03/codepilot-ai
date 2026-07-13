from fastapi import FastAPI
from app.api.upload import router as upload_router
from app.api.chat import router as chat_router
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(upload_router)
app.include_router(chat_router)

@app.get("/")
def home():
    return {
        "project": "CodePilot AI",
        "version": "1.0",
        "status": "Running Successfully"
    }