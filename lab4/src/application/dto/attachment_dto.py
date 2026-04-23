from dataclasses import dataclass


@dataclass(frozen=True)
class AttachmentDTO:
    """Read DTO: Вложение"""
    
    file_id: str
    filename: str
    file_size: int
    mime_type: str
