class DomainException(Exception):
    """Базовое исключение для доменных ошибок"""
    pass


class EmptyAnnouncementException(DomainException):
    """Объявление не может быть пустым"""
    pass


class AnnouncementNotEditableException(DomainException):
    """Объявление не редактируется (статус не DRAFT)"""
    pass


class AttachmentLimitExceededException(DomainException):
    """Превышен лимит вложений"""
    pass


class InvalidStatusTransitionException(DomainException):
    """Недопустимый переход статуса"""
    pass
