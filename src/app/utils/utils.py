import os

import dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import mysql.connector.pooling

from src.app.models.base import Base
from sqlalchemy.pool import QueuePool

dotenv.load_dotenv()

# load env variables
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")


# def create_database_engine():
#     """Create database engine and create schema."""
#     engine = create_engine(f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}", echo=True)
#     Base.metadata.create_all(engine)
#     Session = sessionmaker(bind=engine)
#     return Session()


def create_database_pool_engine():
    """Create database engine with connection pool and create schema."""

    schema_engine = create_engine(f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
                                  echo=True)
    Base.metadata.create_all(schema_engine)
    schema_engine.dispose()

    # Create a connection pool with the size 3
    pool = QueuePool(creator=lambda: mysql.connector.connect(host=DB_HOST,
                                                             port=DB_PORT,
                                                             user=DB_USER,
                                                             password=DB_PASSWORD,
                                                             database=DB_NAME),
                     pool_size=3,
                     recycle=3600)

    # Create the engine using the connection pool
    engine = create_engine('mysql+mysqlconnector://', pool=pool, echo=True)

    return engine


class ApiResponse:
    @staticmethod
    def success(result):
        response = {"type": "success", "result": result}
        return response

    @staticmethod
    def fail(message):
        response = {"type": "fail", "message": message}
        return response
