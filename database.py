#import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# DB_PATH = os.path.join(BASE_DIR, "anketi.db")

engine = create_engine(f"sqlite:///anketi.db")


SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

Base = declarative_base()
