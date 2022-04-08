from typing import Optional

from flask import jsonify, request

from api import app, engine
from src.vending_machine.vending_machine import VendingMachine, VendingMachineInventory
from src.vending_machine.vending_machine_repository import get_vending_machine_repository


@app.route("/vending_machines", methods=["GET"])
def get_vending_machines():
    vending_machine_repository = get_vending_machine_repository(engine=engine)
    vending_machines = vending_machine_repository.get_all()
    return jsonify([
        {
            "id": it.id,
            "name": it.name,
            "model_number": it.model_number,
            "location": it.location
        }
        for it in vending_machines
    ])


@app.route("/vending_machines/<string:vending_machine_id>", methods=["GET"])
def get_vending_machine_details(vending_machine_id: str):
    vending_machine_repository = get_vending_machine_repository(engine=engine)
    vending_machine = vending_machine_repository.get_by_id(_id=vending_machine_id)
    if not vending_machine:
        return {}

    return {
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


@app.route("/vending_machines", methods=["POST"])
def create_vending_machine():
    json_body_data = request.get_json()

    # TODO: validate required parameters

    vending_machine_repository = get_vending_machine_repository(engine=engine)
    name = json_body_data["name"]
    model_number = json_body_data["model_number"]
    location = json_body_data["location"]

    vending_machine = VendingMachine(name=name, model_number=model_number, location=location)
    vending_machine_repository.insert(vending_machine)

    return {
        "vending_machine": vending_machine.id
    }


@app.route("/vending_machine/<string:vending_machine_id>", methods=["PUT"])
def update_vending_machine(vending_machine_id: str):
    json_body_data = request.get_json()

    # TODO: validate required parameters
    vending_machine_repository = get_vending_machine_repository(engine=engine)
    vending_machine = vending_machine_repository.get_by_id(_id=vending_machine_id)
    if not vending_machine:
        return {}

    vending_machine_attrs = ["name", "model_number", "location"]
    for key, value in json_body_data.items():
        if key in vending_machine_attrs:
            setattr(vending_machine, key, value)

    vending_machine_repository.insert(vending_machine)

    return {
        "id": vending_machine.id,
        "name": vending_machine.name,
        "model_number": vending_machine.model_number,
        "location": vending_machine.location
    }


@app.route("/vending_machines/<string:vending_machine_id>/update_inventory", methods=["POST"])
def update_vending_machine_inventory(vending_machine_id: str):
    json_body_data = request.get_json()

    # TODO: validate required parameters
    vending_machine_repository = get_vending_machine_repository(engine=engine)
    vending_machine = vending_machine_repository.get_by_id(_id=vending_machine_id)
    if not vending_machine:
        return {}

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

    return {
        "success": True
    }
