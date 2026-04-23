from dataclasses import dataclass
from ..exceptions.domain_exception import DomainException


@dataclass(frozen=True)
class FileAttachment:
    """Value Object: Вложение файла"""
    
    file_id: str
    filename: str
    file_size: int  # bytes
    mime_type: str
    storage_path: str
    
    def __post_init__(self):
        if not self.file_id or not self.file_id.strip():
            raise DomainException("file_id не может быть пустым")
        
        if not self.filename or not self.filename.strip():
            raise DomainException("filename не может быть пустым")
        
        if self.file_size <= 0:
            raise DomainException(f"file_size должен быть положительным: {self.file_size}")
        
        if not self.mime_type or not self.mime_type.strip():
            raise DomainException("mime_type не может быть пустым")
        
        if not self.storage_path or not self.storage_path.strip():
            raise DomainException("storage_path не может быть пустым")
        
        # Проверка MIME-типа
        allowed_types = ["image/", "application/pdf", "text/plain", "application/msword"]
        if not any(self.mime_type.startswith(t) for t in allowed_types):
            if self.mime_type not in allowed_types:
                raise DomainException(f"Неподдерживаемый MIME-тип: {self.mime_type}")
        
        # Проверка размера (10MB)
        max_size = 10 * 1024 * 1024
        if self.file_size > max_size:
            raise DomainException(f"Файл слишком большой: {self.file_size} байт (макс {max_size})")
    
    def get_file_extension(self) -> str:
        """Получить расширение файла"""
        if "." in self.filename:
            return self.filename.split(".")[-1].lower()
        return ""
