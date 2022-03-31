from typing import Dict, Type, Optional

from src.base.mapper import Mapper
from src.user.user import User
from src.user.db_user import DbUser


class UserMapper(Mapper):
    def data_to_domain(self, data: Dict, domain_class: Type[User], manual_mapper: Optional[Dict] = None) -> User:
        return super().data_to_domain(data=data, domain_class=domain_class, manual_mapper=manual_mapper)

    def domain_to_data(self, domain_data: Dict, model_class: Type[DbUser]) -> DbUser:
        return super().domain_to_data(domain_data=domain_data, model_class=model_class)
