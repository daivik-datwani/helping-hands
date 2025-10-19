from backend.models.helpinghandsdatabase import Base, HelpRequest, Request
from backend.db import engine


Base.metadata.drop_all(bind=engine, tables=[HelpRequest.__table__, Request.__table__])


Base.metadata.create_all(bind=engine, tables=[HelpRequest.__table__, Request.__table__])
