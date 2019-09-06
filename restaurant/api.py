from flask import Flask
from flask import (
    request, render_template,
    redirect, url_for, flash, jsonify
)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from format import menu, order_form
import pdb

app = Flask(__name__)
# This is the password to encode/decode the token
app.secret_key = "DFDKFNWEFOWEFIWV"
app.config["MONGO_URI"] = "mongodb://localhost:27017/demodb"
# The connection to the MongoDB server, this is common for multiple threads of the app
mongo = PyMongo(app)


@app.route("/menu", methods=["GET"])
def getmenu():
    menu_obj = []
    for x in mongo.db.menu.find():
        x['_id'] = str(x['_id'])
        menu_obj.append(x)

    return jsonify(menu_obj)


@app.route("/order", methods=["GET"])
def order():
    items = request.args.getlist('item')
    if len(items) == 0:
        return jsonify({"message": "This is a bad request"}), 400
    else:
        for item in items:
            menu_item = mongo.db.menu.find_one({"name": item})
            if menu_item is None:
                return jsonify({"message": "This is a bad request"}), 400
            else:
                new_order = order_form.copy()
                new_order["name"] = item
                new_order["price"] = menu_item["price"]
                # add the new order to the orders list
                mongo.db.orders.insert(new_order)
        # Give confirmation message to the customer
        return jsonify({"message": "Your food is being prepared in the kitchen"})


@app.route("/order", methods=["DELETE"])
def delete_order():
    delete_order_ids = request.args.getlist('orderid')

    for order_id in delete_order_ids:
        mongo.db.orders.remove({"_id": ObjectId(order_id)})

    return jsonify({"message": "Your order has been cancelled"})


@app.route("/orders", methods=["GET"])
def get_all_orders():
    # orders = [x for x in mongo.db.orders.find()]
    orders = []
    for x in mongo.db.orders.find():
        x['_id'] = str(x['_id'])
        orders.append(x)

    return jsonify({"orders": orders})


@app.route("/pay", methods=["POST"])
def pay_for_item():
    global orders
    order_ids = request.args.getlist('orderid')
    order_ids = [x for x in order_ids]

    money = request.form.copy()
    total = get_total(money)
    total_due = 0

    orders = [x for x in mongo.db.orders.find()]
    for order in orders:
        if str(order['_id']) in order_ids:
            total_due = total_due + order["price"]

    if total < total_due:
        return jsonify({"message": "Money is wrong"}), 400
    else:
        for order in orders:
            if str(order['_id']) in order_ids:
                mongo.db.orders.remove({"_id": order["_id"]})

        return jsonify({"message": "Food has been paid"}), 200


def get_total(money):
    euro_1 = int(money.get("1 euro", 0))
    euro_10 = int(money.get("10 euros", 0))
    euro_5 = int(money.get("5 euros", 0))

    total_amount = euro_1 + 5*euro_5 + 10*euro_10
    return total_amount


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
