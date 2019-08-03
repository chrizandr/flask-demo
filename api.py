"""Main application."""
import datetime
import jwt
import pdb

from flask import Flask
from flask import (
    request, render_template,
    redirect, url_for, flash, jsonify
)
from flask_pymongo import PyMongo
from passlib.hash import bcrypt


app = Flask(__name__)
print("Configuring app...")
app.secret_key = "DFDKFNWEFOWEFIWV"
app.config["MONGO_URI"] = "mongodb://localhost:27017/demodb"
mongo = PyMongo(app)


@app.route("/", methods=["GET"])
def index():
    """Index page."""
    auth_header = request.headers.get('Authorization', None)
    if auth_header is None:
        message = {"message": "No Authorization token provided"}
        response = jsonify(message)
        response.status_code = 401
        return response
    else:
        auth_token = auth_header.split(" ")[1]

    # Assume black box
    status_code, response = decode_auth_token(auth_token)

    if status_code != 200:
        message = {"message": response}
        response = jsonify(message)
        response.status_code = status_code
        return response
    else:
        message = {"message": "This is index page."}
        response = jsonify(message)
        response.status_code = status_code
        return response


@app.route('/register', methods=["GET", "POST"])
def register():
    """Register."""
    if request.method == "GET":
        message = {"message": "Please post with the following fields: username, password, emailid"}
        response = jsonify(message)
        response.status_code = 200
        return response

    if request.method == "POST":
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        email = request.form.get('emailid', None)

        if username is None or password is None or email is None:
            message = {"message": "Please post with the following fields: username, password, emailid"}
            response = jsonify(message)
            response.status_code = 400
            return response

        mongo.db.users.insert({"username": username, "password": bcrypt.encrypt(password),
                              "email": email})

        message = {"message": "Successfully registered, please login at /login"}
        response = jsonify(message)
        response.status_code = 200
        return response


@app.route('/forgot', methods=["GET", "POST"])
def forgot():
    """Register."""
    if request.method == "GET":
        message = {"message": "Please post with the following fields: emailid"}
        response = jsonify(message)
        response.status_code = 200
        return response

    if request.method == "POST":
        email = request.form.get('emailid', None)
        if email is None:
            message = {"message": "Please post with the following fields: emailid"}
            response = jsonify(message)
            response.status_code = 400
            return response
        else:
            message = {"message": "No operation done"}
            response = jsonify(message)
            response.status_code = 200
            return response


@app.route('/login', methods=["GET", "POST"])
def login():
    """Login."""
    if request.method == "GET":
        message = {"message": "Please post with the following fields: username, password, remember[true/false]"}
        response = jsonify(message)
        response.status_code = 200
        return response

    if request.method == "POST":
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        remember = request.form.get("remember", None)

        status_code = 200
        if username is None or password is None or remember is None:
            message = {"message": "Please post with the following fields: username, password, remember[true/false]"}
            status_code = 400
        else:
            user = mongo.db.users.find_one({"username": username})
            if user is None:
                message = {"message": "username does not exist"}
                status_code = 400
            else:
                if not bcrypt.verify(password, user["password"]):
                    message = {"message": "password is incorrect"}
                    status_code = 400
            if remember not in ["true", "false"]:
                message = {"message": "remember field must have true/false"}
                status_code = 400

            if status_code == 200:
                auth_token = encode_auth_token(str(user["_id"]), remember == "true")
                message = {"auth_token": auth_token.decode("utf-8")}

            response = jsonify(message)
            response.status_code = status_code
            return response


@app.route('/logout', methods=["GET"])
def logout():
    """Logout."""
    auth_header = request.headers.get('Authorization', None)
    if auth_header is None:
        message = {"message": "No Authorization token provided"}
        response = jsonify(message)
        response.status_code = 401
        return response
    else:
        auth_token = auth_header.split(" ")[1]

    # Assume black box
    status_code, response = decode_auth_token(auth_token)

    if status_code != 200:
        message = {"message": response}
        response = jsonify(message)
        response.status_code = status_code
        return response
    else:
        mongo.db.token_trash.insert({"token": auth_token})
        message = {"message": "Successfully logged out"}
        response = jsonify(message)
        response.status_code = status_code
        return response


def decode_auth_token(auth_token):
    """Decode the auth token."""
    blacklisted = mongo.db.token_trash.find_one({"token": auth_token})

    # If there is an expired token, then blacklisted variable will have dictionary instead of None
    if blacklisted is not None:
        return 401, 'Session was logged out. Please log in again.'

    else:
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            return 200, payload['sub']
        except jwt.ExpiredSignatureError:
            return 401, 'Session expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 401, 'Invalid token. Please log in again.'


def encode_auth_token(user_id, remember):
    """Generate the Auth Token."""
    # try:
    if remember is True:
        payload = {
            # This tells the time the token was created
            'iat': datetime.datetime.utcnow(),
            # This gives the user id of the user that created token
            'sub': user_id
        }
    else:
        payload = {
            # This tells the time the token will expire
            'iat': datetime.datetime.utcnow(),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
            'sub': user_id
        }
    return jwt.encode(payload, app.config.get('SECRET_KEY'),
                      algorithm='HS256')
    # except Exception as e:
    #     return e


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
