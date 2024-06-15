from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings

# Construct the database URL from the settings configuration
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.database_username}:"
    f"{settings.database_password}@{settings.database_hostname}:"
    f"{settings.database_port}/{settings.database_name}"
)


"""
       FASTAPI
          |
SQLALCHEMY (Python ORM)  ----  (ALEMBIC FOR MIGRATIONS)
          | 
PSYCOPG (PostgreSQL Adapter)
          |
 PostgreSQL DataBase
""" 

# Create an SQLAlchemy engine that will interact with the PostgreSQL database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Configure a session factory that will be used to create new session objects
# autocommit=False: Changes will not be committed automatically
# autoflush=False: Changes will not be flushed automatically to the database
# bind=engine: The session will use the created engine to connect to the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 

# Create a base class for the declarative model classes
Base = declarative_base() # allows interaction between SQLAlchemy and the database using models, with each model associated with one database table. 

def get_db():
    """
    Dependency that provides a database session.

    Yields:
    - db (Session): A new database session.
    
    Ensures that the database session is closed after the request is completed.
    """
    db = SessionLocal()
    try:
        # Yield the database session to the dependent function
        yield db
    finally:
        # Close the database session after the dependent function returns
        db.close()
