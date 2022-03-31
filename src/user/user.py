from dataclasses import dataclass, field
from hashlib import sha256

from src.base.domain import Domain


@dataclass
class User(Domain):
    name: str = field(default=None)


def hash_password(password: str):
    return sha256(password.encode('utf-8')).hexdigest()
