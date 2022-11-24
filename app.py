import os
from flask import Flask, render_template, redirect, request, session, url_for
import sqlite3
from flask_session import Session

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

con = sqlite3.connect("portfolio.db", check_same_thread=False)
db = con.cursor()
# db.execute("CREATE TABLE users(id INTEGER, username TEXT, password_hash INTEGER, PRIMARY KEY(id));")


@app.route("/")
def index():
   return render_template("index.html")

@app.route("/scheduler", methods=["GET","POST"])
def scheduler():
   if request.method == "POST":
      stock = request.form.get("stock")
      return render_template("schedulerpost.html", stock=stock)
   else:
      return render_template("scheduler.html")

@app.route("/register", methods=["GET","POST"])
def register():
   if request.method == "POST":
      temp = db.execute("SELECT MAX(id) from users")
      id = 1
      username = request.form.get("username")
      password = request.form.get("password")
      db.execute("INSERT INTO users VALUES(?, ?, ?)", id, request.form.get("username"), request.form.get("password"))
      con.commit()
      return render_template("registerpost.html", test = temp.fetchone())
   else:
      return render_template("register.html")

if __name__ == '__main__':
   app.run(debug=True)