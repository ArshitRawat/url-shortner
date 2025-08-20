from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine


def getDB():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

DatabaseURL = "sqlite:///./url.db"
engine = create_engine(DatabaseURL, connect_args={"check_same_thread" : False})
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)



Base = declarative_base()



