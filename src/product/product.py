from dataclasses import dataclass, field

from src.base.domain import Domain


@dataclass
class Product(Domain):
    name: str = field(default=None)
    country_of_origin: str = field(default=None)
    calories: float = field(default=0.0)
    flavor: str = field(default=None)
