import re
from datetime import datetime
import random
import pandas as pd
from pathlib import Path

from flask import (Response, Flask, flash, redirect, render_template, request,
                   send_from_directory, session, url_for)
from flask_mail import Mail, Message


app = Flask(__name__)

# configuration of mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'codescatter8980@gmail.com'
app.config['MAIL_PASSWORD'] = 'ynqolwjdibmzudao'
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

@app.route("/", methods=["GET","POST"])
def home():
    return render_template("index-job.html")

@app.route("/about", methods=["GET","POST"])
def about():
    return render_template("about-simple.html")

@app.route("/services", methods=["GET","POST"])
def services():
    return render_template("services-classic.html")

@app.route("/contact", methods=["GET","POST"])
def contact():
    if request.method=="POST":
        name = request.form["name"]
        email = request.form["email"]
        number = request.form["number"]
        messages = request.form["message"]

        df1 = pd.read_csv("contact_data.csv")

        df1 = df1.append(pd.DataFrame([[name, email, number, messages]], columns=["name", "email", "number", "message"]))
        df1.to_csv("contact_data.csv", index=False)

        msg = "you are register successfully"
        return render_template("contact-us-modern.html", msg=msg)
    else:
        return render_template("contact-us-modern.html")


@app.route("/login", methods=["GET","POST"])
def login():
    if request.method=="POST":
        username = request.form["name"]
        password = request.form["password"]

        df = pd.read_csv("register_user.csv")
        for var,var1 in zip(df["Username"], df["Password"]):
            if username==var and password==var1:
                session["username"] = username
                return redirect(url_for('home',  _external=True, _scheme="http"))

        return render_template("login.html", msg="your credential doesn't match!!")
    else:
        return render_template("login.html")

# That is route for sending forget mail for user
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method=="POST":
        full_name = request.form["name"]
        username = request.form["username"]
        email = request.form["email"]
        number = request.form["number"]
        password = request.form["password"]

        df = pd.read_csv("register_user.csv")
        for var in df["Username"]:
            if username==var:
                msg="username already exit!"
                return render_template("register.html", msg=msg)

        df = df.append(pd.DataFrame([[full_name,username,email, number, password]], columns=['Full_name','Username','Email','number','Password']))
        df.to_csv("register_user.csv", index=False)

        msg = "you are register successfully"
        return render_template("register.html", msg=msg)
    else:
        return render_template("register.html")

if __name__ == "__main__":
    # db.create_all()
    app.run(
        host='127.0.0.1',
        port='8000',
        debug=True)

