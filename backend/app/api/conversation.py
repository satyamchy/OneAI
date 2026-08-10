from fastapi import APIRouter
from app.schemas.conversation import RunResponse
from app.services.conversation_service import run_conversation


router = APIRouter()

@router.get("/",  response_model=RunResponse)
async def conversation(query: str):
    return await run_conversation(query)