import uuid
from unittest import TestCase

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.base.mapper import TwoWayDict
from src.user.db_role import DbRole
from src.user.mapper import UserMapper
from src.user.user_repository import UserRepository
from src import Base
from src.user.user import *
from src.user.db_user import DbUser


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
    def setUp(self):
        self.mapped_entities = [
            (User, DbUser),
            (Role, DbRole)
        ]

    def test_data_to_domain(self):
        _id = str(uuid.uuid4())
        user_name = "Test User 1"

        db_user = DbUser(id=_id, name=user_name)

        mapper = UserMapper(self.mapped_entities)

        domain_user = mapper.data_to_domain(db_user.to_dict(), User)

        self.assertEqual(type(domain_user), User)
        self.assertEqual(domain_user.id, _id)
        self.assertEqual(domain_user.name, user_name)

    def test_data_to_domain_with_child_list(self):
        _id = str(uuid.uuid4())
        user_name = "Test User 1"
        roles = [DbRole(name="Seller", user_id=_id)]

        db_user = DbUser(id=_id, name=user_name, roles=roles)

        mapper = UserMapper(self.mapped_entities)

        domain_user = mapper.data_to_domain(db_user.to_dict(), User)

        self.assertEqual(type(domain_user), User)
        self.assertEqual(domain_user.id, _id)
        self.assertEqual(domain_user.name, user_name)
        for it1, it2 in zip(domain_user.roles, db_user.roles):
            self.assertEqual(type(it1), Role)
            self.assertEqual(it1.name, it2.name)
            self.assertEqual(it1.user_id, it2.user_id)

    def test_domain_to_data(self):
        _id = str(uuid.uuid4())
        user_name = "Test User 1"

        domain_user = User(id=_id, name=user_name)

        mapper = UserMapper(self.mapped_entities)

        db_user = mapper.domain_to_data(domain_user, DbUser)

        self.assertEqual(type(db_user), DbUser)
        self.assertEqual(db_user.id, _id)
        self.assertEqual(db_user.name, user_name)

    def test_domain_to_data_with_child_list(self):
        _id = str(uuid.uuid4())
        user_name = "Test User 1"
        roles = [Role(name="Buyer", user_id=_id)]

        domain_user = User(id=_id, name=user_name, roles=roles)

        mapper = UserMapper(self.mapped_entities)

        db_user = mapper.domain_to_data(domain_user, DbUser)

        self.assertEqual(type(db_user), DbUser)
        self.assertEqual(db_user.id, _id)
        self.assertEqual(db_user.name, user_name)
        for it1, it2 in zip(db_user.roles, domain_user.roles):
            self.assertEqual(type(it1), DbRole)
            self.assertEqual(it1.name, it2.name)
            self.assertEqual(it1.user_id, it2.user_id)


class TestUserRepository(TestCase):
    def setUp(self):
        db_url = "sqlite+pysqlite:///:memory:"
        self.engine = create_engine(db_url, future=True, echo=True)
        Base.metadata.create_all(self.engine)

        mapped_entities = [
            (User, DbUser),
            (Role, DbRole)
        ]
        mapper = UserMapper(mapped_entities=mapped_entities)

        self.user_repository = UserRepository(engine=self.engine, mapper=mapper)

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

    def test_get_missing_user(self):
        _id = str(uuid.uuid4())

        res = self.user_repository.get_by_id(_id)

        self.assertFalse(res)

    def test_get_existing_user(self):
        _id1 = str(uuid.uuid4())
        _id2 = str(uuid.uuid4())

        with Session(self.engine) as session:
            db_user_1 = DbUser(id=_id1, name="Test User 1")
            db_user_2 = DbUser(id=_id2, name="Test User 2")

            session.add_all([db_user_1, db_user_2])
            session.commit()

        res = self.user_repository.get_by_id(_id=_id1)

        self.assertEqual(res.id, _id1)

    def test_create_new_user_with_roles(self):
        user_name = "Test User 1"
        roles = [Role(name="Seller")]

        domain_user = User(name=user_name, roles=roles)
        res: User = self.user_repository.insert(domain_user)

        self.assertTrue(res)
        self.assertTrue(res.id)
        self.assertTrue(res.roles)
        self.assertEqual(res.name, user_name)
        for it in res.roles:
            self.assertTrue(it.id)
            self.assertEqual(it.name, "Seller")
            self.assertTrue(it.user_id)
            self.assertEqual(it.user_id, res.id)

    def test_add_role_to_previously_created_user(self):
        user_name = "Test User 1"
        roles = [Role(name="Seller")]

        domain_user = User(name=user_name)
        self.user_repository.insert(domain_model=domain_user)

        domain_user.roles = roles
        res: User = self.user_repository.insert(domain_model=domain_user)

        self.assertTrue(res)
        self.assertTrue(res.id)
        self.assertFalse(res.roles)
        self.assertEqual(res.name, user_name)
        for it in res.roles:
            self.assertTrue(it.id)
            self.assertEqual(it.name, "Seller")
            self.assertTrue(it.user_id)
            self.assertEqual(it.user_id, res.id)

    def test_update_role_to_previously_created_user(self):
        user_name = "Test User 1"
        roles = [Role(name="Seller")]

        domain_user = User(name=user_name, roles=roles)
        domain_user: User = self.user_repository.insert(domain_model=domain_user)

        domain_user.roles[0].name = "Buyer"
        res: User = self.user_repository.insert(domain_model=domain_user)

        self.assertTrue(res)
        self.assertTrue(res.id)
        self.assertTrue(res.roles)
        self.assertEqual(res.name, user_name)
        for it in res.roles:
            self.assertTrue(it.id)
            self.assertEqual(it.name, "Buyer")
            self.assertTrue(it.user_id)
            self.assertEqual(it.user_id, res.id)

