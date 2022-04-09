from typing import Optional, List

from flask import jsonify, request, Request

from api import app, engine
from api.base_api import BaseApi
from service.authorize.authorize import Authorize
from service.vending_machine import VendingMachineService
from src.user.user import User
from src.user.user_repository import get_user_repository
from src.vending_machine.vending_machine import VendingMachine, VendingMachineInventory
from src.vending_machine.vending_machine_repository import get_vending_machine_repository


def has_update_inventory_permission(user: User, inventory_line: VendingMachineInventory):
    valid: bool = any(it.name == "Seller" for it in user.roles)
    if not valid:
        return False, "Must have Seller permission to complete this action"

    if user.id != inventory_line.seller_id:
        return False, "user {0} is not allowed to edit this inventory record {1}".format(user.id, inventory_line.id)

    return True, ""


class VendingMachinesApi(BaseApi):
    def __init__(self, request: Request, methods: List[str]):
        super(VendingMachinesApi, self).__init__(request=request, methods=methods)

        self.methods_map = {
            "get_vending_machines": self.get_vending_machines,
            "get_vending_machine_details": self.get_vending_machine_details,
            "create_vending_machine": self.create_vending_machine,
            "update_vending_machine": self.update_vending_machine,
            "update_vending_machine_inventory": self.update_vending_machine_inventory,
            "add_user_deposit": self.add_user_deposit

        }

    def execute(self, method_name: str, **kwargs):
        return self.methods_map[method_name](**kwargs)

    def get_vending_machines(self):
        vending_machine_repository = get_vending_machine_repository(engine=engine)
        vending_machines = vending_machine_repository.get_all()
        data = [
            {
                "id": it.id,
                "name": it.name,
                "model_number": it.model_number,
                "location": it.location
            }
            for it in vending_machines
        ]

        return self.respond(code=200, data=data)

    def get_vending_machine_details(self, vending_machine_id: str):
        vending_machine_repository = get_vending_machine_repository(engine=engine)
        vending_machine = vending_machine_repository.get_by_id(_id=vending_machine_id)
        if not vending_machine:
            return self.respond(code=404)

        data = {
            "id": vending_machine.id,
            "name": vending_machine.name,
            "model_number": vending_machine.model_number,
            "location": vending_machine.location,
            "inventory": [
                {
                    "product_id": it.product_id,
                    "seller_id": it.seller_id,
                    "amount_available": it.amount_available,
                    "cost": it.cost
                }
                for it in vending_machine.inventory
            ]
        }

        return self.respond(code=200, data=data)

    def create_vending_machine(self):
        valid, message = self.authorizer.is_admin()
        if not valid:
            return self.respond(code=403, message=message)

        request_json_body_data = self.request.get_json()

        required_parameters = ["name", "model_number", "location"]
        valid, response = self.validate_parameters(params=required_parameters, request_params=request_json_body_data)
        if not valid:
            return response

        vending_machine_repository = get_vending_machine_repository(engine=engine)
        name = request_json_body_data["name"]
        model_number = request_json_body_data["model_number"]
        location = request_json_body_data["location"]

        vending_machine = VendingMachine(name=name, model_number=model_number, location=location)
        vending_machine_repository.insert(vending_machine)

        data = {
            "vending_machine": vending_machine.id
        }

        return self.respond(code=200, data=data)

    def update_vending_machine(self, vending_machine_id: str):
        valid, message = self.authorizer.is_admin()
        if not valid:
            return self.respond(code=403, message=message)

        json_body_data = self.request.get_json()

        vending_machine_repository = get_vending_machine_repository(engine=engine)
        vending_machine = vending_machine_repository.get_by_id(_id=vending_machine_id)
        if not vending_machine:
            return self.respond(code=404)

        vending_machine_attrs = ["name", "model_number", "location"]
        for key, value in json_body_data.items():
            if key in vending_machine_attrs:
                setattr(vending_machine, key, value)

        vending_machine_repository.insert(vending_machine)

        data = {
            "id": vending_machine.id,
            "name": vending_machine.name,
            "model_number": vending_machine.model_number,
            "location": vending_machine.location
        }

        return self.respond(code=200, data=data)

    def update_vending_machine_inventory(self, vending_machine_id: str):
        valid, message = self.authorizer.has_role(role="Seller")
        if not valid:
            return self.respond(code=403, message=message)

        json_body_data = self.request.get_json()

        required_parameters = ["product_id"]
        valid, response = self.validate_parameters(params=required_parameters, request_params=json_body_data)
        if not valid:
            return response

        vending_machine_repository = get_vending_machine_repository(engine=engine)
        vending_machine = vending_machine_repository.get_by_id(_id=vending_machine_id)
        if not vending_machine:
            return self.respond(code=404, message="Vending machine {0} not found".format(vending_machine_id))

        product_id = json_body_data["product_id"]
        cost = json_body_data.get("cost", None)
        qty = json_body_data.get("qty", None)

        inventory_line: Optional[VendingMachineInventory] = vending_machine.get_product_inventory_line(product_id)

        if not inventory_line:
            qty = qty or 0
            cost = cost or 0
            inventory_line = VendingMachineInventory(vending_machine_id=vending_machine.id, product_id=product_id,
                                                     seller_id=self.session_user.id, amount_available=qty, cost=cost)
            vending_machine.create_inventory_line(inventory_line)

        else:
            valid, message = self.authorizer.has_permission(has_update_inventory_permission,
                                                            inventory_line=inventory_line)
            if not valid:
                return self.respond(code=403, message=message)

            if qty is not None:
                inventory_line.amount_available += qty

            if cost is not None:
                inventory_line.cost = cost

        vending_machine_repository.insert(vending_machine)

        return self.respond(code=200, message="Updated successfully")

    def add_user_deposit(self):
        valid, user = self.authorizer.is_authorized()
        if not valid:
            return self.respond(code=403)

        request_json_body_data = self.request.get_json()

        required_parameters = ["deposit"]
        valid, response = self.validate_parameters(params=required_parameters, request_params=request_json_body_data)
        if not valid:
            return response

        user_repository = get_user_repository(engine)
        vending_machine_repository = get_vending_machine_repository(engine)
        deposit = request_json_body_data["deposit"]

        vending_machine_service = VendingMachineService(user_repository=user_repository,
                                                        vending_machine_repository=vending_machine_repository)

        res = vending_machine_service.add_user_deposit(user=user, deposit=deposit)
        if not res.success:
            return self.respond(code=417, message=res.message)

        res_user: User = res.data["user"]
        data = {
            "user_id": res_user.id,
            "deposit": res_user.deposit
        }

        return self.respond(code=200, data=data)


