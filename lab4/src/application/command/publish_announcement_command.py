from dataclasses import dataclass


@dataclass(frozen=True)
class PublishAnnouncementCommand:
    """Команда: публикация объявления"""
    
    announcement_id: str
    
    def __post_init__(self):
        if not self.announcement_id or not self.announcement_id.strip():
            raise ValueError("announcement_id не может быть пустым")
