from src.base.repository import Repository
from src.mapper import UserMapper
from user import User
from db_user import DbUser


class UserRepository(Repository):
    def __init__(self, engine, mapper: UserMapper):
        db_model_type = DbUser
        domain_model_type = User
        super(UserRepository, self).__init__(engine=engine, mapper=mapper, db_model_type=db_model_type,
                                             domain_model_type=domain_model_type)
