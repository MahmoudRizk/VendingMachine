from unittest import TestCase

from sqlalchemy import create_engine

from src import Base
from src.product.db_product import DbProduct
from src.product.mapper import ProductMapper
from src.product.product import Product
from src.product.product_repository import ProductRepository
from src.user.db_role import DbRole
from src.user.db_user import DbUser
from src.user.mapper import UserMapper
from src.user.user import User, Role
from src.user.user_repository import UserRepository
from src.vending_machine.db_vending_machine import DbVendingMachine
from src.vending_machine.db_vending_machine_inventory import DbVendingMachineInventory
from src.vending_machine.mapper import VendingMachineMapper
from src.vending_machine.vending_machine import VendingMachine, VendingMachineInventory
from src.vending_machine.vending_machine_repository import VendingMachineRepository


class TestVendingMachineRepository(TestCase):
    def setUp(self):
        db_url = "sqlite+pysqlite:///:memory:"
        self.engine = create_engine(db_url, future=True, echo=True)
        Base.metadata.create_all(self.engine)

        vending_mapped_entities = [
            (VendingMachine, DbVendingMachine),
            (VendingMachineInventory, DbVendingMachineInventory)
        ]
        vending_machine_mapper = VendingMachineMapper(mapped_entities=vending_mapped_entities)
        self.vending_machine_repository = VendingMachineRepository(engine=self.engine, mapper=vending_machine_mapper)

        user_mapped_entities = [
            (User, DbUser),
            (Role, DbRole)
        ]
        user_mapper = UserMapper(mapped_entities=user_mapped_entities)
        self.user_repository = UserRepository(engine=self.engine, mapper=user_mapper)

        product_mapped_entities = [
            (Product, DbProduct)
        ]
        product_mapper = ProductMapper(mapped_entities=product_mapped_entities)
        self.product_repository = ProductRepository(engine=self.engine, mapper=product_mapper)

    def test_create_new_vending_machine_without_inventory(self):
        vending_machine_name = "Vending Machine 1"
        model_number = "FAKE MODEL 1"
        location = "Cairo"

        domain_vending_machine: VendingMachine = VendingMachine(name=vending_machine_name, model_number=model_number,
                                                                location=location)
        res: VendingMachine = self.vending_machine_repository.insert(domain_vending_machine)

        self.assertTrue(res)
        self.assertTrue(res.id)
        self.assertEqual(res.name, vending_machine_name)
        self.assertEqual(res.model_number, model_number)
        self.assertEqual(res.location, location)

    def test_create_new_vending_machine_with_inventory(self):
        vending_machine_name = "Vending Machine 1"
        model_number = "FAKE MODEL 1"
        location = "Cairo"

        product_1 = Product(name="Product 1", country_of_origin="Egypt", calories=90, flavor="Flavor 1")
        product_1 = self.product_repository.insert(product_1)

        user_1 = User(name="Test User 1", deposit=40, roles=[Role(name="Buyer"), Role(name="Seller")])
        user_1 = self.user_repository.insert(user_1)

        inventory = [
            VendingMachineInventory(product_id=product_1.id, seller_id=user_1.id, amount_available=10, cost=2)
        ]

        domain_vending_machine: VendingMachine = VendingMachine(name=vending_machine_name, model_number=model_number,
                                                                location=location, inventory=inventory)
        res: VendingMachine = self.vending_machine_repository.insert(domain_vending_machine)

        self.assertTrue(res)
        self.assertTrue(res.id)
        self.assertEqual(res.name, vending_machine_name)
        self.assertEqual(res.model_number, model_number)
        self.assertEqual(res.location, location)

        res_inventory = res.inventory[0]
        self.assertTrue(res_inventory.id)
        self.assertEqual(res_inventory.vending_machine_id, res.id)
        self.assertEqual(res_inventory.cost, 2)
        self.assertEqual(res_inventory.amount_available, 10)

    def test_update_vending_machine_current_inventory(self):
        vending_machine_name = "Vending Machine 1"
        model_number = "FAKE MODEL 1"
        location = "Cairo"

        product_1 = Product(name="Product 1", country_of_origin="Egypt", calories=90, flavor="Flavor 1")
        product_1 = self.product_repository.insert(product_1)

        product_2 = Product(name="Product 2", country_of_origin="USA", calories=400, flavor="Flavor 2")
        product_2 = self.product_repository.insert(product_2)

        product_3 = Product(name="Product 3", country_of_origin="KSA", calories=500, flavor="Flavor 3")
        product_3 = self.product_repository.insert(product_3)

        user_1 = User(name="Test User 1", deposit=40, roles=[Role(name="Buyer"), Role(name="Seller")])
        user_1 = self.user_repository.insert(user_1)

        inventory = [
            VendingMachineInventory(product_id=product_1.id, seller_id=user_1.id, amount_available=10, cost=2),
            VendingMachineInventory(product_id=product_2.id, seller_id=user_1.id, amount_available=20, cost=3),
            VendingMachineInventory(product_id=product_3.id, seller_id=user_1.id, amount_available=30, cost=4)
        ]

        domain_vending_machine: VendingMachine = VendingMachine(name=vending_machine_name, model_number=model_number,
                                                                location=location, inventory=inventory)
        domain_vending_machine: VendingMachine = self.vending_machine_repository.insert(domain_vending_machine)

        domain_vending_machine.reset_inventory_item_qty(product_id=product_1.id, qty=12)
        domain_vending_machine.sell_item(product_id=product_2.id, qty=3)
        domain_vending_machine.update_inventory_item_qty(product_id=product_3.id, qty=10)

        res: VendingMachine = self.vending_machine_repository.insert(domain_vending_machine)

        res_product_1 = res.inventory[0]
        res_product_2 = res.inventory[1]
        res_product_3 = res.inventory[2]
        
        self.assertEqual(res_product_1.amount_available, 12)
        self.assertEqual(res_product_2.amount_available, 17)
        self.assertEqual(res_product_3.amount_available, 40)
