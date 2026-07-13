from fastapi import APIRouter
from pydantic import BaseModel
from app.services.chat import answer_question, find_bugs
router = APIRouter()


class ChatRequest(BaseModel):
    question: str

class ReviewRequest(BaseModel):
    file_path_filter: str = None
    
    
@router.post("/chat")
async def chat(request: ChatRequest):
    result = answer_question(request.question)
    return result



@router.post("/review")
async def review(request: ReviewRequest):
    result = find_bugs(request.file_path_filter)
    return result