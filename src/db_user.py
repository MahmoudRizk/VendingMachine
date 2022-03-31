from sqlalchemy import Column, String, TEXT

from src import Base


class DbUser(Base):
    __tablename__ = "User"
    __table_args__ = {'extend_existing': True}

    id = Column(TEXT, primary_key=True)
    name = Column(TEXT, nullable=False, unique=True)
    password = Column(TEXT, nullable=True)
