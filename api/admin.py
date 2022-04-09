from typing import List

from flask import Request, request

from api import app, engine
from api.base_api import BaseApi
from src.user.user import User
from src.user.user_repository import get_user_repository


class AdminApi(BaseApi):
    def __init__(self, request: Request, methods: List[str]):
        super(AdminApi, self).__init__(request=request, methods=methods)

        self.methods_map = {
            "get_users": self.get_users,
            "get_user_details": self.get_user_details,
            "create_user": self.create_user,
            "update_user": self.update_user,
            "add_user_role": self.add_user_role,
        }

    def execute(self, method_name: str, **kwargs):
        valid, message = self.authorizer.is_admin()
        if not valid:
            return self.respond(code=403, message=message)
        return self.methods_map[method_name](**kwargs)

    def get_users(self):
        user_repository = get_user_repository(engine=engine)
        users = user_repository.get_all()
        data = [
            {
                "id": it.id,
                "name": it.name,
                "deposit": it.deposit,
                "is_admin": it.is_admin
            }
            for it in users
        ]

        return self.respond(code=200, data=data)

    def get_user_details(self, user_id: str):
        user_repository = get_user_repository(engine=engine)
        user = user_repository.get_by_id(_id=user_id)
        if not user:
            return self.respond(code=404)

        data = {
            "id": user.id,
            "name": user.name,
            "deposit": user.deposit,
            "is_admin": user.is_admin,
            "roles": [
                {
                    "name": it.name
                }
                for it in user.roles
            ]
        }

        return self.respond(code=200, data=data)

    def create_user(self):
        request_json_body_data = self.request.get_json()

        required_parameters = ["user_name", "password"]
        valid, response = self.validate_parameters(params=required_parameters, request_params=request_json_body_data)
        if not valid:
            return response

        user_repository = get_user_repository(engine=engine)
        user_name = request_json_body_data["user_name"]
        password = request_json_body_data["password"]
        deposit = request_json_body_data.get("deposit", 0)
        is_admin = request_json_body_data.get("is_admin", False)

        exists_before = user_repository.get_by_user_name(user_name=user_name)
        if exists_before:
            return self.respond(code=417, message="User Name {0} exists before.".format(user_name))

        user = User(name=user_name, deposit=deposit, is_admin=is_admin)
        user_repository.insert(user)
        user_repository.set_user_password(user.id, password)

        data = {
            "user_id": user.id
        }

        return self.respond(code=200, data=data)

    def update_user(self, user_id: str):
        request_json_body_data = self.request.get_json()

        user_repository = get_user_repository(engine=engine)
        user = user_repository.get_by_id(_id=user_id)
        if not user:
            return self.respond(code=404)

        user_attrs = ["user_name", "deposit", "is_admin"]
        for key, value in request_json_body_data.items():
            if key in user_attrs:
                if key == "user_name":
                    key = "name"
                setattr(user, key, value)

        user_repository.insert(user)

        if request_json_body_data.get("password"):
            password = request_json_body_data["password"]
            user_repository.set_user_password(user_id=user.id, password=password)

        data = {
            "id": user.id,
            "name": user.name,
            "deposit": user.deposit,
            "is_admin": user.is_admin
        }

        return self.respond(code=200, data=data)

    def add_user_role(self, user_id: str):
        request_json_body_data = self.request.get_json()

        user_repository = get_user_repository(engine=engine)
        user = user_repository.get_by_id(_id=user_id)
        if not user:
            return self.respond(code=404)

        required_parameters = ["role"]
        valid, response = self.validate_parameters(params=required_parameters, request_params=request_json_body_data)
        if not valid:
            return response

        role = request_json_body_data["role"]
        if role not in ["Seller", "Buyer"]:
            return self.respond(code=417, message="Invalid role {0}, role must be Seller or Buyer".format(role))

        user.add_role(role=role)
        user_repository.insert(user)

        data = {
            "id": user.id,
            "name": user.name,
            "roles": [
                {
                    "name": it.name
                }
                for it in user.roles
            ]
        }

        return self.respond(code=200, data=data)


@app.route("/admin/users", methods=["GET"])
def get_users():
    return AdminApi(request=request, methods=["GET"]).execute(method_name="get_users")


@app.route("/admin/users/<string:user_id>", methods=["GET"])
def get_user_details(user_id: str):
    return AdminApi(request=request, methods=["GET"]).execute(method_name="get_user_details", user_id=user_id)


@app.route("/admin/users", methods=["POST"])
def create_user():
    return AdminApi(request=request, methods=["POST"]).execute(method_name="create_user")


@app.route("/admin/users/<string:user_id>", methods=["PUT"])
def update_user(user_id: str):
    return AdminApi(request=request, methods=["PUT"]).execute(method_name="update_user", user_id=user_id)


@app.route("/admin/users/<string:user_id>/add_role", methods=["POST"])
def add_user_role(user_id: str):
    return AdminApi(request=request, methods=["POST"]).execute(method_name="add_user_role", user_id=user_id)
