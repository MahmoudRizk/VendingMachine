from flask import request

from api import app, engine
from service.authentication.sign_up import SignUp
from src.user.user_repository import get_user_repository


@app.route("/sign_up", methods=["POST"])
def sign_up():
    json_body_data = request.get_json()

    # TODO: Refactor required parameters logic.
    # TODO: Return error status code.
    if "user_name" not in json_body_data:
        return {
            "success": False,
            "message": "user_name is required"
        }

    if "password" not in json_body_data or not json_body_data["password"]:
        return {
            "success": False,
            "message": "password is required"
        }

    user_name = json_body_data["user_name"]
    password = json_body_data["password"]
    user_repository = get_user_repository(engine)
    sign_up_service = SignUp(user_repository=user_repository)
    res = sign_up_service.sign_up(user_name=user_name, password=password)

    return {
        "success": res.success,
        "message": res.message
    }
