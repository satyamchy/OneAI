import uuid
from sqlalchemy import Boolean, Float, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class ModelRegistry(Base):
    __tablename__ = "model_registry"

    # Primary unique identifier for this model registry row.
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # OpenRouter model name used in API requests.
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    # Provider routing label, currently openrouter.
    provider: Mapped[str] = mapped_column(String(100), nullable=False)
    # Maximum context window advertised for this model.
    context_window: Mapped[int] = mapped_column(Integer, nullable=False)
    # Estimated cost per input token.
    cost_per_input_token: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    # Estimated cost per output token.
    cost_per_output_token: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    # Whether the model should be shown in the UI.
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
