#run this once so that email column yeah then delete
from backend.models.helpinghandsdatabase import Base
from backend.db import engine

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
