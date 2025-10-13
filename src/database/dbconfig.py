"""Database configuration module for SQLAlchemy and FastAPI."""

from typing import Annotated
from dotenv import load_dotenv
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

load_dotenv()

URL_DATABASE = "mysql+pymysql://root:38632696@localhost:3306/Tienda_de_ropa"


# if URL_DATABASE is None:
#     raise ValueError("DATABASE_URL environment variable is not set")
# else:

engine = create_engine(URL_DATABASE)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
