from dataclasses import fields, Field
from typing import Dict, Type, Optional, List, Tuple

from src.base.db_model import DbModel
from src.base.domain import Domain


class TwoWayDict(dict):
    def __init__(self, mapped_entities: List[Tuple], *args, **kwargs):
        super(TwoWayDict, self).__init__(*args, **kwargs)
        for it in mapped_entities:
            self.__setitem__(it[0], it[1])

    def __setitem__(self, key, value):
        if key in self:
            del self[key]
        if value in self:
            del self[value]
        dict.__setitem__(self, key, value)
        dict.__setitem__(self, value, key)

    def __delitem__(self, key):
        dict.__delitem__(self, self[key])
        dict.__delitem__(self, key)


class Mapper:
    def __init__(self, mapped_entities: List[Tuple]):
        self.mapped_entities_dict = TwoWayDict(mapped_entities=mapped_entities)

    def data_to_domain(self, data: Dict, domain_class: Type[Domain], manual_mapper: Optional[Dict] = None) -> Domain:
        manual_mapper = manual_mapper or {}

        res = {}
        valid_keys, list_of_map = self._get_domain_class_fields(domain_class=domain_class)

        for key in valid_keys:
            key = key in manual_mapper and manual_mapper[key] or key
            if key in data:
                if issubclass(type(data[key]), list) and key in list_of_map:
                    _list_of_type = list_of_map[key]
                    res.update({key: [self.data_to_domain(it, _list_of_type) for it in data[key]]})
                else:
                    res.update({key: data[key]})

        return domain_class(**res)

    def domain_to_data(self, domain_data: Domain, model_class: Type[DbModel]) -> DbModel:
        res = {}
        domain_data_dict = domain_data.__dict__
        domain_class_fields, domain_list_of_map = self._get_domain_class_fields(domain_class=type(domain_data))

        for key, value in domain_data_dict.items():
            if key in domain_class_fields:
                if key in domain_list_of_map and issubclass(type(value), list):
                    # support one to many mapping
                    _domain_list_of_type = domain_list_of_map[key]
                    _db_mapped_type: Type = self.mapped_entities_dict[_domain_list_of_type]
                    res.update({key: [self.domain_to_data(it, _db_mapped_type) for it in value]})
                else:
                    res.update({key: value})

        return model_class(**res)

    def _get_domain_class_fields(self, domain_class: Type[Domain]) -> Tuple[List[str], Dict]:
        fields_list: List[Field] = fields(domain_class)
        return [it.name for it in fields_list], domain_class.get_list_of_map()
