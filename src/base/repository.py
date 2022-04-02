from typing import Optional, Type, List

from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from src.base.db_model import DbModel
from src.base.domain import Domain
from src.base.mapper import Mapper


class Repository:
    def __init__(self, engine, mapper: Mapper, db_model_type: Type[DbModel], domain_model_type: Type[Domain]):
        self.engine = engine
        self.mapper = mapper
        self.db_model_type = db_model_type
        self.domain_model_type = domain_model_type

    def insert(self, domain_model: Domain) -> Domain:
        self._set_uuid_if_missing(domain_model)

        with Session(self.engine) as session:
            db_model = self.mapper.domain_to_data(domain_model, self.db_model_type)

            stmt_res = self._get_by_id(session=session, _id=db_model.id)

            if not stmt_res:
                # Insert new record
                session.add(db_model)
                session.commit()
                session.refresh(db_model)
                return self.mapper.data_to_domain(db_model.to_dict(), self.domain_model_type)
            else:
                # Update Existing record
                self._update_db_with_new_values(new_db_model=stmt_res, old_db_model=db_model)
                session.commit()
                session.refresh(stmt_res)
                return self.mapper.data_to_domain(stmt_res.to_dict(), self.domain_model_type)

    def get_by_id(self, _id: str) -> Optional[Domain]:
        with Session(self.engine) as session:
            db_model: Optional[DbModel] = self._get_by_id(session=session, _id=_id)
            if db_model:
                return self.mapper.data_to_domain(db_model.to_dict(), self.domain_model_type)

            return None

    def _get_by_id(self, session, _id: str) -> Optional[DbModel]:
        stmt = select(self.db_model_type).where(self.db_model_type.id == _id)
        try:
            stmt_res = session.scalars(stmt).one()
        except NoResultFound as e:
            stmt_res = None

        return stmt_res

    def _set_uuid_if_missing(self, domain_model: Domain) -> None:
        domain_model.set_uuid()

        for key, domain_type in domain_model.get_list_of_map().items():
            _child_list = getattr(domain_model, key)
            for it in _child_list:
                it.set_uuid()

    def _update_db_with_new_values(self, new_db_model: DbModel, old_db_model: DbModel) -> None:
        _db_attributes_names: List[str] = [key for key in old_db_model.__dict__ if not key.startswith("_")]
        for key in _db_attributes_names:
            if key in new_db_model.__dict__:
                setattr(new_db_model, key, getattr(old_db_model, key))

