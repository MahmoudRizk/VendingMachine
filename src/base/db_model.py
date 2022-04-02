from typing import Dict, List

from sqlalchemy import Column, TEXT

from src import Base


class DbModel:
    __table_args__ = {'extend_existing': True}
    id = Column(TEXT, primary_key=True)

    def to_dict(self) -> Dict:
        _db_model_attributes: List[str] = self._get_db_model_attributes()
        res = {}
        for attr in _db_model_attributes:
            _value = getattr(self, attr)
            if issubclass(type(_value), Base):
                # Skip relational objects.
                continue
            
            if issubclass(type(_value), list):
                _tmp_value = getattr(self, attr)
                _value = [it.to_dict() for it in _tmp_value]

            res.update({attr: _value})

        return res

    def _get_db_model_attributes(self) -> List[str]:
        # Get Database model columns and relations.
        return [key for key in self._sa_class_manager.__dict__["local_attrs"]]