import json
from typing import Optional, List
from unittest import TestCase

from sqlalchemy import create_engine

from service.authentication.sign_in import SignIn
from service.authentication.sign_up import SignUp
from service.authentication.token_generator import TokenGenerator
from service.base_service_response import ServiceResponse
from src import Base
from src.user.db_role import DbRole
from src.user.db_user import DbUser
from src.user.mapper import UserMapper
from src.user.user import User, Role
from src.user.user_repository import UserRepository


class TestSignUp(TestCase):
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

    def test_signup_success(self):
        user_name = "test@test.com"
        password = "12345678"

        sign_up_service = SignUp(user_repository=self.user_repository)
        res = sign_up_service.sign_up(user_name=user_name, password=password)

        self.assertEqual(type(res), ServiceResponse)
        self.assertEqual(res.success, True)

    def test_signup_with_duplicated_username(self):
        user_name = "test@test.com"
        password = "12345678"

        sign_up_service = SignUp(user_repository=self.user_repository)

        first_attempt = sign_up_service.sign_up(user_name=user_name, password=password)
        self.assertEqual(first_attempt.success, True)

        second_attempt = sign_up_service.sign_up(user_name=user_name, password=password)
        self.assertEqual(second_attempt.success, False)
        self.assertTrue(second_attempt.message)


class TestSignIn(TestCase):
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

        self._create_test_users()

    def test_signin_success(self):
        user: User = User(name="test@test.com")
        self.user_repository.insert(user)

        self.user_repository.set_user_password(user_id=user.id, password="12345678")

        sign_in_service = SignIn(user_repository=self.user_repository)
        res = sign_in_service.sign_in(user_name="test@test.com", password="12345678")

        self.assertEqual(type(res), ServiceResponse)
        self.assertEqual(res.success, True)

    def test_signin_with_wrong_username(self):
        sign_in_service = SignIn(user_repository=self.user_repository)
        res = sign_in_service.sign_in(user_name="test@test.com", password="12345678")

        self.assertEqual(res.success, False)

    def test_signin_with_wrong_password(self):
        user: User = User(name="test@test.com")
        self.user_repository.insert(user)

        self.user_repository.set_user_password(user_id=user.id, password="12345678")

        sign_in_service = SignIn(user_repository=self.user_repository)
        res = sign_in_service.sign_in(user_name="test@test.com", password="555555")

        self.assertEqual(type(res), ServiceResponse)
        self.assertEqual(res.success, False)

    def _create_test_users(self, test_users: Optional[List] = None):
        if not test_users:
            test_users = [
                ("test1@test.com", "12345678"),
                ("test2@test.com", "2342qq43"),
                ("test3@test.com", "24352454"),
                ("test4@test.com", "24353244")
            ]

            for it in test_users:
                user: User = User(name=it[0])
                self.user_repository.insert(user)
                self.user_repository.set_user_password(user_id=user.id, password=it[1])


class TestTokenGenerator(TestCase):
    def setUp(self):
        key = "DK2zBekJCArhrituq6sc5sfAF8pQTkKut3D1mp9_GhI='"

        self.token_generator = TokenGenerator(key=key)

    def test_encrypt_success(self):
        test_samples = [
            "Test Sample",
            json.dumps({"a": "abc", "b": "xyz", "c": 1234})
        ]

        for it in test_samples:
            response = self.token_generator.encrypt(it)
            self.assertTrue(response.success)

    def test_decrypt_success(self):
        test_samples = [
            "Test Sample",
            json.dumps({"a": "abc", "b": "xyz", "c": 1234}),
            "X" * 10000
        ]

        for it in test_samples:
            response = self.token_generator.encrypt(it)
            response = self.token_generator.decrypt(response.data)
            
            self.assertTrue(response.success)
            self.assertEqual(response.data, it)

    def test_decrypt_with_wrong_key(self):
        wrong_key = "X1Ul7Y3aR4ITazL-LzZSqVdhq8MIORbUZE-WmmTzjaA="

        text = "Test Sample 123"
        response = self.token_generator.encrypt(text)

        wrong_token_generator = TokenGenerator(key=wrong_key)
        
        # with self.assertRaises()
        response = wrong_token_generator.decrypt(response.data)
        
        self.assertFalse(response.success)
