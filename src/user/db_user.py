from sqlalchemy import Column, TEXT, Float
from sqlalchemy.orm import relationship

from src.base.db_model import DbModel
from src import Base


class DbUser(DbModel, Base):
    __tablename__ = "User"

    name = Column(TEXT, nullable=False, unique=True)
    password = Column(TEXT, nullable=True)
    deposit = Column(Float, default=0.0)
    roles = relationship("DbRole", back_populates="user", cascade="all, delete-orphan")
