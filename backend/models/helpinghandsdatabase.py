from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
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
    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)

    help_requests = relationship("HelpRequest", back_populates="senior")
    feedback = relationship("Feedback", back_populates="senior")
    requests = relationship("Request", back_populates="senior")


class Caretaker(Base):
    __tablename__ = "caretakers"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    phone = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=True)
    password_hash = Column(String, nullable=False)
    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)

    requests = relationship("Request", back_populates="caretaker")
    feedback = relationship("Feedback", back_populates="caretaker")


class HelpRequest(Base):
    __tablename__ = "help_requests"

    id = Column(Integer, primary_key=True, index=True)
    senior_id = Column(Integer, ForeignKey("seniors.id"))
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    category = Column(String, nullable=False)
    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)
    status = Column(String, default="Pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    time = Column(DateTime)
    

    senior = relationship("Senior", back_populates="help_requests")


class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    senior_id = Column(Integer, ForeignKey("seniors.id"))
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    category = Column(String, nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    status = Column(String, default="Pending")
    caretaker_id = Column(Integer, ForeignKey("caretakers.id"))
    time = Column(DateTime)

    senior = relationship("Senior", back_populates="requests")
    caretaker = relationship("Caretaker", back_populates="requests")
    feedback = relationship("Feedback", back_populates="requests")

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    senior_id = Column(Integer, ForeignKey("seniors.id"))
    request_id = Column(Integer, ForeignKey("requests.id"))
    comment = Column(String, nullable=False)
    rating = Column(Integer)
    caretaker_id = Column(Integer, ForeignKey("caretakers.id"))

    senior = relationship("Senior", back_populates="feedback")
    caretaker = relationship("Caretaker", back_populates="feedback")
    requests = relationship("Request", back_populates="feedback")
