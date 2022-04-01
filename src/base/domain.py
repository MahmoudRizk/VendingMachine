from dataclasses import dataclass, field
import uuid
from typing import Type, Dict


@dataclass
class Domain:
    _list_of_map = {}
    id: str = field(default=None)

    def set_uuid(self):
        if not self.id:
            self.id = str(uuid.uuid4())

    def to_dict(self):
        return self.__dict__

    def __post_init__(self):
        if self.id:
            self.id = str(self.id)

    @classmethod
    def list_of_field(cls, key: str, list_of_type: Type):
        cls._list_of_map.update({key: list_of_type})
        return field(default=None)

    @classmethod
    def get_list_of_map(cls) -> Dict:
        return cls._list_of_map
