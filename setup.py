from sqlalchemy_utils import create_database
from sqlalchemy import create_engine

from src import Base

db_url = "sqlite+pysqlite:///database.db"
create_database(db_url)

engine = create_engine(db_url, future=True, echo=True)
conn = engine.connect()

Base.metadata.create_all(engine)
