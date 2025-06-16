from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from app.api.deps import get_current_user
from app.schemas.chat import ChatRequest
from app.services.chat import generate_chat_response

router = APIRouter()

@router.post("/")
async def chat_endpoint(request: ChatRequest, current_user: str = Depends(get_current_user)):
    """
    Handles chat messages and streams responses from the LLM.
    """
    try:
        # `generate_chat_response` yields text chunks
        return StreamingResponse(generate_chat_response(request.messages), media_type="text/plain")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat API error: {e}")