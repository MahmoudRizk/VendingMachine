from src.user.user import User
from src.user.user_repository import UserRepository

from service.base_service_response import ServiceResponse as Response


class SignIn:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def sign_in(self, user_name: str, password: str) -> Response:
        user: User = self.user_repository.get_by_user_name(user_name=user_name)
        if not user:
            return Response(success=False, message="User Name {0} doesn't exist".format(user_name))

        is_correct_password = self.user_repository.validate_user_password(user_id=user.id, password=password)

        if not is_correct_password:
            return Response(success=False, message="Incorrect password for user name {0}".format(user_name))

        return Response(success=True)
