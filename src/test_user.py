from unittest import TestCase

from sqlalchemy import create_engine

from src.mapper import UserMapper
from src.user_repository import UserRepository
from src import Base, db_user
from user import *
from db_user import DbUser


class TestUserDomain(TestCase):
    def test_new_user(self):
        _id = str(uuid.uuid4())
        user_name = "Test User 1"

        user = User(id=_id, name=user_name)

        self.assertEqual(user.id, _id)
        self.assertEqual(user.name, user_name)


class TestDbUser(TestCase):
    def test_new_user(self):
        _id = str(uuid.uuid4())
        user_name = "Test User 1"

        user = DbUser(id=_id, name=user_name)

        self.assertEqual(user.id, _id)
        self.assertEqual(user.name, user_name)


class TestUserMapper(TestCase):
    def test_data_to_domain(self):
        _id = str(uuid.uuid4())
        user_name = "Test User 1"

        db_user = DbUser(id=_id, name=user_name)

        mapper = UserMapper()

        domain_user = mapper.data_to_domain(db_user.__dict__, User)

        self.assertEqual(type(domain_user), User)
        self.assertEqual(domain_user.id, _id)
        self.assertEqual(domain_user.name, user_name)

    def test_domain_to_data(self):
        _id = str(uuid.uuid4())
        user_name = "Test User 1"

        domain_user = User(id=_id, name=user_name)

        mapper = UserMapper()

        domain_user_dict = domain_user.to_dict()
        db_user = mapper.domain_to_data(domain_user_dict, DbUser)

        self.assertEqual(type(db_user), DbUser)
        self.assertEqual(db_user.id, _id)
        self.assertEqual(db_user.name, user_name)


class TestUserRepository(TestCase):
    def setUp(self):
        db_url = "sqlite+pysqlite:///:memory:"
        engine = create_engine(db_url, future=True, echo=True)
        mapper = UserMapper()

        Base.metadata.create_all(engine)

        self.user_repository = UserRepository(engine=engine, mapper=mapper)

    def test_create_new_user(self):
        user_name = "Test User 1"

        domain_user = User(name=user_name)
        res: User = self.user_repository.insert(domain_user)

        self.assertTrue(res)
        self.assertTrue(res.id)
        self.assertEqual(res.name, domain_user.name)

    def test_update_user(self):
        _id = str(uuid.uuid4())
        user_name = "Test User 1"

        domain_user = User(id=_id, name=user_name)
        self.user_repository.insert(domain_user)

        new_user_name = "Test User 2"
        domain_user.name = new_user_name
        res: User = self.user_repository.insert(domain_user)
        
        self.assertEqual(res.id, str(_id))
        self.assertEqual(res.name, new_user_name)