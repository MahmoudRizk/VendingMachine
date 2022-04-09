from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from src.base.repository import Repository
from src.user.db_role import DbRole
from src.user.mapper import UserMapper
from src.user.user import User, hash_password, Role
from src.user.db_user import DbUser


def get_user_repository(engine):
    mapped_entities = [
        (User, DbUser),
        (Role, DbRole)
    ]
    mapper = UserMapper(mapped_entities=mapped_entities)
    return UserRepository(engine=engine, mapper=mapper)


class UserRepository(Repository):
    def __init__(self, engine, mapper: UserMapper):
        db_model_type: DbUser = DbUser
        domain_model_type: User = User
        super(UserRepository, self).__init__(engine=engine, mapper=mapper, db_model_type=db_model_type,
                                             domain_model_type=domain_model_type)

    def get_by_user_name(self, user_name: str) -> Optional[User]:
        with Session(self.engine) as session:
            stmt = select(self.db_model_type).where(self.db_model_type.name == user_name)
            try:
                db_user = session.scalars(stmt).one()
                return self.mapper.data_to_domain(db_user.to_dict(), self.domain_model_type)
            except NoResultFound as e:
                return None

    def set_user_password(self, user_id: str, password: str) -> bool:
        with Session(self.engine) as session:
            try:
                db_user: DbUser = self._get_by_id(session=session, _id=user_id)
                hashed_password = hash_password(password=password)
                db_user.password = hashed_password
                session.add(db_user)
                session.commit()
                return True
            except Exception as e:
                return False

    def validate_user_password(self, user_id: str, password: str) -> bool:
        try:
            with Session(self.engine) as session:
                db_user: DbUser = self._get_by_id(session=session, _id=user_id)
                return db_user.password == hash_password(password=password)
        except Exception as e:
            return False

    def create_or_update_admin(self, password: str):
        admin_user_name = "administrator"
        user = self.get_by_user_name(admin_user_name)
        if not user:
            user = User(name=admin_user_name, is_admin=True)
            self.insert(user)

        self.set_user_password(user_id=user.id, password=password)
