from dataclasses import dataclass, field
from typing import List, Optional

from src.base.domain import Domain


class VendingMachineException(Exception):
    pass


class VendingMachineMissingException(Exception):
    pass


@dataclass
class VendingMachineInventory(Domain):
    vending_machine_id: str = field(default=None)
    product_id: str = field(default=None)
    seller_id: str = field(default=None)
    amount_available: float = field(default=0.0)
    cost: float = field(default=0.0)

    def __post_init__(self):
        super(VendingMachineInventory, self).__post_init__()

        required_attrs = ["product_id", "seller_id"]
        for attr in required_attrs:
            _v = getattr(self, attr)
            if not _v:
                raise VendingMachineException("{0} can't be null".format(_v))


@dataclass
class VendingMachine(Domain):
    name: str = field(default=None)
    model_number: str = field(default=None)
    location: str = field(default=None)
    inventory: List[VendingMachineInventory] = Domain.list_of_field(key="inventory",
                                                                    list_of_type=VendingMachineInventory)

    def __post_init__(self):
        super(VendingMachine, self).__post_init__()

        self.inventory = self.inventory or []

    def reset_inventory_item_qty(self, product_id: str, qty: int):
        inventory_item = self._get_inventory_line(_id=product_id)
        inventory_item.amount_available = qty

    def sell_item(self, product_id: str, qty: int):
        inventory_item = self._get_inventory_line(_id=product_id)

        current_available_amount = inventory_item.amount_available
        inventory_item.amount_available -= qty
        if inventory_item.amount_available <= 0:
            raise VendingMachineException(
                "product_id {0} has no available amount. available: {1}, requested: {2}".format(product_id,
                                                                                                current_available_amount,
                                                                                                qty))

    def create_inventory_line(self, line: VendingMachineInventory) -> None:
        self.inventory.append(line)

    def get_product_inventory_line(self, product_id) -> Optional[VendingMachineInventory]:
        try:
            return self._get_inventory_line(_id=product_id)
        except VendingMachineMissingException as e:
            return None

    def update_inventory_item_cost(self, product_id: str, cost: float):
        inventory_item = self._get_inventory_line(_id=product_id)
        inventory_item.cost = cost

    def update_inventory_item_qty(self, product_id: str, qty: int):
        inventory_item = self._get_inventory_line(_id=product_id)
        inventory_item.amount_available += qty

    def _get_inventory_line(self, _id: str) -> Optional[VendingMachineInventory]:
        for it in self.inventory:
            if it.product_id == _id:
                return it
        raise VendingMachineMissingException("product_id {0} not found".format(_id))
