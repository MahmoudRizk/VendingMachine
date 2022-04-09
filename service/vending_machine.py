from typing import Tuple

from service.base_service_response import ServiceResponse as Response
from src.user.user import User
from src.user.user_repository import UserRepository
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
