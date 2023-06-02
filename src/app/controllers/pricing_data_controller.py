from flask import Blueprint, jsonify, request
from src.app.services.pricing_data_service import PricingDataService
from src.app.utils.utils import create_database_engine
from src.app.utils.utils import ApiResponse
from flask_api import status
pricing_data_bp = Blueprint("pricing_data", __name__)
data_service = PricingDataService(create_database_engine())


class PricingDataController:
    @staticmethod
    def create_pricing_data():
        try:
            data = request.get_json()
            result = data_service.create_pricing_data(data)
            return jsonify(ApiResponse.success(result)), status.HTTP_201_CREATED

        except ValueError as e:
            return jsonify(ApiResponse.fail(e.args[0])), status.HTTP_400_BAD_REQUEST

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


pricing_data_bp.add_url_rule("create-record", methods=["POST"], view_func=PricingDataController.create_pricing_data)
pricing_data_bp.add_url_rule("insert-record", methods=["POST"],
                             view_func=PricingDataController.insert_pricing_data)
pricing_data_bp.add_url_rule("batch-update-records", methods=["POST"],
                             view_func=PricingDataController.batch_update_pricing_data)
pricing_data_bp.add_url_rule("update-record", methods=["POST"],
                             view_func=PricingDataController.update_pricing_data)
pricing_data_bp.add_url_rule("delete-record", methods=["POST"],
                             view_func=PricingDataController.delete_pricing_data)
pricing_data_bp.add_url_rule("get-record", methods=["POST"], view_func=PricingDataController.get_data)
