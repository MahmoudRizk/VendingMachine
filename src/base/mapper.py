from dataclasses import fields, Field
from typing import Dict, Type, Optional, List, Tuple

from src.base.db_model import DbModel
from src.base.domain import Domain


class Mapper:
    def data_to_domain(self, data: Dict, domain_class: Type[Domain], manual_mapper: Optional[Dict] = None) -> Domain:
        manual_mapper = manual_mapper or {}

        res = {}
        valid_keys, list_of_map = self._get_domain_class_fields(domain_class=domain_class)

        for key in valid_keys:
            key = key in manual_mapper and manual_mapper[key] or key
            if key in data:
                if issubclass(type(data[key]), list) and key in list_of_map:
                    _list_of_type = list_of_map[key]
                    res.update({key: [self.data_to_domain(it.__dict__, _list_of_type) for it in data[key]]})
                else:
                    res.update({key: data[key]})

        return domain_class(**res)

    def domain_to_data(self, domain_data: Dict, model_class: Type[DbModel]) -> DbModel:
        return model_class(**domain_data)

    def _get_domain_class_fields(self, domain_class: Type[Domain]) -> Tuple[List[str], Dict]:
        fields_list: List[Field] = fields(domain_class)
        return [it.name for it in fields_list], domain_class.get_list_of_map()
