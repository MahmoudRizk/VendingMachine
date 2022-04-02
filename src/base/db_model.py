from typing import Dict, List

from sqlalchemy import Column, TEXT


class DbModel:
    __table_args__ = {'extend_existing': True}
    id = Column(TEXT, primary_key=True)

    def to_dict(self) -> Dict:
        _db_model_attributes: List[str] = self._get_db_model_attributes()
        res = {}
        for attr in _db_model_attributes:
            res.update({attr: getattr(self, attr)})

        return res

    def _get_db_model_attributes(self) -> List[str]:
        # Get Database model columns and relations.
        return [key for key in self._sa_class_manager.__dict__["local_attrs"]]