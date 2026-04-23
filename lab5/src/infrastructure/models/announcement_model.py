"""SQLAlchemy ORM модель для объявления"""

from sqlalchemy import Column, String, DateTime, Enum, Integer, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()


class AnnouncementModel(Base):
    """ORM модель для таблицы announcements"""
    
    __tablename__ = "announcements"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    group_id = Column(String(36), nullable=False, index=True)
    author_id = Column(String(36), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    content = Column(String(5000), nullable=False)
    status = Column(Enum("draft", "scheduled", "published", "archived", name="status_enum"), 
                    nullable=False, default="draft")
    attachments = Column(JSON, default=[])  # Храним как JSON
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    published_at = Column(DateTime, nullable=True)
    scheduled_for = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    
    def to_dict(self) -> dict:
        """Преобразовать модель в dict"""
        return {
            "id": self.id,
            "group_id": self.group_id,
            "author_id": self.author_id,
            "title": self.title,
            "content": self.content,
            "status": self.status,
            "attachments": self.attachments,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "published_at": self.published_at.isoformat() if self.published_at else None,
            "scheduled_for": self.scheduled_for.isoformat() if self.scheduled_for else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
