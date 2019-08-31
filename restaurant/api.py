from flask import Flask
from flask import (
    request, render_template,
    redirect, url_for, flash, jsonify
)
from flask_pymongo import PyMongo
from format import menu, order_form
import pdb

app = Flask(__name__)
# This is the password to encode/decode the token
app.secret_key = "DFDKFNWEFOWEFIWV"
orders = []
latest_order_id = 0


@app.route("/menu", methods=["GET"])
def getmenu():
    menu_obj = menu.copy()
    return jsonify(menu_obj)


@app.route("/order", methods=["GET"])
def order():
    global latest_order_id, orders
    items = request.args.getlist('item')
    if len(items) == 0:
        return jsonify({"message": "This is a bad request"}), 400
    else:
        for item in items:
            # Make a new order for every item
            new_order = order_form.copy()
            new_order["id"] = latest_order_id + 1
            new_order["item"] = item
            latest_order_id = latest_order_id + 1
            # add the new order to the orders list
            orders.append(new_order)
        # Give confirmation message to the customer
        return jsonify({"message": "Your food is being prepared in the kitchen"})


@app.route("/order", methods=["DELETE"])
def delete_order():
    global orders
    delete_order_ids = request.args.getlist('orderid')
    delete_order_ids = [int(x) for x in delete_order_ids]

    new_order_list = []
    for order in orders:
        if order["id"] not in delete_order_ids:
            new_order_list.append(order)

    orders = new_order_list

    return jsonify({"message": "Your order has been cancelled"})


@app.route("/orders", methods=["GET"])
def get_all_orders():
    global orders
    return jsonify({"orders": orders})


@app.route("/pay", methods=["POST"])
def pay_for_item():
    global orders
    order_ids = request.args.getlist('orderid')
    order_ids = [int(x) for x in order_ids]

    money = request.form.copy()
    total = get_total(money)
    total_due = 0

    for order in orders:
        if order["id"] in order_ids:
            total_due = total_due + order["price"]

    if total != total_due:
        return jsonify({"message": "Money is wrong"}), 400
    else:
        for order in orders:
            if order["id"] in order_ids:
                order["paid"] = True
        return jsonify({"message": "Food has been paid"}), 200


def get_total(money):
    euro_1 = int(money.get("1 euro", 0))
    euro_10 = int(money.get("10 euros", 0))
    euro_5 = int(money.get("5 euros", 0))

    total_amount = euro_1 + 5*euro_5 + 10*euro_10
    return total_amount

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
