from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from backend.db import Base

class Senior(Base):
    __tablename__ = "seniors"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    phone = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=True)
    password_hash = Column(String, nullable=False)

    requests = relationship("Request", back_populates="senior")


class Caretaker(Base):
    __tablename__ = "caretakers"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    phone = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=True)
    password_hash = Column(String, nullable=False)

    requests = relationship("Request", back_populates="caretaker")


class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True)
    time = Column(String)
    senior_id = Column(Integer, ForeignKey("seniors.id"))
    caretaker_id = Column(Integer, ForeignKey("caretakers.id"))
    location = Column(String)
    amount_paid = Column(Integer)

    senior = relationship("Senior", back_populates="requests")
    caretaker = relationship("Caretaker", back_populates="requests")
