
menu = {
    "menu": [
        {
          "name": "fish",
          "price": 20
        },
        {
          "name": "chicken",
          "price": 20
        },
        {
          "name": "pasta",
          "price": 10
        }
    ]
}

order_form = {
    "name": "chicken",
    "price": 30,
    "paid": False
}


if __name__ == "__main__":
    from flask import Flask
    from flask_pymongo import PyMongo
    app = Flask(__name__)
    app.config["MONGO_URI"] = "mongodb://localhost:27017/demodb"
    mongo = PyMongo(app)

    for item in menu["menu"]:
        mongo.db.menu.insert(item)

    app.run(host='localhost', port='32400')
