from fastapi import APIRouter

from app.api.v1 import (
    analytics_routes,
    auth_routes,
    conversation_routes,
    message_routes,
    model_routes,
    user_routes,
)

api_router = APIRouter()
api_router.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
api_router.include_router(user_routes.router, prefix="/users", tags=["users"])
api_router.include_router(conversation_routes.router, prefix="/conversations", tags=["conversations"])
api_router.include_router(message_routes.router, prefix="/conversations", tags=["messages"])
api_router.include_router(model_routes.router, prefix="/models", tags=["models"])
api_router.include_router(analytics_routes.router, prefix="/analytics", tags=["analytics"])

