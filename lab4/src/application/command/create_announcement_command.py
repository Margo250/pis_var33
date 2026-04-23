from dataclasses import dataclass
from typing import Optional, List


@dataclass(frozen=True)
class CreateAnnouncementCommand:
    """Команда: создание нового объявления"""
    
    group_id: str
    author_id: str
    title: str
    content: str
    attachment_ids: Optional[List[str]] = None
    
    def __post_init__(self):
        if not self.group_id or not self.group_id.strip():
            raise ValueError("group_id не может быть пустым")
        
        if not self.author_id or not self.author_id.strip():
            raise ValueError("author_id не может быть пустым")
        
        if not self.title or not self.title.strip():
            raise ValueError("title не может быть пустым")
        
        if not self.content or not self.content.strip():
            raise ValueError("content не может быть пустым")
