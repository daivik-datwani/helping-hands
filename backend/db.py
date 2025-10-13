from sqlalchemy import *
from sqlalchemy.orm import *

Base = declarative_base()
engine = create_engine("postgresql+psycopg2://postgres:Tian12885%40@localhost/postgres")

SessionLocal = sessionmaker(bind=engine)
