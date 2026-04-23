from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ListAnnouncementsByGroupQuery:
    """Запрос: список объявлений в группе"""
    
    group_id: str
    limit: Optional[int] = 50
    offset: Optional[int] = 0
    
    def __post_init__(self):
        if not self.group_id or not self.group_id.strip():
            raise ValueError("group_id не может быть пустым")
        
        if self.limit and self.limit <= 0:
            raise ValueError(f"limit должен быть положительным: {self.limit}")
        
        if self.offset and self.offset < 0:
            raise ValueError(f"offset не может быть отрицательным: {self.offset}")
