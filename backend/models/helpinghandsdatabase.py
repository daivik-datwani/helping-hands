from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from backend.db import Base
from datetime import datetime

class Senior(Base):
    __tablename__ = "seniors"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    email = Column(String, unique=True, nullable=True)
    password_hash = Column(String, nullable=False)
    phone = Column(String, nullable=True)

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


class HelpRequest(Base):
    __tablename__ = "help_requests"

    id = Column(Integer, primary_key=True, index=True)
    senior_id = Column(Integer, ForeignKey("seniors.id"))
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    category = Column(String, nullable=False)
    location = Column(String, nullable=False)
    status = Column(String, default="Pending")
    created_at = Column(DateTime, default=datetime.utcnow)

    senior = relationship("Senior")

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
