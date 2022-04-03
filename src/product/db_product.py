from sqlalchemy import Column, TEXT, Float

from src import Base
from src.base.db_model import DbModel


class DbProduct(DbModel, Base):
    __tablename__ = "Product"

    name = Column(TEXT, nullable=False)
    country_of_origin = Column(TEXT, nullable=False)
    calories = Column(Float, nullable=False)
    flavor = Column(TEXT, nullable=False)
