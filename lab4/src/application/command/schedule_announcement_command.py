from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class ScheduleAnnouncementCommand:
    """Команда: планирование публикации объявления"""
    
    announcement_id: str
    scheduled_for: datetime
    
    def __post_init__(self):
        if not self.announcement_id or not self.announcement_id.strip():
            raise ValueError("announcement_id не может быть пустым")
        
        if not self.scheduled_for:
            raise ValueError("scheduled_for не может быть пустым")
        
        if self.scheduled_for <= datetime.now():
            raise ValueError("scheduled_for должно быть в будущем")
