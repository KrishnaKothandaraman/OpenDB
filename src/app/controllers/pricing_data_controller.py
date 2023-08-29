from functools import wraps

import sqlalchemy.exc
from flask import Blueprint, jsonify, request, session
from src.app.services.pricing_data_service import PricingDataService
from src.app.services.authenticator_service import AuthenticatorService
from src.app.utils.utils import create_database_pool_engine
from src.app.utils.utils import ApiResponse
from flask_api import status

pricing_data_bp = Blueprint("pricing_data", __name__)
pool_engine = create_database_pool_engine()
data_service = PricingDataService(pool_engine)
auth_service = AuthenticatorService(pool_engine)


# Define a decorator to check for authentication headers
def authenticate_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_key = request.headers.get('auth-key')
        user_id = request.headers.get('user-id')
        if not auth_key or not user_id:
            return jsonify(ApiResponse.fail("Authentication failed. Headers missing")), status.HTTP_401_UNAUTHORIZED

        # Perform authentication here using the authenticate_user() function
        if not auth_service.validate_user(user_id=user_id, auth_key=auth_key):
            return jsonify(ApiResponse.fail("Authentication failed")), status.HTTP_401_UNAUTHORIZED

        # Store the authenticated user_id in the session for later use
        session['user_id'] = user_id

        return f(*args, **kwargs)

    return decorated_function


class PricingDataController:

    @staticmethod
    @pricing_data_bp.before_request
    @authenticate_required
    def before_request():
        user_id = session.get('user_id')
        if user_id is None:
            # Authentication failed, return an error response
            return jsonify(
                ApiResponse.fail("Authentication failed"),
                401)
        pass

    @staticmethod
    def create_pricing_data():
        try:
            data = request.get_json()
            result = data_service.create_pricing_data(data)
            return jsonify(ApiResponse.success(result)), status.HTTP_201_CREATED

        except ValueError as e:
            return jsonify(ApiResponse.fail(e.args[0])), status.HTTP_400_BAD_REQUEST
        except sqlalchemy.exc.IntegrityError as e:
            return jsonify(ApiResponse.fail(
                "Integrity check breaks for DB. Possible Duplicate Entry")), status.HTTP_409_CONFLICT

    @staticmethod
    def insert_pricing_data():
        try:
            data = request.get_json()
            result = data_service.insert_pricing_data(data)
            return jsonify(ApiResponse.success(result)), status.HTTP_201_CREATED
        except ValueError as e:
            return jsonify(ApiResponse.fail(e.args[0])), status.HTTP_400_BAD_REQUEST

    @staticmethod
    def batch_update_pricing_data():
        try:
            data = request.get_json()
            result = data_service.batch_update_pricing_data(data)
            return jsonify(ApiResponse.success(result)), status.HTTP_202_ACCEPTED
        except ValueError as e:
            return jsonify(ApiResponse.fail(e.args[0])), status.HTTP_400_BAD_REQUEST

    @staticmethod
    def update_pricing_data():
        try:
            json_data = request.get_json()
            result = data_service.update_pricing_data(json_data)
            return jsonify(ApiResponse.success(result)), status.HTTP_202_ACCEPTED
        except ValueError as e:
            print(f"Error: {e}")
            return jsonify(ApiResponse.fail(e.args[0])), status.HTTP_400_BAD_REQUEST

    @staticmethod
    def delete_pricing_data():
        try:
            json_data = request.get_json()
            result = data_service.delete_pricing_data(json_data)
            return jsonify(ApiResponse.success(result)), status.HTTP_202_ACCEPTED
        except ValueError as e:
            return jsonify(ApiResponse.fail(e.args[0])), status.HTTP_400_BAD_REQUEST

    @staticmethod
    def get_data():
        try:
            filters = request.get_json()
            result = data_service.get_data(filters)
            return jsonify(ApiResponse.success(result)), status.HTTP_200_OK
        except ValueError as e:
            return jsonify(ApiResponse.fail(e.args[0])), status.HTTP_400_BAD_REQUEST

    @staticmethod
    def handle_sales():
        try:
            sales = request.get_json()
            result = data_service.handle_sales(sales)
            return jsonify(ApiResponse.success(result)), status.HTTP_200_OK
        except ValueError as e:
            return jsonify(ApiResponse.fail(e.args[0])), status.HTTP_400_BAD_REQUEST


pricing_data_bp.add_url_rule("create-record", methods=["POST"], view_func=PricingDataController.create_pricing_data)
pricing_data_bp.add_url_rule("insert-record", methods=["POST"],
                             view_func=PricingDataController.insert_pricing_data)
pricing_data_bp.add_url_rule("batch-update-records", methods=["POST"],
                             view_func=PricingDataController.batch_update_pricing_data)
pricing_data_bp.add_url_rule("update-record", methods=["POST"],
                             view_func=PricingDataController.update_pricing_data)
pricing_data_bp.add_url_rule("delete-record", methods=["POST"],
                             view_func=PricingDataController.delete_pricing_data)
pricing_data_bp.add_url_rule("get-records", methods=["POST"], view_func=PricingDataController.get_data)
pricing_data_bp.add_url_rule("notify-sales", methods=["POST"], view_func=PricingDataController.handle_sales)
