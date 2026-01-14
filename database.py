from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url= "postgresql://postgres:starnasir9@localhost:5432/Items"
engine = create_engine(db_url)
session = sessionmaker(bind=engine, autoflush=False, autocommit=False)