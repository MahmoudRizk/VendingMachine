from typing import List, Optional, Dict, Tuple

from flask import Request, make_response

from service.authorize.authorize import Authorize


class BaseApiResponse:
    def __init__(self, code: int = 200, message: str = "", data: Optional[Dict] = None):
        if not data:
            data = {}

        self.code = code
        self.message = message
        self.data = data

    def to_dict(self) -> Dict:
        return {
            "code": self.code,
            "message": self.message,
            "data": self.data
        }


class BaseApi:
    def __init__(self, request: Request, methods: List[str]):
        self.request = request
        self.methods = methods
        self.authorizer = Authorize(request)
        self.is_authorized, self.session_user = self.get_session_user()

    def validate_parameters(self, params: List[str], request_params: Dict) -> Tuple[bool, Optional[BaseApiResponse]]:
        for it in params:
            if it not in request_params:
                message = "Missing parameter, {0} is a required parameter".format(it)
                return False, self.respond(code=417, message=message)

        return True, None

    def respond(self, code: int = 200, message: str = "", data: Optional[Dict] = None):
        return make_response(BaseApiResponse(code=code, message=message, data=data).to_dict(), code)

    def execute(self, **kwargs) -> BaseApiResponse:
        pass

    def get_session_user(self) -> Tuple[bool, Optional["User"]]:
        return self.authorizer.is_authorized()
