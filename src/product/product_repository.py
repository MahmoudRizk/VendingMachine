from src.base.repository import Repository
from src.product.db_product import DbProduct
from src.product.mapper import ProductMapper
from src.product.product import Product


def get_product_repository(engine):
    mapped_entities = [
        (Product, DbProduct)
    ]

    mapper = ProductMapper(mapped_entities=mapped_entities)

    return ProductRepository(engine=engine, mapper=mapper)


class ProductRepository(Repository):
    def __init__(self, engine, mapper: ProductMapper):
        db_model_type = DbProduct
        domain_model_type = Product
        super(ProductRepository, self).__init__(engine=engine, mapper=mapper, db_model_type=db_model_type,
                                                domain_model_type=domain_model_type)
