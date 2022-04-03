from typing import Dict, Type, Optional

from src.base.mapper import Mapper
from src.product.db_product import DbProduct
from src.product.product import Product


class ProductMapper(Mapper):
    def data_to_domain(self, data: Dict, domain_class: Type[Product], manual_mapper: Optional[Dict] = None) -> Product:
        return super().data_to_domain(data=data, domain_class=domain_class, manual_mapper=manual_mapper)

    def domain_to_data(self, domain_data: Product, model_class: Type[DbProduct]) -> DbProduct:
        return super().domain_to_data(domain_data=domain_data, model_class=model_class)
