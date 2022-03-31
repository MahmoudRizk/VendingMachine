from src.base.repository import Repository
from src.user.mapper import UserMapper
from src.user.user import User
from src.user.db_user import DbUser


class UserRepository(Repository):
    def __init__(self, engine, mapper: UserMapper):
        db_model_type = DbUser
        domain_model_type = User
        super(UserRepository, self).__init__(engine=engine, mapper=mapper, db_model_type=db_model_type,
                                             domain_model_type=domain_model_type)
