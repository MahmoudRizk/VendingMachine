from typing import Dict, Type, Optional

from src.user import User
from src.db_user import DbUser


class UserMapper:
    def data_to_domain(self, data: Dict, domain_class: Type[User], manual_mapper: Optional[Dict] = None) -> User:
        manual_mapper = manual_mapper or {}

        res = {}
        valid_keys = domain_class.__dict__

        for key in valid_keys:
            key = key in manual_mapper and manual_mapper[key] or key
            if key in data:
                res.update({key: data[key]})

        return domain_class(**res)

    def domain_to_data(self, domain_data: Dict, model_class: Type[DbUser]) -> DbUser:
        return model_class(**domain_data)
