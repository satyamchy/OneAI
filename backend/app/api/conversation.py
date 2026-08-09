from fastapi import APIRouter

from app.services.conversation_service import run_conversation

from app.schemas.conversation import RunResponse


router = APIRouter()

@router.get("/",  response_model=RunResponse)
async def conversation(query: str):
    return await run_conversation(query)