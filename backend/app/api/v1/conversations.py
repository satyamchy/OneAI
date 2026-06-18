from uuid import UUID
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.conversation import ConversationCreate, ConversationListResponse, ConversationResponse, ConversationUpdate
from app.services.conversation_service import create_conversation, delete_conversation, get_conversation, list_conversations, update_conversation
from app.utils.request_id import generate_request_id

router = APIRouter(prefix="/conversations", tags=["conversations"])

# Lists conversations for the authenticated user.
@router.get("", response_model=ConversationListResponse)
async def list_user_conversations(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    return ConversationListResponse(request_id=generate_request_id(), conversations=await list_conversations(db, user))

# Creates a conversation for the authenticated user.
@router.post("", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
async def create_user_conversation(payload: ConversationCreate, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    conversation = await create_conversation(db, user, payload)
    return ConversationResponse(request_id=generate_request_id(), conversation=conversation)

# Gets one conversation owned by the authenticated user.
@router.get("/{conversation_id}", response_model=ConversationResponse)
async def get_user_conversation(conversation_id: UUID, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    conversation = await get_conversation(db, user, conversation_id)
    return ConversationResponse(request_id=generate_request_id(), conversation=conversation)

# Updates title, model, archive state, or interaction mode for a conversation.
@router.patch("/{conversation_id}", response_model=ConversationResponse)
async def patch_user_conversation(conversation_id: UUID, payload: ConversationUpdate, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    conversation = await update_conversation(db, user, conversation_id, payload)
    return ConversationResponse(request_id=generate_request_id(), conversation=conversation)

# Deletes a conversation owned by the authenticated user.
@router.delete("/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_conversation(conversation_id: UUID, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    await delete_conversation(db, user, conversation_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
