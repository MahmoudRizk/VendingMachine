from sqlalchemy import Column, TEXT, ForeignKey, Float
from sqlalchemy.orm import relationship

from src import Base
from src.base.db_model import DbModel


class DbVendingMachineInventory(DbModel, Base):
    __tablename__ = "VendingMachineInventory"

    vending_machine_id = Column(TEXT, ForeignKey("VendingMachine.id"), nullable=False)
    product_id = Column(TEXT, ForeignKey("Product.id"), nullable=False)
    seller_id = Column(TEXT, ForeignKey("User.id"), nullable=False)
    amount_available = Column(Float, nullable=False, default=0.0)
    cost = Column(Float, nullable=False, default=0.0)

    vending_machine = relationship("DbVendingMachine", back_populates="inventory")
