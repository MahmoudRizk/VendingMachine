from unittest import TestCase

from sqlalchemy import create_engine

from src import Base
from src.product.db_product import DbProduct
from src.product.mapper import ProductMapper
from src.product.product import Product
from src.product.product_repository import ProductRepository


class TestProductRepository(TestCase):
    def setUp(self):
        db_url = "sqlite+pysqlite:///:memory:"
        self.engine = create_engine(db_url, future=True, echo=True)
        Base.metadata.create_all(self.engine)

        mapped_entities = [
            (Product, DbProduct)
        ]

        mapper = ProductMapper(mapped_entities=mapped_entities)

        self.product_repository = ProductRepository(engine=self.engine, mapper=mapper)

    def test_create_new_product(self):
        name = "Test Product 1"
        country_of_origin = "Egypt"
        calories = 50
        flavor = "Chocolate"

        domain_product: Product = Product(name=name, country_of_origin=country_of_origin, calories=calories,
                                          flavor=flavor)
        res: Product = self.product_repository.insert(domain_product)

        self.assertTrue(res)
        self.assertTrue(res.id)
        self.assertEqual(res.name, name)
        self.assertEqual(res.country_of_origin, country_of_origin)
        self.assertEqual(res.calories, calories)
        self.assertEqual(res.flavor, flavor)
