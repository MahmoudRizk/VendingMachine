from typing import Tuple

from service.base_service_response import ServiceResponse as Response
from src.user.user import User
from src.user.user_repository import UserRepository
from src.vending_machine.vending_machine import VendingMachine
from src.vending_machine.vending_machine_repository import VendingMachineRepository


def validate_deposit(deposit: float) -> Tuple[bool, str]:
    if deposit % 5 != 0 or deposit not in [5, 10, 20, 50, 100]:
        return False, "Invalid Deposit {0}, deposit must be in these values [5 ,10, 20, 50, 100]".format(
            str(deposit))

    return True, ""


class VendingMachineService:
    def __init__(self, user_repository: UserRepository, vending_machine_repository: VendingMachineRepository):
        self.user_repository = user_repository
        self.vending_machine_repository = vending_machine_repository

    def add_user_deposit(self, user: User, deposit: float) -> Response:
        valid, message = validate_deposit(deposit=deposit)
        if not valid:
            return Response(success=False, message=message)

        user.deposit += deposit
        self.user_repository.insert(user)

        data = {
            "user": user
        }

        return Response(success=True, data=data)

    def buy_product(self, user: User, vending_machine: VendingMachine, product_id: str, qty: int) -> Response:

        inventory_line = vending_machine.get_product_inventory_line(product_id=product_id)
        if not inventory_line:
            return Response(success=False, message="Product id {0} not found".format(product_id))

        if type(qty) != int:
            return Response(success=False, message="Qty {0} must be an integer value".format(str(qty)))

        total_charges = qty * inventory_line.cost

        if total_charges > user.deposit:
            return Response(success=False,
                            message="No enough deposits '{0}', total charges '{1}'".format(
                                user.deposit,
                                total_charges))

        if qty > inventory_line.amount_available:
            return Response(success=False, message="Qty {0} is more than the available amount {1}".format(str(qty),
                                                                                                          str(inventory_line.cost)))

        vending_machine.sell_item(product_id=product_id, qty=qty)

        user.deposit -= total_charges

        self.user_repository.insert(user)
        self.vending_machine_repository.insert(vending_machine)

        # TODO: factorize the change amount into the available currency base amounts.
        data = {
            "change": user.deposit
        }
        return Response(success=True, data=data)
