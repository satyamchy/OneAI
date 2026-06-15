import uuid

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base, TimestampMixin, uuid_pk


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = uuid_pk()
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(512), nullable=False)
    display_name: Mapped[str | None] = mapped_column(String(160), nullable=True)
    default_model_id: Mapped[str | None] = mapped_column(String(160), nullable=True)
    phone_number: Mapped[str | None] = mapped_column(String(20), nullable=True)
    linked_in_url: Mapped[str | None] = mapped_column(String(160), nullable=True)
    github_url: Mapped[str | None] = mapped_column(String(160), nullable=True)
    updated_resume_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    updated_at: Mapped[str | None] = mapped_column(String(160), nullable=True)

    conversations = relationship("Conversation", back_populates="user")

