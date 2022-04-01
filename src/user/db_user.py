from sqlalchemy import Column, TEXT
from sqlalchemy.orm import relationship

from src.base.db_model import DbModel
from src import Base

from src.user.db_role import DbRole


class DbUser(DbModel, Base):
    __tablename__ = "User"

    name = Column(TEXT, nullable=False, unique=True)
    password = Column(TEXT, nullable=True)
    roles = relationship("DbRole", back_populates="user")
