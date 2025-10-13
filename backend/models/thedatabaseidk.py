from sqlalchemy import *
from backend.db import Base

class User(Base):
    __tablename__ = "seniors"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    phoneemail = Column(String)

