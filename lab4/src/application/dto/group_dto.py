from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class GroupDTO:
    """Read DTO: Группа"""
    
    id: str
    name: str
    owner_id: str
    member_count: int
    admin_ids: List[str]
