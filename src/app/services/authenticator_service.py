from src.app.repositories.authenticator_repository import AuthenticatorRepository


class AuthenticatorService:
    def __init__(self, pool):
        self.repository = AuthenticatorRepository(pool)

    def validate_user(self, user_id, auth_key):
        try:
            user_id = int(user_id)
        except ValueError:
            return False
        user = self.repository.get_user_by_id(user_id)
        print(user, user_id)
        if user is None:
            return False
        print(user.api_key)

        return user.api_key == auth_key
