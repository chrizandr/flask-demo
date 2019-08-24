from flask import Flask
from flask import (
    request, render_template,
    redirect, url_for, flash, jsonify
)
from flask_pymongo import PyMongo
import pdb

user_template = {
    "fname": "String",
    "lname": "String",
    "gender": "String",
    "dob": "YYYY-MM-DD",
    "address": "String",
    "phone": "String",
    "email": "String",
    "notes": "String"
}

app = Flask(__name__)
# This is the password to encode/decode the token
app.secret_key = "DFDKFNWEFOWEFIWV"
app.config["MONGO_URI"] = "mongodb://localhost:27017/demodb"
# The connection to the MongoDB server, this is common for multiple threads of the app
mongo = PyMongo(app)


@app.route("/subscribers/list", methods=["POST"])
def sublist():
    form_data = request.form
    if "page_number" not in form_data or "limit" not in form_data:
        return jsonify({"message": "Wrong format of request"})
    if "cours_id" in form_data:
        return None
    page_number = int(form_data["page_number"])
    limit = int(form_data["limit"])
    all_users = mongo.db.subscribers.find()
    users = all_users[(page_number-1)*limit: (page_number-1)*limit + limit]
    users = [format_data(x) for x in users]
    if len(users) == 0:
        return jsonify({"message": "page_number/limit is Wrong"})
    return jsonify({"list": users})


@app.route("/subscribers/create", methods=["PUT"])
def create():
    form_data = request.form
    new_user = create_user(**form_data)
    mongo.db.subscribers.insert(new_user)
    return jsonify({"message": "New user created"})


def create_user(fname, lname, gender, dob, address, phone, email, notes):
    """Create a new user."""    # Doc string
    # Things to check
    assert type(fname) is str
    assert type(lname) is str
    assert type(gender) is str
    date = [int(x) for x in dob.split('-')]
    assert type(address) is str
    assert type(phone) is str
    assert type(email) is str
    assert type(notes) is str

    # Create the new user
    new_user = user_template.copy()
    new_user["fname"] = fname
    new_user["lname"] = lname
    new_user["gender"] = gender
    new_user["dob"] = dob
    new_user["address"] = address
    new_user["phone"] = phone
    new_user["email"] = email
    new_user["notes"] = notes

    return new_user


def format_data(mongo_dict):
    """Format the mongodb dictionary into user format."""
    keys = list(mongo_dict.keys())
    for key in keys:
        if key not in user_template:
            # Delete the entry with that key from dictionary
            mongo_dict.pop(key)
    return mongo_dict



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
    pdb.set_trace()
