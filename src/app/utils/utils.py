import os

import dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.app.models.base import Base

dotenv.load_dotenv()

# load env variables
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")


def create_database_engine():
    """Create database engine and create schema."""
    engine = create_engine(f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}", echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


class ApiResponse:
    @staticmethod
    def success(result):
        response = {"type": "success", "result": result}
        return response

    @staticmethod
    def fail(message):
        response = {"type": "fail", "message": message}
        return response
