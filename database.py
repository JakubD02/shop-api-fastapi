from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

URL_DATABASE = 'sqlite:///./shop.db'

engine = create_engine(URL_DATABASE, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()