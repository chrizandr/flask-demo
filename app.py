"""Main application."""
import datetime
import jwt
import pdb

from flask import Flask
from flask import (
    request, render_template,
    redirect, url_for, flash
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
    auth_token = request.args.get('token', None)
    if auth_token is None:
        flash("Please log in to continue")
        return redirect(url_for('login'))

    # Assume black box
    authenticated, response = decode_auth_token(auth_token)

    if not authenticated:
        flash(response)
        return redirect(url_for('login'))

    user_id = response
    return render_template("index.html", user=user_id, auth_token=auth_token)


@app.route('/register', methods=["GET", "POST"])
def register():
    """Register."""
    if request.method == "GET":
        return render_template('register.html')

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        email = request.form['emailid']

        mongo.db.users.insert({"username": username, "password": bcrypt.encrypt(password),
                              "email": email})

        flash("Successfully registered, please login")
        return redirect(url_for('login'))


@app.route('/forgot', methods=["GET", "POST"])
def forgot():
    """Register."""
    if request.method == "GET":
        return render_template('forgot.html')

    if request.method == "POST":
        email = request.form['email']

        # Code here to manage password
        return redirect(url_for('login'))


@app.route('/login', methods=["GET", "POST"])
def login():
    """Login."""
    if request.method == "GET":
        return render_template('login.html')

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        remember = request.form.get("remember", "not_clicked")

        is_remember = remember == "clicked"

        error = None
        user = mongo.db.users.find_one({"username": username})

        if user is None:
            error = 'Invalid username.'
        else:
            if not bcrypt.verify(password, user["password"]):
                error = 'Incorrect password.'
            # pass_hash = bcrypt.encrypt(password)
            # if not pass_hash == user["password"]:
            #     error = 'Incorrect password.'

        if error is None:
            auth_token = encode_auth_token(str(user["_id"]), is_remember)
            return redirect(url_for('index', token=auth_token))
            # /?token=sdajndjnodnqoidaismdoaisdo
        else:
            flash(error)
            return redirect(url_for('login'))


@app.route('/logout', methods=["GET"])
def logout():
    """Logout."""
    auth_token = request.args.get('token', None)

    if auth_token is None:
        flash("Please log in to continue")
        return redirect(url_for('login'))

    authenticated, response = decode_auth_token(auth_token)
    if not authenticated:
        flash(response)
        return redirect(url_for('login'))

    mongo.db.expired_tokens.insert({"token": auth_token})
    flash("Successfully logged out")
    return redirect(url_for('login'))


def decode_auth_token(auth_token):
    """Decode the auth token."""
    blacklisted = mongo.db.expired_tokens.find_one({"token": auth_token})

    if blacklisted is not None:
        return False, 'Session was logged out. Please log in again.'

    try:
        payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
        return True, payload['sub']
    except jwt.ExpiredSignatureError:
        return False, 'Session expired. Please log in again.'
    except jwt.InvalidTokenError:
        return False, 'Invalid token. Please log in again.'


def encode_auth_token(user_id, remember=False):
    """Generate the Auth Token."""
    try:
        if remember:
            payload = {
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
        else:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
        return jwt.encode(
            payload,
            app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        return e


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
