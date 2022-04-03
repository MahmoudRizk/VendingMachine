from typing import Dict, Type, Optional

from src.base.mapper import Mapper
from src.vending_machine.db_vending_machine import DbVendingMachine
from src.vending_machine.vending_machine import VendingMachine


class VendingMachineMapper(Mapper):
    def data_to_domain(self, data: Dict, domain_class: Type[VendingMachine],
                       manual_mapper: Optional[Dict] = None) -> VendingMachine:
        return super().data_to_domain(data=data, domain_class=domain_class, manual_mapper=manual_mapper)

    def domain_to_data(self, domain_data: VendingMachine, model_class: Type[DbVendingMachine]) -> DbVendingMachine:
        return super().domain_to_data(domain_data=domain_data, model_class=model_class)