@app.route("/vending_machines", methods=["GET"])
def get_vending_machines():
    return VendingMachinesApi(request=request, methods=["GET"]).execute(method_name="get_vending_machines")


@app.route("/vending_machines/<string:vending_machine_id>", methods=["GET"])
def get_vending_machine_details(vending_machine_id: str):
    return VendingMachinesApi(request=request, methods=["GET"]).execute(method_name="get_vending_machine_details",
                                                                        vending_machine_id=vending_machine_id)


@app.route("/vending_machines", methods=["POST"])
def create_vending_machine():
    return VendingMachinesApi(request=request, methods=["POST"]).execute(method_name="create_vending_machine")


@app.route("/vending_machines/<string:vending_machine_id>", methods=["PUT"])
def update_vending_machine(vending_machine_id: str):
    return VendingMachinesApi(request=request, methods=["PUT"]).execute(method_name="update_vending_machine",
                                                                        vending_machine_id=vending_machine_id)


@app.route("/vending_machines/<string:vending_machine_id>/update_inventory", methods=["POST"])
def update_vending_machine_inventory(vending_machine_id: str):
    return VendingMachinesApi(request=request, methods=["POST"]).execute(method_name="update_vending_machine_inventory",
                                                                         vending_machine_id=vending_machine_id)


@app.route("/vending_machines/add_user_deposit", methods=["POST"])
def add_user_deposit():
    return VendingMachinesApi(request=request, methods=["POST"]).execute(method_name="add_user_deposit")
