from flask import Flask, request, jsonify
from flask_cors import CORS
import os

from src.app.models.pricing_data_model import Base
import dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

dotenv.load_dotenv()

# load env variables
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")

app = Flask(__name__)
CORS(app)


def create_database_engine():
    """Create database engine and create schema."""
    engine = create_engine(f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}", echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


def process_create_request(json):
    return "create success"


def process_read_request(json):
    return "read success"


def process_update_request(json):
    return "update success"


def process_delete_request(json):
    return "delete success"


@app.route("/update-db", methods=["POST", "GET", "PUT", "DELETE"])
def process_request():
    http_method = request.method

    # Check the request type and call the corresponding process request function
    if http_method == "POST":
        response = process_create_request(request.json)
    elif http_method == "GET":
        response = process_read_request(request.json)
    elif http_method == "PUT":
        response = process_update_request(request.json)
    elif http_method == "DELETE":
        response = process_delete_request(request.json)
    else:
        return jsonify({"message": "Unsupported request type"}), 400

    return jsonify(response)
