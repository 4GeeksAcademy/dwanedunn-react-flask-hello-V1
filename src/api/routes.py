"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200


@api.route('/profile/<int:userId>', methods=['GET'])
def handle_profile(userId):
    user = User.query.get(userId)

    if not user:
        raise APIException('User not found', status_code=404)

    response_body = {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name
    }

    return jsonify(response_body), 200


@api.route('/users', methods=['GET'])
def handle_users():
    users = User.query.all()
    response_body = []

    for user in users:
        response_body.append({
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name
        })

    return jsonify(response_body), 200
