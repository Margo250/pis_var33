from dataclasses import dataclass


@dataclass(frozen=True)
class UpdateAnnouncementContentCommand:
    """Команда: обновление содержимого объявления"""
    
    announcement_id: str
    title: str
    content: str
    
    def __post_init__(self):
        if not self.announcement_id or not self.announcement_id.strip():
            raise ValueError("announcement_id не может быть пустым")
        
        if not self.title or not self.title.strip():
            raise ValueError("title не может быть пустым")
        
        if not self.content or not self.content.strip():
            raise ValueError("content не может быть пустым")
