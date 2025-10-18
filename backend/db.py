from sqlalchemy import *
from sqlalchemy.orm import *
import os

Base = declarative_base()

# Use DATABASE_URL if provided (12 factor). Otherwise try the project's Postgres URL.
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
	engine = create_engine(DATABASE_URL)
else:
	try:
		engine = create_engine("postgresql+psycopg2://postgres:Tian12885%40@localhost/postgres")
	except Exception:
		# Fall back to a lightweight SQLite DB for local/dev environments so the app can run
		engine = create_engine("sqlite:///./dev.db", connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(bind=engine)

