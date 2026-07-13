from fastapi import APIRouter
from pydantic import BaseModel
from app.services.chat import answer_question, find_bugs, generate_documentation
router = APIRouter()


class ChatRequest(BaseModel):
    question: str
    history: list = []

class ReviewRequest(BaseModel):
    file_path_filter: str = None
    
    
@router.post("/chat")
async def chat(request: ChatRequest):
    result = answer_question(request.question, request.history)
    return result



@router.post("/review")
async def review(request: ReviewRequest):
    result = find_bugs(request.file_path_filter)
    return result
@router.post("/generate-docs")
async def generate_docs():
    documentation = generate_documentation()
    return {"documentation": documentation}