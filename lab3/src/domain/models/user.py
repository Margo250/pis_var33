from ..exceptions.domain_exception import DomainException


class User:
    """Entity: Пользователь системы"""
    
    def __init__(self, user_id: str, email: str, name: str):
        self._id = user_id
        self._is_active = True
        self._email_verified = False
        self._created_at = None  # TODO: добавить datetime
        
        self._set_email(email)
        self._set_name(name)
    
    def _set_email(self, email: str) -> None:
        if not email or not email.strip():
            raise DomainException("Email не может быть пустым")
        
        if "@" not in email or "." not in email:
            raise DomainException("Некорректный формат email")
        
        self._email = email.strip().lower()
    
    def _set_name(self, name: str) -> None:
        if not name or not name.strip():
            raise DomainException("Имя не может быть пустым")
        
        if len(name) > 100:
            raise DomainException("Имя не может быть длиннее 100 символов")
        
        self._name = name.strip()
    
    def verify_email(self) -> None:
        """Подтвердить email"""
        self._email_verified = True
    
    def deactivate(self) -> None:
        """Деактивировать пользователя"""
        self._is_active = False
    
    def activate(self) -> None:
        """Активировать пользователя"""
        self._is_active = True
    
    # === Геттеры ===
    
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def email(self) -> str:
        return self._email
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def is_active(self) -> bool:
        return self._is_active
    
    @property
    def email_verified(self) -> bool:
        return self._email_verified
    
    # === Равенство по ID ===
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, User):
            return False
        return self._id == other._id
    
    def __hash__(self) -> int:
        return hash(self._id)
