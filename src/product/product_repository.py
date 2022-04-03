from src.base.repository import Repository
from src.product.db_product import DbProduct
from src.product.mapper import ProductMapper
from src.product.product import Product


class ProductRepository(Repository):
    def __init__(self, engine, mapper: ProductMapper):
        db_model_type = DbProduct
        domain_model_type = Product
        super(ProductRepository, self).__init__(engine=engine, mapper=mapper, db_model_type=db_model_type,
                                                domain_model_type=domain_model_type)
