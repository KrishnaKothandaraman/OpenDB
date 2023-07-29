from flask import Flask, request, jsonify
from flask_cors import CORS

from src.app.controllers.pricing_data_controller import pricing_data_bp

app = Flask(__name__)
CORS(app)

# add an url prefix to the blueprint of /pricing-data
app.register_blueprint(pricing_data_bp, url_prefix="/pricing-data")


def create_api_app():
    return app


if __name__ == "__main__":
    app.run(port=5001)
