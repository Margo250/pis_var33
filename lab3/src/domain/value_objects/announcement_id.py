from dataclasses import dataclass
import uuid
from ..exceptions.domain_exception import DomainException


@dataclass(frozen=True)
class AnnouncementId:
    """Value Object: Идентификатор объявления"""
    
    value: str
    
    def __post_init__(self):
        if not self.value or not self.value.strip():
            raise DomainException("AnnouncementId не может быть пустым")
        
        if len(self.value) > 50:
            raise DomainException(f"AnnouncementId слишком длинный: {len(self.value)}")
    
    @staticmethod
    def generate() -> 'AnnouncementId':
        """Сгенерировать новый ID"""
        return AnnouncementId(str(uuid.uuid4()))
    
    def __str__(self) -> str:
        return self.value
