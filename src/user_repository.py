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

            stmt = select(DbUser).where(DbUser.id == db_user.id)
            try:
                stmt_res = session.scalars(stmt).one()
            except NoResultFound as e:
                stmt_res = None

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

    def get_by_id(self, id: str) -> User:
        pass
