import uuid

from sqlalchemy import Boolean, Float, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.models.base import Base, TimestampMixin, uuid_pk


class ModelRegistry(Base, TimestampMixin):
    __tablename__ = "model_registry"

    id: Mapped[uuid.UUID] = uuid_pk()
    provider: Mapped[str] = mapped_column(String(80), index=True, nullable=False)
    model_id: Mapped[str] = mapped_column(String(160), unique=True, index=True, nullable=False)
    display_name: Mapped[str] = mapped_column(String(160), nullable=False)
    capabilities_json: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    context_window: Mapped[int] = mapped_column(Integer, default=8192, nullable=False)
    supports_streaming: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    supports_tools: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    input_cost_per_1m: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    output_cost_per_1m: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    fallback_model_id: Mapped[str | None] = mapped_column(String(160), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True, nullable=False)

