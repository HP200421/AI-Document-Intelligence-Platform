import datetime
from src.db.base import Base
from sqlalchemy import String, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id:Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    filepath: Mapped[str] = mapped_column(String(1000), nullable=False)
    filesize: Mapped[int] = mapped_column(nullable=False)
    content_type:Mapped[str] = mapped_column(String(255), nullable=False)
    created_at:Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default= func.now(),
        nullable=False
    )
    updated_at:Mapped[datetime.datetime] = mapped_column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False
    )
