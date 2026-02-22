# app/models/__init__.py
from app.models.base import Base
from app.models.user import User

# Явно указываем, что доступно при импорте из пакета models
__all__ = [
    "Base",
    "User",
]