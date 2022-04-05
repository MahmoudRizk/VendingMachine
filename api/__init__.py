from flask import Flask
from sqlalchemy import create_engine

db_url = "sqlite+pysqlite:///database.db"
engine = create_engine(db_url, future=True, echo=True)
conn = engine.connect()

app = Flask(__name__)
