from typing import Optional, Type

from sqlalchemy import select
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
        if not domain_model.id:
            domain_model.set_uuid()

        with Session(self.engine) as session:
            db_model = self.mapper.domain_to_data(domain_model.to_dict(), self.db_model_type)

            stmt_res = self._get_by_id(session=session, _id=db_model.id)

            if not stmt_res:
                # Insert new record
                session.add(db_model)
                res = self.mapper.data_to_domain(db_model.__dict__, self.domain_model_type)
            else:
                # Update Existing record
                stmt_res.__dict__.update(db_model.__dict__)
                res = self.mapper.data_to_domain(stmt_res.__dict__, self.domain_model_type)

            session.commit()
            return res

    def get_by_id(self, _id: str) -> Optional[Domain]:
        with Session(self.engine) as session:
            db_model: Optional[DbModel] = self._get_by_id(session=session, _id=_id)
            if db_model:
                return self.mapper.data_to_domain(db_model.__dict__, self.domain_model_type)

            return None

    def _get_by_id(self, session, _id: str) -> Optional[Domain]:
        stmt = select(self.db_model_type).where(self.db_model_type.id == _id)
        try:
            stmt_res = session.scalars(stmt).one()
        except NoResultFound as e:
            stmt_res = None

        return stmt_res
