from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from src.app.models.base import Base


class Authenticator(Base):
    __tablename__ = 'auth_keys'

    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    api_key = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    last_used = Column(DateTime, default=datetime.now())