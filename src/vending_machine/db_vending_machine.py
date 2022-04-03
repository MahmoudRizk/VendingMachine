from sqlalchemy import Column, TEXT
from sqlalchemy.orm import relationship

from src import Base
from src.base.db_model import DbModel


class DbVendingMachine(DbModel, Base):
    __tablename__ = "VendingMachine"

    name = Column(TEXT, nullable=False)
    model_number = Column(TEXT, nullable=False)
    location = Column(TEXT, nullable=False)
    inventory = relationship("DbVendingMachineInventory", back_populates="vending_machine",
                             cascade="all, delete-orphan")
