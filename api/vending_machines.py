from typing import Optional, List

from flask import jsonify, request, Request

from api import app, engine
from api.base_api import BaseApi
from src.vending_machine.vending_machine import VendingMachine, VendingMachineInventory
from src.vending_machine.vending_machine_repository import get_vending_machine_repository


class VendingMachinesApi(BaseApi):
    def __init__(self, request: Request, methods: List[str]):
        super(VendingMachinesApi, self).__init__(request=request, methods=methods)

        self.methods_map = {
            "get_vending_machines": self.get_vending_machines,
            "get_vending_machine_details": self.get_vending_machine_details,
            "create_vending_machine": self.create_vending_machine,
            "update_vending_machine": self.update_vending_machine,
            "update_vending_machine_inventory": self.update_vending_machine_inventory,

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

        # TODO: check user permissions
        if not inventory_line:
            # TODO: create a new one.
            qty = qty or 0
            cost = cost or 0
            inventory_line = VendingMachineInventory(vending_machine_id=vending_machine.id, product_id=product_id,
                                                     seller_id="MOCKED SELLER", amount_available=qty, cost=cost)
            vending_machine.create_inventory_line(inventory_line)

        else:
            if qty is not None:
                inventory_line.amount_available += qty

            if cost is not None:
                inventory_line.cost = cost

        vending_machine_repository.insert(vending_machine)

        return self.respond(code=200, message="Updated successfully")


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
