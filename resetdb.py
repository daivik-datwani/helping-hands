#run this once so that email column yeah then delete
from backend.models.helpinghandsdatabase import Base, Request, Feedback
from backend.db import engine

Base.metadata.drop_all(bind=engine, tables=[Feedback.__table__])
Base.metadata.drop_all(bind=engine, tables=[Request.__table__])
Base.metadata.create_all(bind=engine, tables=[Request.__table__])
Base.metadata.create_all(bind=engine, tables=[Feedback.__table__])

