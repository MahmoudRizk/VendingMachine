from flask import Flask
from sqlalchemy import create_engine

db_url = "sqlite+pysqlite:///database.db"
authentication_secret_key = "X1Ul7Y3aR4ITazL-LzZSqVdhq8MIORbUZE-WmmTzjaA="

engine = create_engine(db_url, future=True, echo=True)
conn = engine.connect()

app = Flask(__name__)
