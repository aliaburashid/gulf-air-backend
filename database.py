from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from config.environment import db_URI

# Connect FastAPI with SQLAlchemy
# Enable foreign key constraints for SQLite
engine = create_engine(
    db_URI,
    connect_args={"check_same_thread": False} if "sqlite" in db_URI else {}
)

# Enable foreign key constraints for SQLite
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if "sqlite" in db_URI:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# This function is a dependency that provides database access to API endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
