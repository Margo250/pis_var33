"""Конфигурация подключения к PostgreSQL"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from typing import Generator
import os

# URL подключения к БД
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://announcement_user:announcement_pass@localhost:5432/announcement_db"
)

# Создание engine
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    echo=True  # Логировать SQL запросы
)

# Фабрика сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """Dependency injection для получения сессии БД"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Инициализация БД (создание таблиц)"""
    from ..models.announcement_model import AnnouncementModel
    Base.metadata.create_all(bind=engine)
