from dataclasses import dataclass
import re
from ..exceptions.domain_exception import DomainException


@dataclass(frozen=True)
class Email:
    """Value Object: Email пользователя"""
    
    value: str
    
    def __post_init__(self):
        if not self.value or not self.value.strip():
            raise DomainException("Email не может быть пустым")
        
        # Простая валидация email
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, self.value.strip()):
            raise DomainException(f"Некорректный формат email: {self.value}")
        
        object.__setattr__(self, 'value', self.value.strip().lower())
    
    def get_domain(self) -> str:
        """Получить домен email"""
        return self.value.split("@")[1]
