from typing import List
from ..exceptions.domain_exception import DomainException


class Group:
    """Entity: Группа пользователей"""
    
    MIN_MEMBERS = 1
    MAX_MEMBERS = 100
    
    def __init__(self, group_id: str, name: str, owner_id: str):
        self._id = group_id
        self._owner_id = owner_id
        self._member_ids: List[str] = []
        self._admin_ids: List[str] = []
        
        self._set_name(name)
    
    def _set_name(self, name: str) -> None:
        if not name or not name.strip():
            raise DomainException("Название группы не может быть пустым")
        
        if len(name) > 100:
            raise DomainException("Название группы не может быть длиннее 100 символов")
        
        self._name = name.strip()
    
    def add_member(self, user_id: str) -> None:
        """Добавить участника"""
        if user_id in self._member_ids:
            raise DomainException(f"Пользователь {user_id} уже в группе")
        
        if len(self._member_ids) >= self.MAX_MEMBERS:
            raise DomainException(f"Группа достигла максимума участников ({self.MAX_MEMBERS})")
        
        self._member_ids.append(user_id)
    
    def remove_member(self, user_id: str) -> None:
        """Удалить участника"""
        if user_id not in self._member_ids:
            raise DomainException(f"Пользователь {user_id} не состоит в группе")
        
        if user_id == self._owner_id:
            raise DomainException("Нельзя удалить владельца группы")
        
        self._member_ids.remove(user_id)
        
        # Если пользователь был администратором, убрать права
        if user_id in self._admin_ids:
            self._admin_ids.remove(user_id)
    
    def add_admin(self, user_id: str) -> None:
        """Назначить администратора"""
        if user_id not in self._member_ids:
            raise DomainException(f"Пользователь {user_id} не состоит в группе")
        
        if user_id not in self._admin_ids:
            self._admin_ids.append(user_id)
    
    def remove_admin(self, user_id: str) -> None:
        """Снять права администратора"""
        if user_id == self._owner_id:
            raise DomainException("Нельзя снять права администратора с владельца")
        
        if user_id in self._admin_ids:
            self._admin_ids.remove(user_id)
    
    def is_admin(self, user_id: str) -> bool:
        """Проверить, является ли пользователь администратором"""
        return user_id == self._owner_id or user_id in self._admin_ids
    
    def is_member(self, user_id: str) -> bool:
        """Проверить, состоит ли пользователь в группе"""
        return user_id in self._member_ids
    
    # === Геттеры ===
    
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def owner_id(self) -> str:
        return self._owner_id
    
    @property
    def member_ids(self) -> List[str]:
        return self._member_ids.copy()
    
    @property
    def admin_ids(self) -> List[str]:
        return self._admin_ids.copy()
    
    @property
    def member_count(self) -> int:
        return len(self._member_ids)
    
    # === Равенство по ID ===
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Group):
            return False
        return self._id == other._id
    
    def __hash__(self) -> int:
        return hash(self._id)
