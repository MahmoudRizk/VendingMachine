from typing import Tuple, Optional, Callable

from api import authentication_secret_key, engine
from service.authentication.token_generator import TokenGenerator
from src.user.user import User
from src.user.user_repository import get_user_repository
import json


class Authorize:
    def __init__(self, request):
        self.request = request

    def is_authorized(self) -> Tuple[bool, Optional[User]]:
        token = self.request.headers.get("token")

        return self.get_user_from_token(token=token)

    def has_permission(self, permission_func: Callable, **kwargs) -> Tuple[bool, str]:
        valid, user = self.is_authorized()
        if not valid:
            return False, "Not authorized"

        is_admin, _ = self.is_admin()
        if is_admin:
            return True, ""

        _has_perm, message = permission_func(user=user, **kwargs)
        return _has_perm, message

    def is_admin(self) -> Tuple[bool, str]:
        valid, user = self.is_authorized()
        if not valid:
            return False, "Not authorized"

        if user.is_admin:
            return True, ""

        return False, "Not admin"

    def has_role(self, role: str) -> Tuple[bool, str]:
        return self.has_permission(self._has_role, role=role)

    def _has_role(self, user: User, role: str) -> Tuple[bool, str]:
        valid: bool = any(it.name == role for it in user.roles)
        if not valid:
            return False, "Must have {0} permission to complete this action.".format(role)
        return True, ""

    def get_user_from_token(self, token: str) -> Tuple[bool, Optional[User]]:
        if not token:
            return False, None

        token_generator = TokenGenerator(key=authentication_secret_key)
        res = token_generator.decrypt(token)
        if res.success:
            _dict = json.loads(res.data)
            user_id = _dict.get("user_id", None)
            if not user_id:
                return False, None
            user_repository = get_user_repository(engine)
            user = user_repository.get_by_id(_id=user_id)
            if not user:
                return False, None

            return True, user
        return False, None
