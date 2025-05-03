from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL= "sqlite:///./usuarios.db"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(autoflush=False, autocommit=False, bind=engine)
session = Session()
Base = declarative_base()
