from sqlalchemy import Column, TEXT

from src.base.db_model import DbModel
from src import Base


class DbUser(DbModel, Base):
    __tablename__ = "User"

    name = Column(TEXT, nullable=False, unique=True)
    password = Column(TEXT, nullable=True)
