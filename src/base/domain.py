from dataclasses import dataclass, field
import uuid


@dataclass
class Domain:
    id: str = field(default=None)

    def set_uuid(self):
        if not self.id:
            self.id = str(uuid.uuid4())

    def to_dict(self):
        return self.__dict__

    def __post_init__(self):
        if self.id:
            self.id = str(self.id)
