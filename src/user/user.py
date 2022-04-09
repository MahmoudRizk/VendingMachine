from dataclasses import dataclass, field
from hashlib import sha256
from typing import List

from src.base.domain import Domain


@dataclass
class Role(Domain):
    name: str = field(default=None)
    user_id: str = field(default=None)


@dataclass
class User(Domain):
    name: str = field(default=None)
    deposit: float = field(default=0.0)
    is_admin: bool = field(default=False)
    roles: List[Role] = Domain.list_of_field(key="roles", list_of_type=Role)

    def __post_init__(self):
        super(User, self).__post_init__()
        self.roles = self.roles or []

    def add_role(self, role: str):
        role_added_before = any(it.name for it in self.roles if it.name == role)
        if not role_added_before:
            self.roles.append(Role(name=role, user_id=self.id))


def hash_password(password: str):
    return sha256(password.encode('utf-8')).hexdigest()
