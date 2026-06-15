from fastapi import APIRouter, Response, status

from app.core.dependencies import CurrentUser, DbSession
from app.schemas.conversation import ConversationCreate, ConversationRead, ConversationUpdate
from app.services.conversation_service import ConversationService

router = APIRouter()


@router.get("", response_model=list[ConversationRead])
async def list_conversations(db: DbSession, user: CurrentUser) -> list[ConversationRead]:
    conversations = await ConversationService(db).list_for_user(user)
    return [ConversationRead.model_validate(conversation) for conversation in conversations]


@router.post("", response_model=ConversationRead, status_code=status.HTTP_201_CREATED)
async def create_conversation(
    payload: ConversationCreate,
    db: DbSession,
    user: CurrentUser,
) -> ConversationRead:
    conversation = await ConversationService(db).create(payload, user)
    return ConversationRead.model_validate(conversation)


@router.get("/{conversation_id}", response_model=ConversationRead)
async def get_conversation(
    conversation_id: str,
    db: DbSession,
    user: CurrentUser,
) -> ConversationRead:
    conversation = await ConversationService(db).get_owned(conversation_id, user)
    return ConversationRead.model_validate(conversation)


@router.patch("/{conversation_id}", response_model=ConversationRead)
async def update_conversation(
    conversation_id: str,
    payload: ConversationUpdate,
    db: DbSession,
    user: CurrentUser,
) -> ConversationRead:
    conversation = await ConversationService(db).update(conversation_id, payload, user)
    return ConversationRead.model_validate(conversation)


@router.delete("/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation(
    conversation_id: str,
    db: DbSession,
    user: CurrentUser,
) -> Response:
    await ConversationService(db).delete(conversation_id, user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

