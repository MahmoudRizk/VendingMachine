from src.base.repository import Repository
from src.vending_machine.db_vending_machine import DbVendingMachine
from src.vending_machine.db_vending_machine_inventory import DbVendingMachineInventory
from src.vending_machine.mapper import VendingMachineMapper
from src.vending_machine.vending_machine import VendingMachine, VendingMachineInventory


def get_vending_machine_repository(engine):
    mapped_entities = [
        (VendingMachine, DbVendingMachine),
        (VendingMachineInventory, DbVendingMachineInventory)
    ]

    mapper = VendingMachineMapper(mapped_entities=mapped_entities)

    return VendingMachineRepository(engine=engine, mapper=mapper)


class VendingMachineRepository(Repository):
    def __init__(self, engine, mapper: VendingMachineMapper):
        db_model_type = DbVendingMachine
        domain_model_type = VendingMachine
        super(VendingMachineRepository, self).__init__(engine=engine, mapper=mapper, db_model_type=db_model_type,
                                                       domain_model_type=domain_model_type)
