from sqlalchemy import Column, TEXT, ForeignKey
from sqlalchemy.orm import relationship

from src import Base
from src.base.db_model import DbModel


class DbRole(DbModel, Base):
    __tablename__ = "Role"

    name = Column(TEXT, nullable=False)
    user_id = Column(TEXT, ForeignKey('User.id'), nullable=False)
    user = relationship("DbUser", back_populates="roles")
