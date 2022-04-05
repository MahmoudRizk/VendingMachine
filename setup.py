from sqlalchemy_utils import create_database
from sqlalchemy import create_engine

from src import Base
from src.user.db_user import DbUser
from src.user.db_role import DbRole
from src.product.db_product import DbProduct
from src.vending_machine.db_vending_machine import DbVendingMachine
from src.vending_machine.db_vending_machine_inventory import DbVendingMachineInventory

db_url = "sqlite+pysqlite:///database.db"
create_database(db_url)

engine = create_engine(db_url, future=True, echo=True)
conn = engine.connect()

Base.metadata.create_all(engine)
