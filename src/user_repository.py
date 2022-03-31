from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from src.mapper import UserMapper
from user import User
from db_user import DbUser

from sqlalchemy.orm import Session


class UserRepository:
    def __init__(self, engine, mapper: UserMapper):
        self.mapper = mapper
        self.engine = engine

    def insert(self, user: User) -> User:
        if not user.id:
            user.set_uuid()

        with Session(self.engine) as session:
            db_user = self.mapper.domain_to_data(user.to_dict(), DbUser)

            stmt_res = self._get_by_id(session=session, _id=db_user.id)

            if not stmt_res:
                # Insert new record.
                session.add(db_user)
                res = self.mapper.data_to_domain(db_user.__dict__, User)
            else:
                # Update Existing record.
                stmt_res.__dict__.update(db_user.__dict__)
                res = self.mapper.data_to_domain(stmt_res.__dict__, User)

            session.commit()
            return res

    def get_by_id(self, _id: str) -> User:
        with Session(self.engine) as session:
            db_user: Optional[DbUser] = self._get_by_id(session=session, _id=_id)
            if db_user:
                return self.mapper.data_to_domain(db_user.__dict__, User)

            return None

    def _get_by_id(self, session, _id: str) -> Optional[DbUser]:
        stmt = select(DbUser).where(DbUser.id == _id)
        try:
            stmt_res = session.scalars(stmt).one()
        except NoResultFound as e:
            stmt_res = None

        return stmt_res
