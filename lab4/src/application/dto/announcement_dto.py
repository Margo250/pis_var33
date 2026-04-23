from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from .attachment_dto import AttachmentDTO


@dataclass(frozen=True)
class AnnouncementDTO:
    """Read DTO: Объявление"""
    
    id: str
    group_id: str
    author_id: str
    title: str
    content: str
    status: str
    attachments: List[AttachmentDTO]
    created_at: datetime
    published_at: Optional[datetime]
    scheduled_for: Optional[datetime]
    updated_at: datetime
