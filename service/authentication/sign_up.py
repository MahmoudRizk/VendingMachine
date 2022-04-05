from src.user.user import User, Role
from src.user.user_repository import UserRepository

from service.base_service_response import ServiceResponse as Response


class SignUp:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def sign_up(self, user_name: str, password: str) -> Response:
        is_duplicated_user = self._is_duplicated_user_name(user_name=user_name)
        if is_duplicated_user:
            return Response(success=False, message="User Name {0} is used before".format(user_name))

        default_role = Role(name="Buyer")
        user = User(name=user_name, roles=[default_role])

        user = self.user_repository.insert(user)

        passwd_success = self.user_repository.set_user_password(user_id=user.id, password=password)

        if not passwd_success:
            return Response(success=False,
                            message="failed to set password to user {0}, please contact support".format(user_name))

        return Response(success=True)

    def _is_duplicated_user_name(self, user_name: str):
        user = self.user_repository.get_by_user_name(user_name=user_name)
        return bool(user)
