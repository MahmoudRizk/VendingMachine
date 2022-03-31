from sqlalchemy import Column, TEXT


class DbModel:
    __table_args__ = {'extend_existing': True}
    id = Column(TEXT, primary_key=True)
