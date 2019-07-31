from flask import Flask
from flask import request, render_template, redirect, url_for
from models import User, engine

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
import pdb


app = Flask(__name__)
db_session = scoped_session(sessionmaker(bind=engine))
print("Configuring app...")
app.secret_key = "DFDKFNWEFOWEFIWV"


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template('register.html')

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        new_user = User(username, password, email)
        db_session.add(new_user)
        db_session.commit()
        return redirect(url_for('register'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
