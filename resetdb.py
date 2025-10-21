#run this once so that email column yeah then delete
from backend.models.helpinghandsdatabase import Base, Request, HelpRequest
from backend.db import engine, SessionLocal


	
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


'''
from datetime import datetime
from sqlalchemy import extract

db = SessionLocal()

# Find all requests with year > 9999 (or any unreasonable value)
bad_requests = db.query(Request).filter(extract('year', Request.time) > 9999).all()

for req in bad_requests:
    print(f"Fixing request {req.id} with time {req.time}")
    # Set to a safe default date
    req.time = datetime.now()

db.commit()
db.close()
'''