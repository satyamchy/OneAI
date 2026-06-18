import uuid
from datetime import datetime
from sqlalchemy import DateTime, Enum, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.constants import RunStatus
from app.database import Base

class ModelRun(Base):
    __tablename__ = "model_runs"

    # Primary unique identifier for the model run.
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # Assistant message produced by this model run.
    message_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("messages.id", ondelete="CASCADE"), index=True, nullable=False)
    # Model requested before any provider fallback.
    model_requested: Mapped[str] = mapped_column(String(255), nullable=False)
    # Model that actually produced the response.
    model_used: Mapped[str] = mapped_column(String(255), nullable=False)
    # Provider that served the response.
    provider: Mapped[str] = mapped_column(String(100), nullable=False)
    # Estimated input tokens sent to the provider.
    input_tokens: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    # Estimated output tokens received from the provider.
    output_tokens: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    # End-to-end latency in milliseconds.
    latency_ms: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    # Estimated model cost for this run.
    estimated_cost: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    # Final status of the model run.
    status: Mapped[RunStatus] = mapped_column(Enum(RunStatus), default=RunStatus.SUCCESS, nullable=False)
    # Optional reason if fallback or error occurred.
    fallback_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Trace ID attached to API responses and logs.
    request_id: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    # Timestamp when the run was recorded.
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    message = relationship("Message", back_populates="model_run")
