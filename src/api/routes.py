"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS


from flask_jwt_extended import jwt_required


app = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(app)


@app.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200


@app.route('/profile/<int:userId>', methods=['GET'])
def handle_profile(userId):
    user = User.query.get(userId)

    if not user:
        raise appException('User not found', status_code=404)

    response_body = {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name
    }

    return jsonify(response_body), 200


@app.route('/users', methods=['GET'])
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


@app.route('/users', methods=['POST'])
def handle_create_user():
    body = request.get_json()

    if not body or not all(key in body for key in ('email', 'first_name', 'last_name')):
        raise APIException('Invalid input', status_code=400)

    new_user = User(
        email=body['email'],
        first_name=body['first_name'],
        last_name=body['last_name']
    )

    db.session.add(new_user)
    db.session.commit()

    response_body = {
        "id": new_user.id,
        "email": new_user.email,
        "first_name": new_user.first_name,
        "last_name": new_user.last_name
    }

    return jsonify(response_body), 201


@app.route('/users/<int:userId>', methods=['PUT'])
def handle_update_user(userId):
    body = request.get_json()
    user = User.query.get(userId)

    if not user:
        raise APIException('User not found', status_code=404)

    if not body or not all(key in body for key in ('email', 'first_name', 'last_name')):
        raise APIException('Invalid input', status_code=400)

    user.email = body['email']
    user.first_name = body['first_name']
    user.last_name = body['last_name']

    db.session.commit()

    response_body = {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name
    }

    return jsonify(response_body), 200


@app.route('/users/<int:userId>', methods=['DELETE'])
def handle_delete_user(userId):
    user = User.query.get(userId)

    if not user:
        raise APIException('User not found', status_code=404)

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted successfully"}), 200


# Generate the token for the user based on the email and password
@app.route('/token', methods=['POST'])
def generate_token():

    email = request.json.get("email", None)
    password = request.json.get("password", None)
    if email != "test" or password != "test":
        return jsonify({"msg": "Bad email or password"}), 401

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)
    return jsonify(response_body), 200
