from flask import Flask
from sqlalchemy import create_engine

import os
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv("DB_URL")
authentication_secret_key = os.getenv("AUTHENTICATION_SECRET_KEY")

engine = create_engine(db_url, future=True, echo=True)
conn = engine.connect()

app = Flask(__name__)
