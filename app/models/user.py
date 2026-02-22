# app/models/user.py
from datetime import datetime
from sqlalchemy import BigInteger, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base

class User(Base):
    __tablename__ = "users"

    # MAX API User ID. Запрещаем БД генерировать собственные ID.
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    
    # Поля, специфичные для MAX API (уточни типы и длины согласно документации MAX API)
    username: Mapped[str | None] = mapped_column(String(32))
    first_name: Mapped[str] = mapped_column(String(64))
    language_code: Mapped[str | None] = mapped_column(String(10))
    
    # Системные поля для аналитики и дебага
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now()
    )