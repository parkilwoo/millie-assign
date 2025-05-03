from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from infrastructure.orm.sql_alchemy.base import Base
from config import settings

engine = create_engine(url=settings.database_url, pool_pre_ping=True)
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autoflush=False, bind=engine)

def get_db_session():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()