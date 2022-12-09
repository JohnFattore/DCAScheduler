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
# db.execute("CREATE TABLE stocks(id INTEGER, symbol TEXT, shares INTEGER, costbasis INTEGER, user_id INTEGER, PRIMARY KEY(id),FOREIGN KEY(user_id) REFERENCES users(id));")


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
      db.execute("SELECT MAX(id) from users")
      id = int(db.fetchone()[0]) + 1
      username = request.form.get("username")
      password = request.form.get("password")
      db.execute("INSERT INTO users (id, username, password_hash) VALUES(?, ?, ?)", (id, request.form.get("username"), request.form.get("password")))
      con.commit()
      session["username"] = username
      return render_template("registerpost.html", test = id)
   else:
      return render_template("register.html")

@app.route("/login", methods=["GET","POST"])
def login():
   if request.method == "POST":
      username = request.form.get("username")
      password = request.form.get("password")
      db.execute("SELECT password_hash FROM users WHERE username = ?", [username])
      if password != (db.fetchone()[0]):
            return render_template("login.html", test = "Wrong Password")
      session["username"] = username
      return render_template("loginpost.html", test = session["username"])
   else:
      return render_template("login.html")

@app.route("/assetmanager", methods=["GET","POST"])
def assetmanager():
   if request.method == "POST":
      db.execute("SELECT MAX(id) from stocks")
      id = int(db.fetchone()[0]) + 1
      symbol = request.form.get("symbol")
      shares = request.form.get("shares")
      costbasis = request.form.get("costbasis")
      db.execute("SELECT ID from users WHERE username = ?", (session["username"],))
      user_id = db.fetchone()[0]
      db.execute("INSERT INTO stocks (id, symbol, shares, costbasis, user_id) VALUES(?, ?, ?, ?, ?)", (id, symbol, shares, costbasis, user_id))
      con.commit()
      return render_template("assetmanager.html", test = session["username"])
   else:
      if session["username"] == None:
         return render_template("login.html", test = "Must be login")
      return render_template("assetmanager.html", test = "GET")

if __name__ == '__main__':
   app.run(debug=True)