from sqlalchemy_utils import create_database
from sqlalchemy import create_engine

from src import Base
from src.user.db_user import DbUser
from src.user.db_role import DbRole
from src.product.db_product import DbProduct
from src.user.user_repository import get_user_repository
from src.vending_machine.db_vending_machine import DbVendingMachine
from src.vending_machine.db_vending_machine_inventory import DbVendingMachineInventory

import os
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv("DB_URL")
admin_password = os.getenv("ADMIN_PASSWORD")

create_database(db_url)

engine = create_engine(db_url, future=True, echo=True)
conn = engine.connect()

Base.metadata.create_all(engine)

user_repository = get_user_repository(engine)
user_repository.create_or_update_admin(password=admin_password)
