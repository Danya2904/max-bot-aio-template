from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """
    Базовый класс для всех SQLAlchemy моделей.
    Именно отсюда Alembic будет брать Base.metadata для генерации миграций.
    """
    pass