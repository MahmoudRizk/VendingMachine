from dataclasses import dataclass, field
import uuid
from hashlib import sha256


@dataclass
class User:
    id: str = field(default=None)
    name: str = field(default=None)

    def set_uuid(self):
        if not self.id:
            self.id = str(uuid.uuid4())

    def to_dict(self):
        return self.__dict__

    def __post_init__(self):
        if self.id:
            self.id = str(self.id)


def hash_password(password: str):
    return sha256(password.encode('utf-8')).hexdigest()
