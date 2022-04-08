import json

from flask import request

from api import app, engine, authentication_secret_key
from api.base_api import BaseApi
from service.authentication.sign_in import SignIn
from service.authentication.token_generator import TokenGenerator
from src.user.user_repository import get_user_repository


class SingInApi(BaseApi):
    def execute(self):
        request_json_body_data = self.request.get_json()
        required_parameters = ["user_name", "password"]
        valid, response = self.validate_parameters(params=required_parameters, request_params=request_json_body_data)
        if not valid:
            return response

        user_name = request_json_body_data["user_name"]
        password = request_json_body_data["password"]
        user_repository = get_user_repository(engine)
        sign_in_service = SignIn(user_repository=user_repository)
        res = sign_in_service.sign_in(user_name=user_name, password=password)

        data = {}
        if res.success:
            code = 200
            token_generator = TokenGenerator(key=authentication_secret_key)
            token_content = json.dumps({"user_id": res.data["user_id"]})
            token = token_generator.encrypt(token_content)
            data.update({"token": str(token.data)})
        else:
            code = 417

        return self.respond(code=code, message=res.message, data=data)


@app.route("/sign_in", methods=["POST"])
def sign_in():
    return SingInApi(request=request, methods=["POST"]).execute()
