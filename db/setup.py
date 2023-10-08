import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_URI = os.environ.get("DB_URI")

engine = create_engine(DB_URI, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    # Dependency
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
