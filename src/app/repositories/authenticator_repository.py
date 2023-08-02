from src.app.models.authenticator_model import Authenticator
from sqlalchemy.orm import Session
from sqlalchemy import Engine, select
from sqlalchemy import update, case, literal


class AuthenticatorRepository:
    def __init__(self, engine: Engine):
        self.engine = engine

    def get_user_by_id(self, user_id):
        with self.engine.connect() as conn:
            session = Session(conn)
            user = session.query(Authenticator).filter(Authenticator.user_id == user_id).first()
            session.close()
            return user