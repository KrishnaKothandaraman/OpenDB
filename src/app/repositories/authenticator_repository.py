from src.app.models.authenticator_model import Authenticator
from sqlalchemy.orm import Session
from sqlalchemy import update, case, literal


class AuthenticatorRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_user_by_id(self, user_id):
        return self.session.query(Authenticator).filter_by(user_id=user_id).first()
